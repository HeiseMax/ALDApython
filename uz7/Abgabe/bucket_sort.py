from math import sqrt as sqrt
import random
import timeit
import pytest

def insertionSort(a):   # sort 'a' in-place
    N = len(a)          # number of elements
    
    for i in range(N):
        current = a[i]  # remember the current element
        # find the position of the gap where 'current' is supposed to go
        j = i       # initial guess: 'current' is already at the correct position
        while j > 0:
            if current < a[j-1]:  # a[j-1] should be on the right of 'current'
                a[j] = a[j-1]     # move a[j-1] to the right
            else:
                break             # gap is at correct position
            j -= 1                # shift gap one index to the left
        a[j] = current            # place 'current' into appropriate gap

    return a

def quantize1(r, M):
    if r != 0:
        index = int((1/r^2)*M) #Die Verteilung wächst quadratisch mit dem Radius was man an der Flächenformel des Kreises erkennt
    else:
        index = 0
    return index

def quantize2(r, M):
    return r*M
    
def BucketSort(a, quantize, d):
    N = len(a)
    M = int(N / float(d))  # Anzahl der Buckets festlegen
      
    # M leere Buckets erzeugen
    buckets = [[] for k in range(M)]
      
    # Daten auf die Buckets verteilen
    for k in range(len(a)):
        index = quantize(a[k].key, M) # Bucket-Index berechnen
        buckets[index].append(a[k])    # a[k] im passenden Bucket einfügen
      
    # Daten sortiert wieder in a einfügen
    start = 0                          # Anfangsindex des ersten Buckets 
    for k in range(M):
        insertionSort(buckets[k])      # Daten innerhalb des aktuellen Buckets sortieren
        end = start + len(buckets[k])  # Endindex des aktuellen Buckets
        a[start:end] = buckets[k]      # Daten an der richtigen Position in a einfügen
        start += len(buckets[k])       # Anfangsindex für nächsten Bucket aktualisieren

    return a

def build_buckets(a, quantize, d):
    N = len(a)
    M = int(N / float(d))  # Anzahl der Buckets festlegen
      
    # M leere Buckets erzeugen
    buckets = [[] for k in range(M)]
      
    # Daten auf die Buckets verteilen
    for k in range(len(a)):
        index = quantize(a[k].key, M) # Bucket-Index berechnen
        buckets[index].append(a[k])    # a[k] im passenden Bucket einfügen

    return buckets

def chi_squared(buckets):
    M = len(buckets) #Anzahl der buckets
    N = 0
    for k in len(buckets):
        N += len(buckets[k])
    
    chi_squared = 0
    
    for k in len(buckets):
        additional = ((len(buckets[k])^2-(N/M)))/(N/M)
        chi_squared += additional

    tau = sqrt(2*chi_squared) - sqrt(2*M-3)

    if abs(tau) > 3:
        return False
    else:
        return True

def create_data(size):
    a = []
    while len(a) < size:
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
    r = sqrt(x**2 + y**2)
    if r < 1.0: # der Punkt (x,y) liegt im Einheitskreis
        a.append(r)
    return a

def test_quantize():
    
    a = create_data(10)
    b = build_buckets(a, quantize1, 2)
    assert chi_squared(b)==True

    a = create_data(10)
    b = build_buckets(a, quantize1, 3)
    assert chi_squared(b)==True

    a = create_data(10)
    b = build_buckets(a, quantize1, 4)
    assert chi_squared(b)==True

    a = create_data(10)
    b = build_buckets(a, quantize2, 2)
    assert chi_squared(b)==False

    a = create_data(10)
    b = build_buckets(a, quantize2, 3)
    assert chi_squared(b)==False

    a = create_data(10)
    b = build_buckets(a, quantize2, 4)
    assert chi_squared(b)==False

    a = create_data(100)
    b = build_buckets(a, quantize1, 2)
    assert chi_squared(b)==True

    a = create_data(100)
    b = build_buckets(a, quantize1, 10)
    assert chi_squared(b)==True

    a = create_data(100)
    b = build_buckets(a, quantize1, 20)
    assert chi_squared(b)==True

    a = create_data(100)
    b = build_buckets(a, quantize2, 2)
    assert chi_squared(b)==False

    a = create_data(100)
    b = build_buckets(a, quantize2, 10)
    assert chi_squared(b)==False

    a = create_data(100)
    b = build_buckets(a, quantize2, 20)
    assert chi_squared(b)==False

    a = create_data(1000)
    b = build_buckets(a, quantize1, 10)
    assert chi_squared(b)==True

    a = create_data(1000)
    b = build_buckets(a, quantize1, 100)
    assert chi_squared(b)==True

    a = create_data(1000)
    b = build_buckets(a, quantize1, 200)
    assert chi_squared(b)==True

    a = create_data(1000)
    b = build_buckets(a, quantize2, 10)
    assert chi_squared(b)==False

    a = create_data(1000)
    b = build_buckets(a, quantize2, 100)
    assert chi_squared(b)==False

    a = create_data(1000)
    b = build_buckets(a, quantize2, 200)
    assert chi_squared(b)==False

test_quantize()

def test_BucketSort(): #Der Code von insertionsort wurde bereits getestet und ist daher verlässlich
    a = create_data(10)
    assert BucketSort(a, quantize1, 5)==insertionSort(a)
    assert BucketSort(a, quantize1, 4)==insertionSort(a)
    assert BucketSort(a, quantize1, 2)==insertionSort(a)
    assert BucketSort(a, quantize2, 5)==insertionSort(a)
    assert BucketSort(a, quantize2, 4)==insertionSort(a)
    assert BucketSort(a, quantize2, 2)==insertionSort(a)

    a = create_data(100)
    assert BucketSort(a, quantize1, 5)==insertionSort(a)
    assert BucketSort(a, quantize1, 4)==insertionSort(a)
    assert BucketSort(a, quantize1, 2)==insertionSort(a)
    assert BucketSort(a, quantize2, 5)==insertionSort(a)
    assert BucketSort(a, quantize2, 4)==insertionSort(a)
    assert BucketSort(a, quantize2, 2)==insertionSort(a)

    a = create_data(1000)
    assert BucketSort(a, quantize1, 5)==insertionSort(a)
    assert BucketSort(a, quantize1, 4)==insertionSort(a)
    assert BucketSort(a, quantize1, 2)==insertionSort(a)
    assert BucketSort(a, quantize2, 5)==insertionSort(a)
    assert BucketSort(a, quantize2, 4)==insertionSort(a)
    assert BucketSort(a, quantize2, 2)==insertionSort(a)

test_BucketSort()

code_to_be_measured = '''
BucketSort(a, quantize1, 5)
'''
initalisation = '''
a = create_data(10)
'''
t = timeit.Timer (code_to_be_measured, initalisation)
time = t.timeit(5)
print (time/5)

code_to_be_measured = '''
BucketSort(a, quantize2, 5)
'''
initalisation = '''
a = create_data(10)
'''
t = timeit.Timer (code_to_be_measured, initalisation)
time = t.timeit(5)
print (time/5)

code_to_be_measured = '''
BucketSort(a, quantize1, 5)
'''
initalisation = '''
a = create_data(100)
'''
t = timeit.Timer (code_to_be_measured, initalisation)
time = t.timeit(10)
print (time/10)

code_to_be_measured = '''
BucketSort(a, quantize2, 5)
'''
initalisation = '''
a = create_data(100)
'''
t = timeit.Timer (code_to_be_measured, initalisation)
time = t.timeit(10)
print (time/10)



