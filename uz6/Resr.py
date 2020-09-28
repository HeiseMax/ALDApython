@staticmethod
def top_impl(root, a, min_priority):
    if root != None:
        if root._priority >= min_priority:
            a.append([root._key, root._priority])
        DynamicTreap.top_impl(root._l, a, min_priority)
        DynamicTreap.top_impl(root._l, a, min_priority)
    return a


def top(self, min_priority):
    root = self._root
    a = []
    x = DynamicTreap.top_impl(root, a, min_priority)
    return x


# File einlesen und nach Unicode konvertieren (damit Umlaute korrekt sind)
s = open("helmholtz-naturwissenschaften.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
    s = s.replace(k, '')  # Sonderzeichen entfernen
s = s.lower()  # Alles klein schreiben
text = s.split()  # String in Array von Wörtern umwandeln
# Die Wörter in text werden nun in die beiden Treaps eingefügt:
rt = RandomTreap()
dt = DynamicTreap()
for word in text:
    rt[word] = None  # die values werden in dieser Übung nicht benötigt
    dt[word] = None  # alternativ können die values als Zähler dienen


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


print(compare_trees(rt, dt))
print(rt._size)
# Ein perfekt balancierter Baum hätte Tiefe log(rt._size)= ?
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
    x = middepth_impl(root, 0, 0)
    md = x / tree.depth
    return md


print(middepth(rt))
print(middepth(dt))


def midaccess_impl(root, sum, k):
    k += 1
    if root == None:
        return sum
    else:
        sum += k * root._priority
        midaccess_impl(root._l, sum, k)
        midaccess_impl(root._r, sum, k)


def midaccess(tree):
    root = tree._root
    x = midaccess_impl(root, 0, 0)
    ma = x / tree.depth
    return ma


print(midaccess(rt))
print(midaccess(dt))

print(dt.top(30))

s = open("stopwords.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
    s = s.replace(k, '')  # Sonderzeichen entfernen
s = s.lower()  # Alles klein schreiben
text = s.split()  # String in Array von Wörtern umwandeln
# Die Wörter in text werden nun in die beiden Treaps eingefügt:
y = set()
for word in text:
    set.add(word)

s = open("helmholtz-naturwissenschaften.txt", encoding="latin-1").read()
for k in ',;.:-"\'!?':
    s = s.replace(k, '')  # Sonderzeichen entfernen
s = s.lower()  # Alles klein schreiben
text = s.split()  # String in Array von Wörtern umwandeln
# Die Wörter in text werden nun in die beiden Treaps eingefügt:
cleaned_treap = DynamicTreap()
for word in text:
    x = set(word)
    if y.isdisjoint(x) == False:
        cleaned_treap[word]

print(cleaned_treap.top(20))
















