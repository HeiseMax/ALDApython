import pytest
import math
import random


class TreapBase:
    class Node:
        def __init__(self, key, value, priority):
            self._key = key
            self._value = value
            self._priority = priority
            self._left = self._right = None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        node = TreapBase._tree_find(self._root, key, self.is_dynamic_treap)
        if node is None:
            raise KeyError(key)
        return node._value

    def __setitem__(self, key, value):
        self._root, key_is_new = TreapBase._tree_insert(
            self._root, key, value, self.is_dynamic_treap
        )
        if key_is_new:
            self._size += 1

    def __delitem__(self, key):
        self._root = TreapBase._tree_remove(self._root, key)
        self._size -= 1

    @staticmethod
    def _tree_find(node, key, is_dynamic_treap):
        if node is None:
            return None
        if key == node._key:
            if is_dynamic_treap:  # DynamicTreap, Zugriff erhöht Priorität um 1
                node._priority += 1
            return node
        if key < node._key:
            # erst Node finden und dabei evtl. die Priorität erhöhen
            found = TreapBase._tree_find(node._left, key, is_dynamic_treap)
            # dann heap-Bedingung überprüfen und ggf. reparieren
            if found is not None and found._priority > node._priority:  
                found = TreapBase._tree_rotate_right(node)
            return found
        else:
            # dito für rechtes Kind
            found = TreapBase._tree_find(node._right, key, is_dynamic_treap)
            if found is not None and found._priority > node._priority:  
                found = TreapBase._tree_rotate_left(node)
            return found


    @staticmethod
    def _tree_insert(node, key, value, is_dynamic_treap):
        if node is None:
            if is_dynamic_treap:
                priority = 1
            else:
                priority = random.randint(0, 4294967295)
            node = TreapBase.Node(key, value, priority)
            key_is_new = True
        elif key == node._key:
            if is_dynamic_treap:             # dynamic Treap modus
                node._priority += 1          # => Prioritaet inkrementieren
            node._value = value
            key_is_new = False
        elif key < node._key:
            node._left, key_is_new = TreapBase._tree_insert(
                node._left, key, value, is_dynamic_treap
            )
            if node._left._priority > node._priority:
                node = TreapBase._tree_rotate_right(node)
        else:
            node._right, key_is_new = TreapBase._tree_insert(
                node._right, key, value, is_dynamic_treap
            )
            if node._right._priority > node._priority:
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
                node._priority = pred._priority
                node._left = TreapBase._tree_remove(node._left, pred._key)

                if node._left._priority > node._priority:
                    node = TreapBase._tree_rotate_right(node)
        return node

    @staticmethod
    def _tree_rotate_left(root):
        if root._right is None:
            raise RuntimeError('Root does not have right child')
        new_root = root._right
        root._right = new_root._left
        new_root._left = root
        return new_root

    @staticmethod
    def _tree_rotate_right(root):
        if root._left is None:
            raise RuntimeError('Root does not have left child')
        new_root = root._left
        root._left = new_root._right
        new_root._right = root
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



class RandomTreap(TreapBase):
    def __init__(self):
        super(RandomTreap, self).__init__()
        self.is_dynamic_treap = False


class DynamicTreap(TreapBase):
    def __init__(self):
        super(DynamicTreap, self).__init__()
        self.is_dynamic_treap = True

    def top(self, min_priority):

        def _top(rootnode, array, min_priority):
            if rootnode is None or rootnode._priority < min_priority:
                return

            array.append((rootnode._key, rootnode._priority))

            _top(rootnode._left, array, min_priority)
            _top(rootnode._right, array, min_priority)

        top_nodes = []
        _top(self._root, top_nodes, min_priority)

        # nach absteigender Priorität sortieren
        return list(reversed(sorted(top_nodes, key=lambda x: x[1])))


@pytest.mark.parametrize("t", [RandomTreap(), DynamicTreap()])
def test_treap(t):
    assert len(t) == 0

    # Einfaches Einfügen

    t[1] = 10
    assert len(t) == 1
    assert t[1] == 10
    with pytest.raises(KeyError):
        _ = t[2]

    if t.is_dynamic_treap:
        assert t._root._priority == 2  # 1. Zugriff bei insert, zweiter Zugriff bei Überprüfung des Werts der Node

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    t[2] = 20
    assert len(t) == 2
    assert t[2] == 20

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    t[3] = 30
    assert len(t) == 3
    assert t[3] == 30

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    # Zugriff und Überschreiben eines Werts

    t[1] = 11
    assert len(t) == 3
    assert t[1] == 11
    if t.is_dynamic_treap:
        assert t._root._priority == 4

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    # Einfügen nach Überschreiben

    t[0] = 0
    assert len(t) == 4
    assert t[0] == 0
    if t.is_dynamic_treap:
        assert t._root._priority == 4

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    # Mehrfacher Zugriff mit Überschreiben

    for i in range(10):
        t[2] = i
    assert len(t) == 4
    assert t[2] == 9
    if t.is_dynamic_treap:
        assert t._root._priority == 13

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    for i in range(10):
        t[0] = i
    assert len(t) == 4
    assert t[0] == 9
    if t.is_dynamic_treap:
        assert t._root._priority == 13

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)

    # Löschen

    del t[2]
    assert len(t) == 3
    assert t[0] == 9
    assert t[1] == 11
    assert t[3] == 30
    with pytest.raises(KeyError):
        _ = t[2]
    if t.is_dynamic_treap:
        assert t._root._priority == 14

    _check_key_sorted(t._root)
    _check_priority_sorted(t._root)


