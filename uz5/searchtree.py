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
        
    def __getitem__(self, key):          # implements 'value = tree[key]'
        return self._tree_find(self._root, key)

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        global counter
        if self._root == None:
            self._root = self.Node(key, value)
            self._size += 1
        else:
            self._tree_insert(self._root, key, value)
            self._size += counter

    def __delitem__(self, key):          # implements 'del tree[key] '
        self._tree_remove(self._root, key)

    @staticmethod
    def _tree_find(node, key):           # internal implementation
        if node == None:
            print("Key" + str(key) + " does not exist!")
            raise KeyError('Key not existent')
        if key == node._key:
            return node._value
        elif key >= node._key:
            if node._right == None:
                print("Key " + str(key) + " does not exist!")
                raise KeyError('Key not existent')
            else:
                tree = SearchTree()
                tree._root = node._right
                return tree[key]
        elif key <= node._key:
            if node._left == None:
                print("Key " + str(key) + " does not exist!")
                raise KeyError('Key not existent')
            else:
                tree = SearchTree()
                tree._root = node._left
                return tree[key]

    @staticmethod
    def _tree_insert(node, key, value):  # internal implementation
        global counter
        counter = 0
        if key == node._key:
            node._value = value
        elif key >= node._key:
            if node._right == None:
                node._right = SearchTree.Node(key, value)
                counter += 1
            else:
                tree = SearchTree()
                tree._root = node._right
                tree[key] = value
        elif key <= node._key:
            if node._left == None:
                node._left = SearchTree.Node(key, value)
                counter += 1
            else:
                tree = SearchTree()
                tree._root = node._left
                tree[key] = value

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        if node == None:
            print("Key" + str(key) + " does not exist!")
            raise KeyError('Key not existent')
        if key == node._key:
            if node._left == None and node._right == None:
                node._value = None
                node._key = None
                node = None
            elif node._left == None and node._right != None:
                node._value = node._right._value
                node._key = node._right._key
                node._left = node._right._left
                node._right = node._right._right
            elif node._left != None and node._right == None:
                node._value = node._left._value
                node._key = node._left._key
                node._right = node._left._right
                node._left = node._left._left
            else:
                predecessor = node
                predecessor = predecessor._left
                while predecessor._right != None:
                    predecessor = predecessor._right
                node._value = predecessor._value
                node._key = predecessor._key
                predecessor = None
        elif key >= node._key:
            if node._right == None:
                print("Key " + str(key) + " does not exist!")
                raise KeyError('Key not existent')
            else:
                tree = SearchTree()
                tree._root = node._right
                del tree[key]
        elif key <= node._key:
            if node._left == None:
                print("Key " + str(key) + " does not exist!")
                raise KeyError('Key not existent')
            else:
                tree = SearchTree()
                tree._root = node._left
                del tree[key]

    def depth(self):
        depth = 0
        if self._root == None:
            return -1
        else:
            tree = SearchTree()
            tree._root = self._root._left
            depth_left = tree.depth()
            tree._root = self._root._right
            depth_right = tree.depth()
            if depth_left <= depth_right:
                depth = depth_right
            else:
                depth = depth_left
            depth += 1
            return depth

counter = 0

def test_search_tree():
    t = SearchTree()
    assert len(t) == 0
    for i in range (8): #Baum in Form einer Kette
        t[i] = i
    for i in range (8):
        assert t[i] == i
    t[2] = 10
    assert t[2] == 10
    assert t.__len__() == 8
    assert t.depth() == 7 #Test für Algorithmus aus b)
    del t[2]
    with pytest.raises(KeyError):
        assert t[2] == 10
    del t[1]
    with pytest.raises(KeyError):
        assert t[1] == 1

    tr = SearchTree()
    order = [4,2,1,3,6,5,7]
    for i in (order): #Balancierter Baum mit 4 als Wurzel
        tr[i] = i
    for i in (order):
        assert tr[i] == i
    tr[4] = 10
    assert tr[4] == 10
    with pytest.raises(KeyError):
        assert tr[10] == 10
    assert tr.__len__() == 7
    assert tr.depth() == 2 #Test für Algorithmus aus b)
    del tr[2]
    with pytest.raises(KeyError):
        assert tr[2] == 1
    del tr[4]
    with pytest.raises(KeyError):
        assert tr[4] == 1
    with pytest.raises(KeyError):
        del tr[19]


'''
Aufgabe 1 c): Wenn ich die Schlüssel in einem sortierten Array habe, mache ich den Schlüssel in der Mitte zur Wurzel
                und sortiere die Hälfte mit den kleineren Werten in den linken Teilbaum
                und die Hälfte mit den größeren Werten in den rechten Teilbaum.
                So weiter iterativ fortfahren.
        1 d): Die Reihenfolge des Löschens ist egal. Leider kein Beweis ;C
'''