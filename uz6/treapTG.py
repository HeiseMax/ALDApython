import pytest
from random import randint

class TreapBase:
    class Node:
        def __init__(self, key, value, priority):
            self._key = key
            self._value = value
            self._left = self._right = None
            self._priority = priority
        

    def __init__(self):
        self._root = None
        self._size = 0
        self.is_dynamic_treap = -1
        
    def __len__(self):
        return self._size
        
    def __getitem__(self, key):
        flag = self.is_dynamic_treap
        node = TreapBase._tree_find(self._root, key, flag)
        if node is None:
            raise KeyError(key)
        return node._value
        
    def __setitem__(self, key, value):
        flag = self.is_dynamic_treap
        self._root, key_is_new = TreapBase._tree_insert(self._root, key, value, flag)
        if key_is_new:
            self._size += 1
        
    def __delitem__(self, key):
        self._root = TreapBase._tree_remove(self._root, key)
        self._size -= 1
    
    @staticmethod
    def _tree_find(node, key, flag):
        if node is None:
            return None
        if key == node._key:
            if flag == 0:
                node._priority += 1
            return node
        if key < node._key:
            return TreapBase._tree_find(node._left, key, flag)
        else:
            return TreapBase._tree_find(node._right, key, flag)
    
    @staticmethod
    def _tree_insert(node, key, value, flag):
        if node is None:
            if flag == 1: 
                node = TreapBase.Node(key, value, randint(0,1000))
            if flag == 0:
                node = TreapBase.Node(key, value, 1)
            key_is_new = True
        elif key == node._key:
            node._value = value
            if flag == 0:
                node._priority += 1
            key_is_new = False

        elif key < node._key:
            node._left, key_is_new = TreapBase._tree_insert(node._left, key, value, flag)
        else:
            node._right, key_is_new = TreapBase._tree_insert(node._right, key, value, flag)

        if node._priority < node._left._priority:
            node = TreapBase._tree_rotate_right(node)
        if node._priority < node._right._priority:
            node = TreapBase._tree_rotate_left(node)

        return node, key_is_new

    @staticmethod
    def _restructure_priority_backwards(node):
        if node._priority < node._left._priority:
            node = TreapBase._tree_rotate_right(node)
        if node._priority < node._right._priority:
            node = TreapBase._tree_rotate_left(node) 
        TreapBase._restructure_priority_backwards(node._left)
        TreapBase._restructure_priority_backwards(node._right)

        return node
    
    @staticmethod
    def _tree_predecessor(node):
        node = node._left
        while node._right is not None:
            node = node._right
        return node
        
    @staticmethod
    def _tree_remove(node, key):
        if node is None:
            raise KeyError(key)
        if key < node._key: 
            node._left = TreapBase._tree_remove(node._left, key)
        elif key > node._key:
            node._right = TreapBase._tree_remove(node._right, key)
        else:                                                       
            if node._left is None and node._right is None: 
                node = None            
            elif node._left is None: 
                node = node._right 
            elif node._right is None: 
                node = node._left
            else:                                          #Nur hier kann sich die Prioritätsrangfolge verändern
                pred = TreapBase._tree_predecessor(node)
                node._key = pred._key
                node._value = pred._value
                node._left = TreapBase._tree_remove(node._left, pred._key)
                node._priority = pred._priority 
                
                node = TreapBase._restructure_priority_backwards(node)

        return node
        

    
    def depth(self):
        """
        Gibt die Tiefe des Baumens (d.h. Abstand Wurzel z. tiefsten Blatt) aus
        """
    
        def _depth(rootnode):
            """
            Hilfsfunktion fuer depth: die Tiefe des aktuellen 'rootnode'
            ist um eins groesser als die Tiefe seines groessten Unterbaums.
            """
            if rootnode is None:
                return 0
            return max(_depth(rootnode._left), _depth(rootnode._right)) + 1
    
        if self._root is None:
            raise RuntimeError("depth(): tree is empty.")
        
        result = _depth(self._root)
        
        # eins abziehen, da wir die Kanten zaehlen und nicht die Knoten
        return result - 1

    @staticmethod
    def _tree_rotate_right(old_root):
        new_root = old_root._left
        old_root._left = new_root._right
        new_root._right = old_root
        return new_root

    @staticmethod
    def _tree_rotate_left(old_root):
        new_root = old_root._right
        old_root._right = new_root._left
        new_root._left = old_root
        return new_root


