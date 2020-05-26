
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


'''
  Generate all the compostions using a prefix tree
'''
def ptree( word=[] , level=5 ):
    if level <= 0: return

    print(word)

    for k in range(level):
        word.append(k+1)
        tree( word , level - (k+1) )
        word.pop()
        
        
  # standarize basis
  '''
        nb = len(Basis)
        B = [ (sum(Basis[i]),Basis[i],i) for i in range(nb) ]
        B.sort()
        Signature = [ Signature[b[2]] for b in B[1:] ]
  '''


def aP(n):
    """Generate partitions of n as ordered lists in ascending
    lexicographical order.

    This highly efficient routine is based on the delightful
    work of Kelleher and O'Sullivan.

    Examples
    ========

    >>> for i in aP(6): i
    ...
    [1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 2]
    [1, 1, 1, 3]
    [1, 1, 2, 2]
    [1, 1, 4]
    [1, 2, 3]
    [1, 5]
    [2, 2, 2]
    [2, 4]
    [3, 3]
    [6]

    >>> for i in aP(0): i
    ...
    []

    References
    ==========

    .. [1] Generating Integer Partitions, [online],
        Available: http://jeromekelleher.net/generating-integer-partitions.html
    .. [2] Jerome Kelleher and Barry O'Sullivan, "Generating All
        Partitions: A Comparison Of Two Encodings", [online],
        Available: http://arxiv.org/pdf/0909.2331v2.pdf

    """
    #  The list `a`'s leading elements contain the partition in which
    #  y is the biggest element and x is either the same as y or the
    #  2nd largest element; v and w are adjacent element indices
    #  to which x and y are being assigned, respectively.
    a = [1]*n
    y = -1
    v = n
    while v > 0:
        v -= 1
        x = a[v] + 1
        while y >= 2 * x:
            a[v] = x
            y -= x
            v += 1
        w = v + 1
        while x <= y:
            a[v] = x
            a[w] = y
            yield a[:w + 1]
            x += 1
            y -= 1
        a[v] = x + y
        y = a[v] - 1
        yield a[:w]