def _check_key_sorted(node):
    if node._left is not None:
        _check_key_sorted(node._left)
        assert node._key > node._left._key

    if node._right is not None:
        _check_key_sorted(node._right)
        assert node._key < node._right._key


def _check_priority_sorted(node):
    if node._left is not None:
        _check_priority_sorted(node._left)
        assert node._priority >= node._left._priority

    if node._right is not None:
        _check_priority_sorted(node._right)
        assert node._priority >= node._right._priority


def mean_depth(t):
    """
    Gibt die mittlere Tiefe des Baums aus
    """

    def _sum_depths(node, depth):
        """
        Hilfsfunktion für mean_depth: berechne die Summe aller Tiefen.
        Der Wurzel jedes Unterbaums hat eine um eins größere Tiefe.
        """
        if node is None:
            return 0

        return depth + _sum_depths(node._left, depth + 1) + \
               _sum_depths(node._right, depth + 1)

    if t._root is None:
        raise RuntimeError("mean_depth(): tree is empty.")

    sum = _sum_depths(t._root, 0)  # root ist bei Tiefe 0

    return sum/len(t)   # Mittelwert


def priorities(t, N):
    """
    Gibt eine Liste der Zugriffshäufigkeiten aus
    """

    def _priorities(rootnode, array):
        '''
        Hilfsfunktion: Sammle alle Prioritäten in 'array'.
        '''
        if rootnode is None:
            return

        array.append(rootnode._priority / N)

        _priorities(rootnode._left, array)
        _priorities(rootnode._right, array)

    priorities = []
    _priorities(t._root, priorities)

    return priorities


def mean_access_time(t, relative_priorities):
    """
    Gibt die mittlere Zugriffszeit des Baums aus

    relative_priorities enthält eine Liste der Node-Prioritäten in
    Reihenfolge von oben nach unten und links nach rechts, geteilt durch
    die Gesamtzahl aller Wörter.
    """

    def _depths(rootnode, array, depth):
        """
        Hilfsfunktion: Sammle alle Tiefen in 'array'.
        Wichtig: Knoten müssen in der selben Reihenfolge abgearbeitet 
        werden wie in der Hilfsfuntion _priorities()
        """
        if rootnode is None:
            return

        array.append(depth)

        _depths(rootnode._left, array, depth + 1)
        _depths(rootnode._right, array, depth + 1)

    if t._root is None:
        raise RuntimeError("depth(): tree is empty.")

    depths = []
    _depths(t._root, depths, 0)  # root ist bei Tiefe 0

    return sum([h*d for h, d in zip(relative_priorities, depths)])


def tree_sort(node, array):         # leeres dynamisches Array als 2. Argument
    if node is None:                # Rekursionsabschluss
        return
    tree_sort(node._left, array)    # rekursiv: kleine Schlüssel einfügen
    array.append(node._key)         # mittleren Schlüssel einfügen
    tree_sort(node._right, array)   # rekursiv: große Schlüssel einfügen



def compare_treaps(t1, t2):
    array1, array2 = [], []
    tree_sort(t1._root, array1)
    tree_sort(t2._root, array2)

    if array1 == array2:
        return True
    return False


if __name__ == "__main__":

    files = [
        'casanova-erinnerungen-band-2.txt',
        'die-drei-musketiere.txt',
        'helmholtz-naturwissenschaften.txt'
    ]

    for filename in files:
        print("\n###\n")
        print(f"Untersuchung von {filename}")
        s = open(filename, encoding="latin-1").read()
        for k in ',;.:="\'!?':
            s = s.replace(k, '')

        s = s.lower()
        text = s.split()

        rt = RandomTreap()
        dt = DynamicTreap()
        for word in text:
            rt[word] = None
            dt[word] = None

        if compare_treaps(rt, dt):
            print("Treaps enthalten gleiche Elemente in gleicher Sortierung")
        else:
            print("Treaps sind nicht gleich sortiert")

        N = len(text)
        print(f"Anzahl Wörter im Text: {N}")
        print(f"Anzahl verschiedener Wörter im Text: {len(dt)}")
        print(f"Tiefe RandomTreap: {rt.depth()}")
        print(f"Tiefe DynamicTreap: {dt.depth()}")
        print(f"Tiefe perfekt balancierter Baum {int(math.ceil(math.log(len(dt)) / math.log(2.0)))}")

        print(f"Mittlere Tiefe RandomTreap: {mean_depth(rt)}")
        print(f"Mittlere Tiefe DynamicTreap: {mean_depth(dt)}")

        prios = priorities(dt, N)

        print(f"Mittlere Zugriffszeit RandomTreap: {mean_access_time(rt, prios):.2f}")
        print(f"Mittlere Zugriffszeit DynamicTreap: {mean_access_time(dt, prios):.2f}")

        print("\nDie ~100 häufigsten Wörter:")

        # prios enthält alle Prioritätenvon dt =>
        # Top 100 Priorität ist das 100te Element vom Ende der sortierten Liste
        top = sorted(prios)[-100] * N 
        print(dt.top(top))

        filename = './stopwords.txt'
        s = open(filename, encoding="latin-1").read()
        for k in ',;.:="\'!?':
            s = s.replace(k, '')

        s = s.lower()
        stopwords = set(s.split())

        cleaned_treap = DynamicTreap()
        for word in text:
            if word in stopwords:
                continue
            cleaned_treap[word] = None

        print("\nDie ~100 häufigsten Wörter ohne stopwords:")

        prios = priorities(cleaned_treap, N)
        # prios enthält alle Prioritäten von cleaned_treap =>
        # Top 100 Priorität ist das 100te Element vom Ende der sortierten Liste
        top = sorted(prios)[-100] * N

        print(cleaned_treap.top(top))
