from urllib.request import urlopen
import sys
import xml.etree.ElementTree as ET

# adapted from : https://github.com/PSICQUIC/psicquic-webservice/blob/master/src/example/python/read-all-psicquic.py
# see also: http://python-guide-pt-br.readthedocs.io/en/latest/scenarios/xml/

#########################################################################################################################  
class PsicquicService:
    def __init__(self, name, restUrl):
        self.name = name
        self.restUrl = restUrl
#########################################################################################################################  
def readURL(url):
    try:
        fileHandle = urlopen(url)
        content = fileHandle.read()
        fileHandle.close()
    except IOError:
        print ('Cannot open URL ' % url)
        content = ''

    return content
#########################################################################################################################  
def readServicesFromRegistry(state):
    registryActiveUrl = 'http://www.ebi.ac.uk/Tools/webservices/psicquic/registry/registry?action='+state+'&format=xml'
    content           = readURL(registryActiveUrl)
    doc               = ET.fromstring(content)
    serviceNodes      = doc.findall(".")[0] #xpath.Evaluate('service', doc.documentElement)
    services          = []

    for serviceNode in serviceNodes:
        name    = serviceNode[0].text #serviceNode.getElementsByTagName('name')[0].firstChild.nodeValue
        restUrl = serviceNode[2].text #serviceNode.getElementsByTagName('restUrl')[0].firstChild.nodeValue
        service = PsicquicService(name, restUrl)
        services.append(service)
    return services
#########################################################################################################################  
def getXrefByDatabase(line, database):
   fields = line.split('|')

   for field in fields:
       parts = field.split(':')
       db = parts[0]
       value = parts[1].split('(')[0]
       if database == db:
           return value
   else:
    # if no db found, return the first field
        return fields[0]
#########################################################################################################################  
def countHits(psicquicRestUrl, query):
    psicquicUrl = psicquicRestUrl + 'query/' + query #+ '?firstResult=' + str(offset) + '&maxResults='
    psicquicResultLines = readURL(psicquicUrl).splitlines()
    return len(psicquicResultLines)
#########################################################################################################################  
def queryPsicquic(psicquicRestUrl, query, offset, maxResults):
    psicquicUrl = psicquicRestUrl + 'query/' + query + '?firstResult=' + str(offset) + '&maxResults=' + str(maxResults)
    print ('\t\tURL: ' + psicquicUrl)
    psicquicResultLines = readURL(psicquicUrl).splitlines()
    for line in psicquicResultLines:
        cols = line.split('\t')
        print ('\t' + getXrefByDatabase(cols[0], 'uniprotkb') + ' interacts with ' + getXrefByDatabase(cols[1], 'uniprotkb'))
#########################################################################################################################  

query = 'BBC1'
services = readServicesFromRegistry('ACTIVE')
print("Available services: ")
for service in services:
    print ('\t' + service.name.ljust(30,' ') + service.restUrl)#countHits(service.restUrl, query).ljust(6,' ')+' hits')

print("\nUnvailable services: ")
services = readServicesFromRegistry('INACTIVE')
for service in services:
    print ('\t' + service.name)
    




