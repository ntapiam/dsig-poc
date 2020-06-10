import collections
import functools


class Node:
    def __init__(self, value=None, key=(), weight=0, children=[]):
        self.value = value
        self.key = key
        self.antipode = []
        self.children = children
        self.weight = weight

    def dfs(self):
        yield self
        for c in self.children:
            yield from c.dfs()

    def bfs(self, callback=lambda n, c: c):
        queue = collections.deque([self])
        while queue:
            node = queue.popleft()
            func = functools.partial(callback, node)
            yield from map(func, node.children)
            queue.extend(node.children)

    def lookup(self, key):
        if not key:
            return self
        else:
            # Relies on knowledge of the tree. Change?
            try:
                return self.children[key[0] - 1].lookup(key[1:])
            except IndexError:
                print("Key not found")
                return None
                

    def contract(self, level):
        self.children = list(filter(lambda t: t.weight <= level, self.children))
        for t in self.children:
            t.contract(level)

    def expand(self, level):
        max_weight = len(self.children) + self.weight
        if max_weight < level:
            new = [
                Node(key=self.key + (k,), weight=self.weight + k)
                for k in range(max_weight - self.weight + 1, level - self.weight + 1)
            ]
            self.children = self.children + new
            for c in self.children:
                c.expand(level)

    def __del__(self):
        for c in self.children:
            del c
        del self


def gen_tree(level, root=Node()):
    root.children = [
        Node(key=(k,), weight=root.weight + k)
        for k in range(1, level - root.weight + 1)
    ]
    for t in root.children:
        gen_tree(level, t)
    return root




class pTree:
    def __init__(self, level):
        self.level = level
        self.words = []
        self.parents = [] 
        self.fill()
        
    def fill(self):
        
        # Stack Info
        WordStack = [[]]
        LevelStack = [self.level]
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
    
    def comp2index(self, comp ):
        s=len(comp)
        le=self.level
        for x in comp :
            s += ((1<<le)-1) - ((1<<(le-x+1)) - 1)
            le -= x
        return s
    
    def index2comp(self, index)
        return self.words[index]
    
