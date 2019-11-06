import requests, xmltodict as xml2dict,sys
from pprint import pprint
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import quote as formatURL # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote
myprint, myflush = sys.stdout.write, sys.stdout.flush
################################################################################################################
def log(response):
    #pp = pprint.PrettyPrinter(indent=1)
    logfile = open ('psicquic_services_status.log','w')
    logfile.write('\nREST requets were executed on '+ str(datetime.now())+', this was the active PSICQUIC services then: \n\n')
    pprint(response, stream=logfile)
    return logfile
################################################################################################################
def Queries():
    return { 'Human-PSICQUIC': formatURL("taxidA:9606 AND taxidB:9606 AND type:\"direct interaction\" AND detmethod:\"experimental interaction detection\""),
             'Yeast-PSICQUIC': formatURL("taxidA:559292 AND taxidB:559292 AND type:\"direct interaction\" AND detmethod:\"experimental interaction detection\""),
             'Plant-PSICQUIC': formatURL("taxidA:3702 AND  taxidB:3702 AND type:\"direct interaction\" AND detmethod:\"experimental interaction detection\"")
             }
################################################################################################################
def update_network(net,A,B):
    if (A,B) not in net.keys():
        net[(A,B)] = 0
    net[(A,B)] += 1
    return
################################################################################################################
def dump_network(net,file):
    netfile = open(file,'w')
    netfile.write('InteractorA\tInteractorB')
    for (interactorA,interactorB) in net.keys():
        netfile.write('\n'+interactorA +'\t'+interactorB)
################################################################################################################

ACTIVE   = requests.get("http://www.ebi.ac.uk/Tools/webservices/psicquic/registry/registry?action=ACTIVE&format=xml")
response = xml2dict.parse(ACTIVE.content) 
logfile  = log (response)

for Q in sorted(Queries().keys()):
    myprint('='*100+'\n'+' '*40+Q+' '*40+'\n'+'='*100)

    total_hits = 0
    unique = {}
    for service in response['registry']['service']: 
        query   = service['restUrl']+'query/'+Queries()[Q]#+'?maxResults=2'
        myprint('\n'+(service['name']+' ').ljust(25,'.'))
        results = urlopen(query).read().splitlines()#('\n')
        myprint('   '+str(len(results)).ljust(6, ' ')+' hits')
        for row in results:
            total_hits +=1
            row = row.decode('UTF-8').strip().split('\t')
            interactorA, interactorB = row[0].split(':')[1], row[1].split(':')[1]
            update_network(unique,interactorA,interactorB)
        myprint(' .. processed'*(len(results)>0))
        myflush()
    dump_network(unique,Q+'_extracted.txt')
    duplicates = sum([unique[k]-1 for k in unique.keys()])
    myprint('\n\nTotal hits: '+str(total_hits)+',\tUnique hits: '+str(total_hits-duplicates)+' ('+str(duplicates)+' duplicates)\n')

