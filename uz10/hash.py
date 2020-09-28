


def hash1(daten):
    hashwerte = []
    for tripple in daten:
        hash = 0
        hash += 6 * tripple[0]
        hash += 6 * tripple[1]
        hash += 2 * tripple[2]
        hash = hash%11
        hashwerte.append(hash)
    return hashwerte

def hash2(daten):
    hashwerte = []
    for tripple in daten:
        hash = 0
        hash += 5 * tripple[0]
        hash += 1 * tripple[1]
        hash += 8 * tripple[2]
        hash = hash%13
        hashwerte.append(hash)
    return hashwerte

def hash3(daten):
    hashwerte = []
    for tripple in daten:
        hash = 0
        hash += 1 * tripple[0]
        hash += 2 * tripple[1]
        hash += 4 * tripple[2]
        hash = hash%11
        hashwerte.append(hash)
    return hashwerte

def is_minimal_perfekt_hash(hashwerte):
    for x in hashwerte:
        if hashwerte.count(x) != 1:
            print(x,"is", hashwerte.count(x), "times in list")
            return False
    for x in range(0, len(hashwerte)):
        if x not in hashwerte:
            print(x, "not in list")
            return False
    print ("appears to be an minimal perfekt hash")
    return True


daten = [(19, 7, 13), (10, 19, 10), (19, 11, 15), (3, 18, 11), (13, 7, 19), (14, 8, 14), (19, 14, 1), (10, 18, 3), (6, 11, 1), (3, 15, 15), (2, 10, 14)]


hashwerte = hash1(daten)
print (hashwerte)
is_minimal_perfekt_hash(hashwerte)
hashwerte = hash2(daten)
print (hashwerte)
is_minimal_perfekt_hash(hashwerte)
hashwerte = hash3(daten)
print (hashwerte)
is_minimal_perfekt_hash(hashwerte)


hashtabelle = []
for x in range(len(daten)):
    hashtabelle.append((hashwerte[x], daten[x]))

for n,m in sorted(hashtabelle):
    print(n, ":", m)
