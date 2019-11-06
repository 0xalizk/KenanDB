import os, operator


def parser(path):
    lines = open (path,'r')
    INTERACTIONS, DATABASES, ROWS, DUPLICATES = {}, {}, 0, 0
    total_rows = 0
    try:
        while True:
            interaction       = next(lines).strip().split(',')
            ROWS              += 1
            source, target, db = interaction[0].strip().replace('\"',''), interaction[2].strip().replace('\"',''), interaction[4].strip().replace('\"','')
            if (source,target) not in INTERACTIONS.keys():
                INTERACTIONS[(source,target)]  = 1
            else:
                INTERACTIONS[(source,target)] +=1
                DUPLICATES +=1
            if db in DATABASES.keys():
                DATABASES[db] +=1
            else:
                DATABASES[db]=1
    except:
        print(str(ROWS).ljust(10,' ')+' interactions, \tnumber of duplicate interactions = '+str(len([key for key in INTERACTIONS.keys() if INTERACTIONS[key]>1])))
        pass#EOF
    assert ROWS == sum(INTERACTIONS.values()) 
    unique = len(INTERACTIONS.keys())
    print('\n'+str(ROWS)          +' total interactions')
    print(     str(DUPLICATES)    +' duplicates')
    print(     str(unique)        +' unique interactions')
    print(     str(len(set([x[0] for x in INTERACTIONS.keys()]+[x[1] for x in INTERACTIONS.keys()])))+' unique genes')
    print("The most duplicated interactions:")
    common = sorted(INTERACTIONS.items(), key=operator.itemgetter(1), reverse=True)
    for i in set([e[1] for e in common]):
        print ('\t'+str(len([c for c in common if c[1]==i])).ljust(10,' ') +' interactions are duplicated \t'+ str(i-1)+' \t times ')

    print("\nDatabases: "+str([str(key)+':'+str(DATABASES[key]) +'('+ str(round((DATABASES[key]/unique)*100,2))+' %)' for key in DATABASES.keys()]))

    with open (path.split('/')[-1].split('_')[0]+'-Liu_extracted.txt','w') as f:
        f.write('source\ttarget')
        for e in INTERACTIONS.keys():
            f.write('\n'+e[0]+'\t'+e[1])
    print('='*100)

parser('../Human_export_Thu_Jun_15_04_41_14_UTC_2017.csv')
parser('../Mouse_export_Thu_Jun_15_04_42_58_UTC_2017.csv')

