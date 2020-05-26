
import numpy.random as rnd
import numpy as np

    
def recursive_compositions(y,L,stdBasis=True): 

    # Stack Info
    WordStack = [[]]
    InnerStack = [ [1]*len(y) ] 
    LevelStack = [L]
    LastStack = [1]
    
    # Return Info
    Basis = []
    Signature = []
    
    while len(LevelStack) > 0 :
        level = LevelStack.pop()
        word = WordStack.pop()
        inner = InnerStack.pop()
        last = LastStack.pop()
        
        Basis.append( word )
        Signature.append( last )
        
        for s in reversed(range(1,level+1)) :
        
            outer = [ v**s for v in y ]
            
            auxInner = np.multiply(inner,outer).cumsum().tolist()
            auxLast = auxInner.pop()
            auxInner.insert(0, 0)
            
        
            word.append(s)
            WordStack.append(word.copy())
            word.pop()
            
            LevelStack.append( level - s )
            InnerStack.append( auxInner )
            LastStack.append(auxLast)
    
    return Basis
    
    # This 'if' is pretty much not optimal !!! 
    if stdBasis : 
        nb = len(Basis)
        B = [ (sum(Basis[i]),Basis[i],i) for i in range(nb) ]
        B.sort()
        Signature = [ Signature[b[2]] for b in B[1:] ]
    
    return(Signature)
    
    
def rec_ISS(x,L):
    if L <= 0 : return None
    
    # Obtain the [non-zero] increments
    dx = list(filter(lambda v: v != 0, np.diff(x)))
    dx.insert( 0 , x[0] )
    
    return recursive_compositions(dx,L)
    
