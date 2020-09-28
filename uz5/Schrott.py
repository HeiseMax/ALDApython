@staticmethod
    def _tree_remove(node, key):         # internal implementation
       if node == None:
            return None
        if key < node._key:
            node._left = _tree_remove( node._left,key)
        elif key > node._key:
            node._right = remove(node._right, key)
        else:
            if node._left == None and node._right == None:
                node = None
            elif node._left == None:
                node = node._right
            elif node._right == None:
                node = node._left
            else:
                prd = node
                prd = prd.left
                while prd._right is not None:
                    prd = prd._right
                    node._key = prd._key
                    node._left = _tree_remove(node._left, prd._key)
        return node

    if node == None:
            print("Key" + key + " does not exist!")
            raise KeyError('Key not existent')
        if key == node._key:
            print("hey")
            if node._left == None and node._right == None:
                print("hey")
                return None
            elif node._left == None and node._right != None:
                return node._right
            elif node._left != None and node._right == None:
                return node._left
            else:
                predecessor = node
                prdecessor = predecessor._left
                while predecessor._right != None:
                    predecessor = predecessor._right
                predecessor._left = node._left
                predecessor._right = node._right
                return predecessor
        elif key >= node._key:
            if node._right == None:
                print("Key " + key + " does not exist!")
                raise KeyError('Key not existent')
            else:
                tree = SearchTree()
                tree._root = node._right
                del tree[key]
        elif key <= node._key:
            if node._left == None:
                print("Key " + key + " does not exist!")
                raise KeyError('Key not existent')
            else:
                tree = SearchTree()
                tree._root = node._left
                del tree[key]


def __delitem__(self, key):  # implements 'del tree[key] '
    while True:
        if self._root == None:
            return None
        if key < self._root._key:
            self._root._left = _tree_remove(self._root._left, key)
        elif key > self._root._key:
            del self[key]
        else:
            if self._root._left == None and self._root._right == None:
                self._root = None
            elif self._root._left == None:
                node = self._root._right
            elif self._root._right == None:
                node = self._root._left
            else:
                prd = self._root
                prd = prd.left
                while prd._right is not None:
                    prd = prd._right
                    self._root._key = prd._key
                    self._root._left = _tree_remove(self._root._left, prd._key)
    # return node

    tree = SearchTree()
    tree._root = node2
    while True:
        node = tree._root
        if node == None:
            return None
        if key < node._key:
            tree._root = node._left
        elif key > node._key:
            tree._root = node._right
        else:
            if node._left == None and node._right == None:
                x = 50
                break
            elif node._left == None:
                x = 100
                break
            elif node._right == None:
                x = 200
                break
            else:
                x = 300
                break
    if x == 50:
        tree._root = None
    elif x == 75:
        node._left = None
    elif x == 100:
        node._right = node._right._right
    elif y == 100:
        node._left = node._left._right
    elif x == 200:
        node._right = node._right.left
    elif y == 200:
        node._left = node._left.left
    else:
        prd = node
        prd = prd.left
        while prd._right is not None:
            prd = prd._right
        node._key = prd._key
        node._value = node._value
        tree = SearchTree()
        tree._root = node._left