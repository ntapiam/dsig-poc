
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
def fill(self):
        
    # Stack Info
    WordStack = [[]]
    LevelStack = [self._level]
    ParentStack = [-1]

    while len(LevelStack) > 0 :
        level = LevelStack.pop()
        word = WordStack.pop()
        parent = ParentStack.pop()
    
        self.words.append(word)
        self.parents.append(parent)
        
        parent = len(self.words)-1
    
        for s in reversed(range(1,level+1)) :
    
            word.append(s)
            WordStack.append(word.copy())
            word.pop()
        
            LevelStack.append( level - s )
            
            ParentStack.append(parent)



def binaryRepresentation(level=5):
    
    parents=[-1]
    face=[0]
    
    for k in range(1,1<<level):
        j=0
        l = k
        while k&1: 
            k >>= 1 
            j+= 1
        k>>=1
        parents.append(k)
        face.append(j+(k!=0))
    
    return [parents,face]
    
    
    


