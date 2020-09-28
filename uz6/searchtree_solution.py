import pytest

class SearchTree:
    class Node:
        def __init__(self, key, value):
            self._key = key
            self._value = value
            self._left = self._right = None

    def __init__(self):
        self._root = None
        self._size = 0
        
    def __len__(self):
        return self._size
        
    def __getitem__(self, key):
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            raise KeyError(key)
        return node._value
        
    def __setitem__(self, key, value):
        self._root, key_is_new = SearchTree._tree_insert(self._root, key, value)
        if key_is_new:
            self._size += 1
        
    def __delitem__(self, key):
        self._root = SearchTree._tree_remove(self._root, key)
        self._size -= 1
    
    @staticmethod
    def _tree_find(node, key):
        if node is None:
            return None
        if key == node._key:
            return node
        if key < node._key:
            return SearchTree._tree_find(node._left, key)
        else:
            return SearchTree._tree_find(node._right, key)
    
    @staticmethod
    def _tree_insert(node, key, value):
        if node is None:
            node = SearchTree.Node(key, value)
            key_is_new = True
        elif key == node._key:
            node._value = value
            key_is_new = False
        elif key < node._key:
            node._left, key_is_new = SearchTree._tree_insert(node._left, key, value)
        else:
            node._right, key_is_new = SearchTree._tree_insert(node._right, key, value)
        return node, key_is_new
    
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
            node._left = SearchTree._tree_remove(node._left, key)
        elif key > node._key:
            node._right = SearchTree._tree_remove(node._right, key)
        else: 
            if node._left is None and node._right is None: 
                node = None            
            elif node._left is None: 
                node = node._right 
            elif node._right is None: 
                node = node._left
            else:
                pred = SearchTree._tree_predecessor(node)
                node._key = pred._key
                node._value = pred._value
                node._left = SearchTree._tree_remove(node._left, pred._key)
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


# Note: To test all possible cases of _tree_remove(), we
# need to understand how this functions works. Thus, although the
# assertions themselves are black-box tests (i.e. use only the public
# interface of SearchTree), the _selection of the test data_ 
# is based on the gray-box paradigm.
def test_search_tree():
    t = SearchTree()
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
        
    t = SearchTree()
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
    
def test_depth():
    t1 = SearchTree()
    
    with pytest.raises(RuntimeError):
        t1.depth()
    
    t1[1] = 10
    assert t1.depth() == 0
    
    t1[2] = 20
    t1[3] = 30
    assert t1.depth() == 2
    
    t2 = SearchTree()
    t2[6] = 60
    t2[3] = 30
    t2[1] = 10
    t2[4] = 42
    t2[8] = 8
    assert t2.depth() == 2
    