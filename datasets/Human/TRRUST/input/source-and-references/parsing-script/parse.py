import collections, random, operator
######################################################################
def pick_sign(S):
    if S['+']> S['-'] and S['+']>S['?']:
        return '+'
    if S['-']> S['+'] and S['-']>S['?']:
        return '-'
    else:
        return random.SystemRandom().choice(['+','-'])
######################################################################
lines = (open ('../trrust_rawdata.txt','r')).readlines()

interactions = {}
activations, repressions, unknowns = 0,0,0
id = 1
for i in lines:
    i = i.strip().split()
    source, target, sign, refs = i[0].strip(), i[1].strip(), i[2].strip(), i[3].strip().split(';')
    if (source, target) not in interactions.keys():
        interactions[(source,target)]={}
        interactions[(source,target)]['id']=id
        interactions[(source,target)]['count']=0
        interactions[(source,target)]['signs']={}  
        interactions[(source,target)]['signs']['+']=0
        interactions[(source,target)]['signs']['-']=0
        interactions[(source,target)]['signs']['?']=0
        

    interactions[(source,target)]['count']+=1

    if sign.lower() == 'activation':
        interactions[(source,target)]['signs']['+']+= len(refs)
        activations+=1
    elif sign.lower() == 'repression':
        interactions[(source,target)]['signs']['-']+= len(refs)
        repressions+=1
    else:
        interactions[(source,target)]['signs']['?']+= len(refs)
        unknowns+=1
    id+=1

print ('Total interactions: '.ljust(30,' ')    + str(len(lines)))
print ('Unique interactions: '.ljust(30,' ')    + str(len(interactions.keys())))
print ('Promotional interactions: '.ljust(30,' ')    + str(activations).ljust(7,' ')+str(activations*100/len((interactions.keys())))+' %')
print ('Inhibitory interactions: '.ljust(30,' ')    + str(repressions).ljust(7,' ')+str(repressions*100/len((interactions.keys())))+ ' %')
print ('Unknown-effect interactions: '.ljust(30,' ')    + str(unknowns).ljust(7,' ')+str(unknowns*100/len((interactions.keys())))+' %')

print('\nInteractions\t[number of times it was reported +]\t[-]\t[?]')
print('='*50)

outfile = open ('Human-TRRUST_extracted.txt','w')
outfile.write('source\ttarget\tsign')
for record in sorted(interactions.items(), key=lambda y:y[1]['id']):
    # record = (('ZNF300', 'CDKN1A'), {'signs': {'+': 0, '?': 0, '-': 1}, 'count': 1, 'id': 8188})
    key = record[0]
    source,target,sign = key[0], key[1], pick_sign(interactions[key]['signs'])
    if interactions[key]['count']>1:        
        print(str(key).ljust(30,' ')+'+ ('+str(interactions[key]['signs']['+'])+'), - ('+str(interactions[key]['signs']['-'])+'), ? ('+str(interactions[key]['signs']['-'])+')\tchosen: '+sign)
    outfile.write('\n'+'\t'.join([source,target,sign]))
        