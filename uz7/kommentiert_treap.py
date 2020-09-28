import pytest
import random

#comment: In der Abgabe war noch die Implementation von Searchtree vorhanden.

class TreapBase:
    is_dynamic_treap = bool
    class Node:
        def __init__(self, key, value, priority):
            self._key = key
            self._value = value
            self._left = self._right = None
            self._priority = priority

    def __init__(self):
        self._root = None
        self._size = 1

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        node = TreapBase._tree_find(self._root, key, self.is_dynamic_treap)
        if node is None:
            raise KeyError(key)
        if self._root._left is not None and (self._root._priority < self._root._left._priority):
                self._root = TreapBase._tree_rotate_right(self._root)
        if self._root._right is not None and (self._root._priority < self._root._right._priority):
                self._root = TreapBase._tree_rotate_left(self._root)
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
            if flag == True:
                node._priority += 1
            return node
        if key < node._key:
            node = TreapBase._tree_find(node._left, key, flag)
            if node is not None and node._left is not None and (node._priority < node._left._priority):
               node = TreapBase._tree_rotate_right(node)
            return node

        else:
            node = TreapBase._tree_find(node._right, key, flag)
            if node is not None and node._right is not None and (node._priority < node._right._priority):
               node = TreapBase._tree_rotate_left(node)
            return node

    @staticmethod
    def _tree_insert(node, key, value, flag):
        if node is None:
            if (flag == False):
                priority = random.randint(1,1000)
                node = TreapBase.Node(key, value, priority)
            else:
                node = TreapBase.Node(key, value, 1)
            key_is_new = True
        elif key == node._key:
            node._value = value
            if (flag == True):
                node._priority += 1
            key_is_new = False
        elif key < node._key:
            node._left, key_is_new = TreapBase._tree_insert(node._left, key, value, flag)
            if node._priority < node._left._priority:
               node = TreapBase._tree_rotate_right(node)
        else:
            node._right, key_is_new = TreapBase._tree_insert(node._right, key, value, flag)
            if node._priority < node._right._priority:
               node = TreapBase._tree_rotate_left(node)
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
            else:
                pred = TreapBase._tree_predecessor(node)
                node._key = pred._key
                node._value = pred._value
                node._left = TreapBase._tree_remove(node._left, pred._key)
                while node._left is not None:
                    if node._priority < node._left._priority:
                        node = TreapBase._tree_rotate_right(node)
                    else:
                        break
                while node._right is not None:
                    if node._priority < node._right._priority:
                        node = TreapBase._tree_rotate_left(node)
                    else:
                        break
        return node

    @staticmethod
    def _tree_rotate_left(node):
        new_root = node._right
        node._right = new_root._left
        new_root._left = node
        return new_root

    @staticmethod
    def _tree_rotate_right(node):
        new_root = node._left
        node._left = new_root._right
        new_root._right = node
        return new_root

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

    def rotate_right(self):
        TreapBase()._tree_rotate_right(self._root)

    def rotate_left(self):
        TreapBase()._tree_rotate_left(self._root)

class RandomTreap(TreapBase):
    def __init__(self):
        self._root = None
        self._size = 0
        self.is_dynamic_treap = False

class DynamicTreap(TreapBase):
    def __init__(self):
        self._root = None
        self._size = 0
        self.is_dynamic_treap = True

    @staticmethod
    def top_impl (root, min_priority):
        if root == None:
            return None
        elif root._priority < min_priority:
            return None
        else:
            left = DynamicTreap.top_impl(root._left, min_priority)
            right = DynamicTreap.top_impl(root._right, min_priority)
            a = []
            if left is not None:
                a = a + left
            if right is not None:
                a = a + right
            a.append((root._key, root._priority))
            return a

    def top(self, min_priority):
        root = self._root
        x = DynamicTreap.top_impl (root, min_priority)
        x.sort(reverse = True, key = lambda x: x[1])
        return x

# tests basic functions DynamicTreap
def test_Dynamic_treap():
    t = DynamicTreap()
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

    t[1] = 11  # overwrite value of existing key
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11

    t[2] = 2
    assert len(t) == 3
    assert t[0] == 0
    assert t[1] == 11
    assert t[2] == 2

    del t[2]  # delete leaf
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    with pytest.raises(KeyError):
        v = t[2]

    del t[1]  # replace node with left child
    assert len(t) == 1
    assert t[0] == 0
    with pytest.raises(KeyError):
        v = t[1]

    with pytest.raises(KeyError):
        del t[1]  # delete invalid key

    t = DynamicTreap()
    t[0] = 0
    t[3] = 3
    t[1] = 1
    t[2] = 2
    t[4] = 4
    assert len(t) == 5
    for k in [0, 1, 2, 3, 4]:
        assert t[k] == k

    del t[3]  # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[3]
    assert len(t) == 4
    for k in [0, 1, 2, 4]:
        assert t[k] == k

    del t[2]  # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[2]
    assert len(t) == 3
    for k in [0, 1, 4]:
        assert t[k] == k

    del t[1]  # replace node with right child
    with pytest.raises(KeyError):
        v = t[1]
    assert len(t) == 2
    for k in [0, 4]:
        assert t[k] == k

    del t[4]  # remove leaf
    with pytest.raises(KeyError):
        v = t[4]
    assert len(t) == 1
    assert t[0] == 0

    del t[0]  # remove leaf
    with pytest.raises(KeyError):
        v = t[0]
    assert len(t) == 0
    assert check_condition2(t._root)
    assert check_condition1(t._root)

