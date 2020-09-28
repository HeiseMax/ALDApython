

def hash(s):
    h = 0
    for k in s:
        h = 23*h + ord(k)
    return h

s = []
s = open("collisions.txt", encoding="latin-1").read()
print (s)
s = s.split()
for i in s:
    print (hash(i))
'''
print (hash("Bbbb"))
print (hash("D5LK"))

print (hash("Aybb"))
print (hash("Axyb"))
print (hash("Axxy"))
print (hash("AxzK"))

print (hash("AzKb"))
print (hash("AzJy"))
print (hash("AzLK"))


print (hash("CKbb"))

print (hash("CJyb"))
print (hash("CJxy"))
print (hash("CJzK"))

print (hash("CLKb"))
print (hash("CLJy"))
print (hash("CLLK"))





print (("Bbbb"))
print (("D5LK"))

print (("Aybb"))
print (("Axyb"))
print (("Axxy"))
print (("AxzK"))

print (("AzKb"))
print ("AzJy")
print ("AzLK")


print (("CKbb"))

print (("CJyb"))
print (("CJxy"))
print (("CJzK"))

print (("CLKb"))
print (("CLJy"))
print (("CLLK"))

'''