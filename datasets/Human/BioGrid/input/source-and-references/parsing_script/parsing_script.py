# 0		BioGRID Interaction ID	
# 1 	Entrez Gene Interactor A	
# 2 	Entrez Gene Interactor B	
# 3		BioGRID ID Interactor A	
# 4		BioGRID ID Interactor B	
# 5		Systematic Name Interactor A	
# 6		Systematic Name Interactor B	
# 7		Official Symbol Interactor A	
# 8		Official Symbol Interactor B	
# 9		Synonyms Interactor A	
# 10	Synonyms Interactor B	
# 11	Experimental System	
# 12	Experimental System Type	
# 13	Author	
# 14	Pubmed ID	
# 15	Organism Interactor A	
# 16	Organism Interactor B	
# 17	Throughput	
# 18	Score	
# 19	Modification	
# 20	Phenotypes	
# 21	Qualifications	
# 22	Tags	
# 23	Source Database


# name....................................TaxID..............Total number of interactions (with duplicates) in BIOGRID-MV-Physical-3.4.149.tab2.zip
#==================================================================================================================================================
# Homo Sapiens (Human).....................9606..........................121649 					
# Arabidopsis thaliana (Plant).............3702..........................9713  					
# Caenorhabditis elegans (Worm)............6239..........................812  					
# Drosophila melanogaster (Fly)............7227..........................1633  					
# Mus musculus (Mouse).....................10090.........................5035  					
# Saccharomyces cerevisiae S288C(Yeast)....559292........................60271  	

####################################################################################################
def Extract(Organism, MV=1):
    outfile = open (Organism['Name']+'-BioGrid_extracted.txt','w')
    outfile.write('source_entrezID\ttarget_entrezID')
    selected = [k for k in Organism['network'].keys() if Organism['network'][k]>=MV]
    for key in selected:
        outfile.write('\n'+str(key[0])+'\t'+str(key[1]))
    print (('extracted '+Organism['Name']+': ').ljust(20,' ')+str(len(selected)))
####################################################################################################

lines = (open('../BIOGRID-MV-Physical-3.4.149.tab2.txt','r')).readlines()[1:] # skip the column headers

NETWORKS =     {9606:   {'Name':'Human',  'network':{}},
                3702:   {'Name':'Plant',  'network':{}},
                6239:   {'Name':'Worm',   'network':{}},
                7227:   {'Name':'Fly',    'network':{}},
                10090:  {'Name':'Mouse',  'network':{}},
                559292: {'Name':'Yeast',  'network':{}}} 

for i in lines:
    i=i.strip().split('\t')

    OrgA, OrgB = int(i[15].strip()),int(i[16].strip())
    if OrgA != OrgB:
        continue # skip interactions where organisms don't match
    if OrgA not in NETWORKS.keys():
        continue
    source,target = int(i[1].strip()),int(i[2].strip())
    # treat all interactions as undirected
    if (source,target) not in NETWORKS[OrgA]['network'].keys() and (target,source) not in NETWORKS[OrgA]['network'].keys() :
        NETWORKS[OrgA]['network'][(source,target)]=1
    elif (source,target) in NETWORKS[OrgA]['network'].keys():
        NETWORKS[OrgA]['network'][(source,target)]+=1
    else:
        assert (target,source) in NETWORKS[OrgA]['network'].keys()
        NETWORKS[OrgA]['network'][(target,source)]+=1

for org in NETWORKS.keys():
    print(NETWORKS[org]['Name'].ljust(20,' ')+str(sum(NETWORKS[org]['network'].values())).ljust(10,' ')+'total interactions, \t\t',end='')
    print(str(len(NETWORKS[org]['network'].keys())).ljust(10,' ')+'unique interactions, ')
print("\nwriting out network files:")

Extract(NETWORKS[9606], MV=4) # MV=x ==> only interactions multi-validated more than x times will be extracted
Extract(NETWORKS[3702]) # not supplying MV means "extract everything"
Extract(NETWORKS[6239])
Extract(NETWORKS[7227])
Extract(NETWORKS[10090])
Extract(NETWORKS[559292], MV=3)
