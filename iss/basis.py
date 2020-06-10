
'''
    Interprets a binary number as a partition by intervals and
    return the corresponding composition.
    A 0 in the i-th position means i and (i+1) belongs to the same partition
'''
def binary_to_composition( binNum , L ):
	
    comp = []
    y = 1 
    
    for i in range(L) : 
        if not ( binNum & (1<<i) ) :
            comp.append(y)
            y = 0
        y += 1
    
    comp.append(y)
    comp.reverse()
    
    return(comp)
 
'''
    Give all the compostiions of the numbers 0..L in lexicographic order
''' 
def all_compositions_upto(L):
    for lev in range(L):
        for ind in range(1<<lev):
            yield(binary_to_composition(ind,lev))


def prefix_tree_hash( comp , level ):
    s=len(comp)
    le=level
    for x in comp :
        s += ((1<<le)-1) - ((1<<(le-x+1)) - 1)
        le -= x
    return s

def 



'''
  Generate all the compostions using a prefix tree
'''
def ptree( word=[] , level=5 ):
    if level < 0: return

    print(hash(word,5),word)

    for k in range(level+1):
        word.append(k+1)
        ptree( word , level - (k+1) )
        word.pop()