# tests basic functions RandomTreap
def test_Random_treap():
    t = RandomTreap()
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

    t[1] = 11  # overwrite value of existing key
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11

    t[2] = 2
    assert len(t) == 3
    assert t[0] == 0
    assert t[1] == 11
    assert t[2] == 2

    del t[2]  # delete leaf
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    with pytest.raises(KeyError):
        v = t[2]

    del t[1]  # replace node with left child
    assert len(t) == 1
    assert t[0] == 0
    with pytest.raises(KeyError):
        v = t[1]

    with pytest.raises(KeyError):
        del t[1]  # delete invalid key

    t = RandomTreap()
    t[0] = 0
    t[3] = 3
    t[1] = 1
    t[2] = 2
    t[4] = 4
    assert len(t) == 5
    for k in [0, 1, 2, 3, 4]:
        assert t[k] == k

    del t[3]  # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[3]
    assert len(t) == 4
    for k in [0, 1, 2, 4]:
        assert t[k] == k

    del t[2]  # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[2]
    assert len(t) == 3
    for k in [0, 1, 4]:
        assert t[k] == k

    del t[1]  # replace node with right child
    with pytest.raises(KeyError):
        v = t[1]
    assert len(t) == 2
    for k in [0, 4]:
        assert t[k] == k

    del t[4]  # remove leaf
    with pytest.raises(KeyError):
        v = t[4]
    assert len(t) == 1
    assert t[0] == 0

    del t[0]  # remove leaf
    with pytest.raises(KeyError):
        v = t[0]
    assert len(t) == 0
    assert check_condition2(t._root)
    assert check_condition1(t._root)

#method to check for keySorting
def check_condition1(node):
    if node == None:
        return True
    else:
        if check_condition1(node._right) == check_condition1(node._left) == True:
            if (node._left is not None and  node._right is not None):
                if (node._key > node._left._key and node._key < node._right._key):
                    return True
                else:
                    return False
            elif (node._left is not None):
                if (node._key > node._left._key):
                    return True
                else:
                    return False
            elif (node._right is not None):
                if (node._key < node._right._key):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

#method to check for PrioritySorting
def check_condition2(node):
    if node == None:
        return True
    else:
        if check_condition1(node._right) == check_condition1(node._left) == True:
            if (node._left is not None and node._right is not None):
                if (node._priority >= node._left._priority and node._priority >= node._right._priority):
                    return True
                else:
                    return False
            elif (node._left is not None):
                if (node._priority >= node._left._priority):
                    return True
                else:
                    return False
            elif (node._right is not None):
                if (node._priority >= node._right._priority):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

def test_conditions():
    t1 = DynamicTreap()
    t1[1] = 10
    t1[2] = 20
    t1[3] = 30
    t1[6] = 60
    t1[4] = 42
    t1[8] = 8
    t1[1] = 10
    t1[2] = 20
    t1[3] = 30
    t1[6] = 60
    t1[4] = 42
    t1[8] = 8
    t1[3] = 30
    t1[6] = 20
    k = t1[3]
    k = t1[3]
    k = t1[6]
    k = t1[6]
    k = t1[6]
    del t1[3]
    del t1[8]
    assert check_treap_find(t1._root, 6) == 6
    assert check_condition1(t1._root)
    assert check_condition2(t1._root)

    t2 = RandomTreap()
    t2[1] = 10
    t2[2] = 20
    t2[3] = 30
    t2[6] = 60
    t2[4] = 42
    t2[8] = 8
    t2[1] = 10
    t2[2] = 20
    t2[3] = 30
    t2[6] = 60
    t2[4] = 42
    t2[8] = 8
    t2[3] = 30
    k = t2[6]
    k = t2[6]
    k = t2[6]
    del t2[3]
    del t2[8]
    assert check_condition1(t1._root)
    assert check_condition2(t1._root)

#returns the Priority of given key in DynamicTreap
def check_treap_find(node, key):
    found = DynamicTreap._tree_find(node,key, False)
    return found._priority

def test_treap_find():
    t1 = DynamicTreap()
    t1[1] = 10
    t1[2] = 20
    t1[3] = 30
    t1[6] = 60
    t1[4] = 42
    t1[8] = 8
    k = t1[4]
    k = t1[4]
    k = t1[4]
    assert check_treap_find(t1._root, 4) == 4

def compare_trees(tree1, tree2):
    return compare_trees_impl(tree1._root, tree2._root)

