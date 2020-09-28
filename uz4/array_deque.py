import doctest
import pytest
import time

###########################################################

class array_deque:

    def __init__(self):                   # constructor for empty container
        '''your documentation here'''
        self._size = 0                    # no item has been inserted yet
        self._capacity = 1                # we reserve memory for at least one item
        self._data = [None]               # internal memory (init one free cell)
        self._0Index  = 0                 # index of first Elem
        self._EndIndex = 0                  # index of last Elem
        
    def size(self):
        '''your documentation here
        returns the number of Elemnts in the container'''
        return self._size
        
    def capacity(self):
        '''your documentation here
        returns the number of avaliable memory cells'''
        return self._capacity                       # your code here
        
    def push(self, item):                 # add item at the end
        '''your documentation here
        appends item at the  end'''
        if self._capacity == self._size:  # internal memory is full
            dataCopy = [None] * (self._capacity * 2)
            for i in range (0,self._capacity):
                dataCopy[i] = self._data[i]
            self._capacity = self._capacity * 2                          # your code to double the memory
            self._data = dataCopy

        self._data[(self._0Index + self._size) % self._capacity] = item                               # your code to insert the new item
        self._size += 1
        self._EndIndex = (self._EndIndex + 1) % self._capacity
        
    def pop_first(self):
        '''your documentation here
        removes first element'''
        if self._size == 0:
            raise RuntimeError("pop_first() on empty container")
        else:                              # your code here
            self._0Index  = (self._0Index + 1) % self._capacity
            self._size -= 1

        
    def pop_last(self):
        '''your documentation here
        removes last element'''
        if self._size == 0:
            raise RuntimeError("pop_last() on empty container")
        else:
            self._EndIndex = (self._EndIndex - 1) % self._capacity
            self._size -= 1

        
    def __getitem__(self, index):         # __getitem__ implements v = c[index]
        '''your documentation here
        allows to read an element via index'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        return self._data[(self._0Index + index) % self._capacity]                        # your code here
        
    def __setitem__(self, index, v):      # __setitem__ implements c[index] = v
        '''your documentation here
        allows to alter an element via index'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        self._data[(self._0Index + index) % self._capacity] = v                               # your code here
        
    def first(self):
        '''your documentation here
        returns the first element of the container'''
        return self._data[self._0Index]                        # your code here
        
    def last(self):
        '''your documentation here
        returns the last element of the container'''
        return self._data[self._EndIndex]                        # your code here
        
    def __eq__(self, other):
        '''returns True if self and other have same size and elements'''
        if (self._size == other._size):                              # your code here
            for i in range(0, self._size):
                if (self[i] != other[i]):
                    return False
            return True
        else:
            return False


    def __ne__(self, other):
        '''returns True if self and other have different size or elements'''
        return not (self == other)

###########################################################

class slow_array_deque(array_deque):

    def push(self, item):                 # add item at the end
        if self._capacity == self._size:  # internal memory is full
            dataCopy = [None] * (self._capacity + 1)
            for i in range(0, self._capacity):
                dataCopy[i] = self._data[i]
            self._capacity = self._capacity +1
            self._data = dataCopy                           # code to enlarge the memory by one

        self._data[(self._0Index + self._size) % self._capacity] = item  # your code to insert the new item
        self._size += 1
        self._EndIndex = (self._EndIndex + 1) % self._capacity                             

###########################################################

def test_array_deque():
    F = array_deque()
    assert F._size == 0                                # your tests here#
    assert F._size <= F._capacity
    F.push("1")
    F.push("2")
    assert F.first() == F[0]
    assert F.last() == F[(F._size)-1]


#messen der zeit von push()
C = array_deque()

startC = time.time()
for i in range(0, 10000):
    C.push(i)

endC = time.time()
print(endC - startC)

startC = time.time()
for i in range(0, 100000):
    C.push(i)

endC = time.time()
print(endC - startC)

startC = time.time()
for i in range(0, 1000000):
    C.push(i)

endC = time.time()
print(endC - startC)

'''c)
    Die Anzahl der Aktionen wird verzehnfacht, die Zeit verzehnfacht sich im Mittel auch d.h. die Dauer einer Aktion
        hängt nicht von der Anzahl der Aktionen ab ==> push() ist amotisiert konstant'''

D = slow_array_deque()

start = time.time()
for i in range(0, 50):
    D.push(i)

end = time.time()
print(end - start)

start = time.time()
for i in range(0, 100):
    D.push(i)

end = time.time()
print(end - start)

start = time.time()
for i in range(0, 200):
    D.push(i)

end = time.time()
print(end - start)

'''d)
    Die Zeit steigt quadratisch zur Anzahl der Aktionen d.h. die Dauer einer Aktion
        hängt von der Anzahl der Aktionen ab ==> push() hat lineare Komplexität'''