# Note: To test all possible cases of _tree_remove(), we
# need to understand how this functions works. Thus, although the
# assertions themselves are black-box tests (i.e. use only the public
# interface of SearchTree), the _selection of the test data_ 
# is based on the gray-box paradigm.
def test_search_tree():
    t = TreapBase()
    assert len(t) == 0
    
    t[1] = 1
    assert len(t) == 1
    assert t[1] == 1
    with pytest.raises(KeyError):
        v = t[2]
    
    t[0] = 0
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 1
    
    t[1] = 11                # overwrite value of existing key
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    
    t[2] = 2
    assert len(t) == 3
    assert t[0] == 0
    assert t[1] == 11
    assert t[2] == 2
    
    del t[2]                 # delete leaf
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    with pytest.raises(KeyError):
        v = t[2]
        
    del t[1]                 # replace node with left child
    assert len(t) == 1
    assert t[0] == 0
    with pytest.raises(KeyError):
        v = t[1]

    with pytest.raises(KeyError):
        del t[1]             # delete invalid key
        
    t = TreapBase()
    t[0]=0
    t[3]=3
    t[1]=1
    t[2]=2
    t[4]=4
    assert len(t) == 5
    for k in [0, 1, 2, 3, 4]:
        assert t[k] == k
        
    del t[3]                 # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[3]
    assert len(t) == 4
    for k in [0, 1, 2, 4]:
        assert t[k] == k
        
    del t[2]                 # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[2]
    assert len(t) == 3
    for k in [0, 1, 4]:
        assert t[k] == k
        
    del t[1]                 # replace node with right child
    with pytest.raises(KeyError):
        v = t[1]
    assert len(t) == 2
    for k in [0, 4]:
        assert t[k] == k
        
    del t[4]                 # remove leaf
    with pytest.raises(KeyError):
        v = t[4]
    assert len(t) == 1
    assert t[0] == 0
        
    del t[0]                 # remove leaf
    with pytest.raises(KeyError):
        v = t[0]
    assert len(t) == 0

    r = RandomTreap()
    r[0] = 1
    r[1] = 4
    r[2] = 5

    root = r._root
    lchild = root._left
    rchild = root._right
    assert root._priority > lchild._priority
    assert root._priority > rchild._priority
    assert root._key > lchild._key
    assert root._key < lchild._key

    r[4] = 5
    r[3] = 6
    r[5] = 5
    r[6] = 6

    del r[1]
    root = r._root
    lchild = root._left
    rchild = root._right
    assert root._priority > lchild._priority
    assert root._priority > rchild._priority
    assert root._key > lchild._key
    assert root._key < lchild._key


    d = DynamicTreap()
    d[0] = 1
    d[1] = 4
    d[2] = 5

    root = d._root
    lchild = root._left
    rchild = root._right
    assert root._priority > lchild._priority
    assert root._priority > rchild._priority
    assert root._key > lchild._key
    assert root._key < lchild._key

    d[1] = 5

    root = d._root
    lchild = root._left
    rchild = root._right
    assert root._priority > lchild._priority
    assert root._priority > rchild._priority
    assert root._key > lchild._key
    assert root._key < lchild._key

    v= d[2]
    v= d[2]

    root = d._root
    lchild = root._left
    rchild = root._right
    assert root._priority > lchild._priority
    assert root._priority > rchild._priority
    assert root._key > lchild._key
    assert root._key < lchild._key

    d[4] = 5
    d[3] = 6
    d[5] = 5
    d[6] = 6 

    del d[1]
    root = d._root
    lchild = root._left
    rchild = root._right
    assert root._priority > lchild._priority
    assert root._priority > rchild._priority
    assert root._key > lchild._key
    assert root._key < lchild._key



    