def compare_trees_impl(root1, root2):
    if root1 == root2 == None:
        return True
    elif root1 == None:
        return False
    elif root2 == None:
        return False
    elif compare_trees_impl(root1._left, root2._left) and compare_trees_impl(root1._right, root2._right):
        if (root1 == root2):
            return True
        else:
            return False
    else:
        return False

def test_compare_trees():
    t1 = DynamicTreap()
    t1[1] = 10
    t1[2] = 20
    t1[3] = 30
    t1[6] = 60
    t1[4] = 42
    t1[8] = 8
    t1[1] = 10
    assert compare_trees(t1,t1)

    t2 = RandomTreap()
    t2[1] = 10
    t2[2] = 20
    t2[3] = 30
    t2[6] = 60
    t2[4] = 42
    t2[8] = 8
    t2[1] = 10
    t2[9] = 9
    assert compare_trees(t2,t2)
    with pytest.raises(AssertionError):
        assert compare_trees(t1,t2)

# File einlesen und nach Unicode konvertieren (damit Umlaute korrekt sind)
s = open("helmholtz-naturwissenschaften.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
        s = s.replace(k, '') # Sonderzeichen entfernen
s = s.lower() # Alles klein schreiben
text = s.split() # String in Array von Wörtern umwandeln
#Die Wörter in text werden nun in die beiden Treaps eingefügt:
rt = RandomTreap()
dt = DynamicTreap()
wordCount = 0
for word in text:
    wordCount +=1 #comment: Counter um Gesamtanzahl der Woerterr zu zaehlen
    rt[word] = 0
    dt[word] = 0

for word in text:
    rt[word] += 1 # values = Anzahl des Wortes

print ("")
print ("Aufgabe 1 f)")
print ("Der Text 'Helmholtz-Naturwissenschaften' enthält " + str(rt.__len__()) + " verschiedene Wörter.")
print("Eine perfekt balancierter Baum hätte die Tiefe T >= log2(2627) = 11.359 ==> also Tiefe = 12.")
print("Die Tiefe des DynamischenTreaps ist " + str(TreapBase.depth(dt)) + ".")
print("Die Tiefe des RandomTreaps ist dieses Mal " + str(TreapBase.depth(rt)) + ", variiert allerdings.")


def middepth_impl(root, k):
    if root == None:
        return 0
    else:
        sum_left = middepth_impl(root._left, k +1)
        sum_right = middepth_impl(root._right, k +1)
        sum = sum_right + sum_left + k
        return sum

def middepth(tree):
    root = tree._root
    x = middepth_impl(root,0)
    md = x/int((rt.__len__())) #comment: hier muss die Anzahl der verschiedenen Woerter benutzt werden
    return md

print("Die mittlere Tiefe des DynamicTreaps ist " + str(middepth(dt)) + ".")
print("Die mittlere Tiefe des RandomTreaps ist dieses Mal " + str(middepth(rt)) + ", variiert allerdings.")

def midaccess_impl(root, k, len, flag):
    if root == None:
        return 0
    else:
        sum_left = midaccess_impl(root._left, k + 1,len, flag) #comment: In der Abgabe wurde die middepth_impl(root, k) benutzt
        sum_right = midaccess_impl(root._right, k + 1,len, flag)
        if flag == True:
            Nw = root._priority
        else:
            Nw = root._value
        sum = sum_right + sum_left + ((Nw/len) * k)
        return sum

def midaccess(tree):
    root = tree._root
    len = wordCount #comment: hier wird die Gesamtzahl der Woerter benutzt
    flag = tree.is_dynamic_treap
    x = midaccess_impl(root,0, len, flag)
    return x

print("Die mittlere Zugriffszeit des DynamicTreaps ist " + str(midaccess(dt)) + ".")
print("Die mittlere Zugriffszeit des RandomTreaps ist dieses Mal " + str(midaccess(rt)) + ", variiert allerdings.")
print("Die mittlere Tiefe ist bei RandomTreap im Durchschnitt kleiner und die mittlere Zugriffszeit im Durchschnitt länger.")
#comment: hier war die Aussage in der Abgabe falsch, da in der midaccess funktion die falsche Implementation verwendet wurde

print ("")
print ("Aufgabe 1 g)")
print ("Die meist benutzten Woerter sind:")
a = dt.top(11)
j = 1
for i,x in (a):
    print (j, ".:",i,":",x)
    j += 1



s = open("stopwords.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
        s = s.replace(k, '') # Sonderzeichen entfernen
s = s.lower() # Alles klein schreiben
stopwords = s.split() # String in Array von Wörtern umwandeln

cleaned_treap = DynamicTreap()
cleaned_text = [x for x in text if x not in stopwords]
for word in cleaned_text:
   cleaned_treap[word] = None

print ("")
print ("Die meist benutzten Woerter in der 'cleaned' Version sind:")
a = cleaned_treap.top(11)
j = 1
for i,x in (a):
    print (j, ".:",i,":",x)
    j += 1

print ("")
print ("Die Woerter lassen nun definitiv auf eine Wissenschaftliche Arbeit schliessen")
print ("")
print ("Die schriftlichen Lösungen für Aufgabe f), g) sind oben in der Ausgabe")