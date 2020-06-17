
class pTree:
    def __init__(self, level):
        self._level = 0
        self._words = [[]]
        self.parents = [-1] 
        self.key = [0]
        self._expand(level)
        self._level = level
    
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        if level > self._level:
            self._expand(level)
        else:
            self._contract(level)
        self._level = level
    
    @property
    def basis(self):
        if( len(self._words) >= 1<<self._level ): 
            return self._words[:1<<self._level]
        
        for k in range(len(self._words),1<<self._level):
            wd = self._words[ self.parents[k] ].copy()
            wd.append( self.key[k] )
            self._words.append( wd )
        
        return self._words
    
    def _contract(self,level):
        self.parents = self.parents[:newL]
        self.key = self.key[:newL]
        if(len(self._words)==prevL):
            self._words = self._words[:newL]
        
    
    def _expand(self,level):
    
        prevL = 1<<self._level
        newL = 1<<level 
                
        for k in range(prevL,newL):
            j=0
            l = k
            while k&1: 
                k >>= 1 
                j+= 1
            k>>=1
            self.parents.append(k)
            self.key.append(j+(k!=0))