def test_depth():
    t1 = TreapBase()
    
    with pytest.raises(RuntimeError):
        t1.depth()
    
    t1[1] = 10
    assert t1.depth() == 0
    
    t1[2] = 20
    t1[3] = 30
    assert t1.depth() == 2
    
    t2 = TreapBase()
    t2[6] = 60
    t2[3] = 30
    t2[1] = 10
    t2[4] = 42
    t2[8] = 8
    assert t2.depth() == 2


class RandomTreap (TreapBase):
    def __init__(self):
        self._root = None
        self._size = 0
        self.is_dynamic_treap = 1

class DynamicTreap (TreapBase):
    def __init__(self):
        self._root = None
        self._size = 0
        self.is_dynamic_treap = 0

    @staticmethod
    def top_impl (root, a, min_priority):
        if root != None:
            if root._priority >= min_priority:
                a.append([root._key,root._priority])
            DynamicTreap.top_impl(root._l, a, min_priority)
            DynamicTreap.top_impl(root._l, a, min_priority)
        return a


    def top(self, min_priority):
        root = self._root
        a = []
        x = DynamicTreap.top_impl (root, a, min_priority)
        return x


# File einlesen und nach Unicode konvertieren (damit Umlaute korrekt sind)
s = open("helmholtz-naturwissenschaften.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
        s = s.replace(k, '') # Sonderzeichen entfernen
s = s.lower() # Alles klein schreiben
text = s.split() # String in Array von Wörtern umwandeln
#Die Wörter in text werden nun in die beiden Treaps eingefügt:
rt = RandomTreap()
dt = DynamicTreap()
for word in text:
    rt[word] = None # die values werden in dieser Übung nicht benötigt
    dt[word] = None # alternativ können die values als Zähler dienen

def compare_trees_impl(root1, root2):
    if root1 != None and root2 != None:
        if root1._value != root2._value:
            return False
        compare_trees_impl(root1._l, root2._l)
        compare_trees_impl(root1._r, root2._r)

    return True

def compare_trees(tree1, tree2):
    root1 = tree1._root
    root2 = tree2._root
    x = compare_trees_impl(root1, root2)
    return x

print (compare_trees(rt, dt))
print(rt._size)
#Ein perfekt balancierter Baum hätte Tiefe log(rt._size)= ?
print(rt.depth)
print(dt.depth)

def middepth_impl(root, sum, k):
    k += 1
    if root == None:
        return sum
    else:
        sum += k
        middepth_impl(root._l, sum, k)
        middepth_impl(root._r, sum, k)

def middepth(tree):
    root = tree.root
    x = middepth_impl(root,0, 0)
    md = x/tree.depth
    return md

print(middepth(rt))
print(middepth(dt))

def midaccess_impl(root, sum, k):
    k += 1
    if root == None:
        return sum
    else:
        sum += k*root._priority
        midaccess_impl(root._l, sum, k)
        midaccess_impl(root._r, sum, k)

def midaccess(tree):
    root = tree._root
    x = midaccess_impl(root,0, 0)
    ma= x/tree.depth
    return ma

print(midaccess(rt))
print(midaccess(dt))

print (dt.top(30))

s = open("stopwords.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
        s = s.replace(k, '') # Sonderzeichen entfernen
s = s.lower() # Alles klein schreiben
text = s.split() # String in Array von Wörtern umwandeln
#Die Wörter in text werden nun in die beiden Treaps eingefügt:
y = set()
for word in text:
    set.add(word)

s = open("helmholtz-naturwissenschaften.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
        s = s.replace(k, '') # Sonderzeichen entfernen
s = s.lower() # Alles klein schreiben
text = s.split() # String in Array von Wörtern umwandeln
#Die Wörter in text werden nun in die beiden Treaps eingefügt:
cleaned_treap = DynamicTreap()
for word in text:
    x = set(word)
    if y.isdisjoint(x) == False:
        cleaned_treap[word]

print (cleaned_treap.top(20))