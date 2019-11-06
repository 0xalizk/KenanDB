import random,sys
randomize = random.SystemRandom().choice

##################################################### 
def update_network(network,source,target,sign,evidence):
    if (source,target) not in network.keys():
        network[(source,target)]={'count':0, 'sign':[],'evidence':evidence}
    network[(source,target)]['count']+=1
    network[(source,target)]['sign'].append(sign)
##################################################### 

RAW_Files = ['raw/network_tf_gene.txt', 'raw/network_tf_tf.txt']
network = {}
sign_conflict ={}
###################### TF-GENE ###################### 
overall=0
print()
for f in RAW_Files:
    raw_file = open(f,'r').readlines()
    i = 0
    for line in raw_file:
        if line[0].strip()=='#':
            continue #skip comment lines
        line = line.strip().split()
        source,target,sign,evidence = line[0].strip().lower(), line[1].strip().lower(), line[2].strip().lower(), line[-1].strip().lower()
        if evidence not in ['strong','confirmed']:
            continue # skip weak-evidence (or null-evidence) interactions
        if sign not in ['+','-']: 
            sign = randomize(['+','-'])
        update_network(network,source,target,sign,evidence)
        i+=1
    overall+=i
    print((f.split('/')[-1] + ':').ljust(25,' ')+str(i).ljust(5,' ')+' interactions')

netfile = open('processed/Bacteria-RegulonDB_extracted.txt','w')
netfile.write("regulator \t regulated \t sign")

for (source,target) in network.keys():
    sign=None
    #if len(network[(source,target)]['sign'])>1:
        #print('\t'.join([source,target,' '.join(network[(source,target)]['sign'])]))
    sign = randomize(network[(source,target)]['sign']) 
    netfile.write('\n'+'\t'.join([source,target, sign, network[(source,target)]['evidence']]))
print('\nOverall: '.ljust(10,' ')+str(overall).ljust(5,' ')+' interactions, '+str(sum([network[k]['count']-1 for k in network.keys()]))+' of which are duplicates')
#print (str( len ([k for k in network.keys() if network[k]['count']>1])))
#print (str(len([k for k in network.keys() if len(network[k]['sign'])>1])))
print()
