import pytest
from random import randint

class Student:
    def __init__(self, name, mark):
        '''Construct new Student object with given 'name' and 'mark'.'''
        self._name = name
        self._mark = mark

    def get_name(self):
        '''Access the name.'''
        return self._name

    def get_mark(self):
        '''Access the mark.'''
        return self._mark

    def __repr__(self):
        '''Convert Student object to a string.'''
        return "%s: %3.1f" % (self._name, self._mark)

    def __eq__(self, other):
        '''Check if two Student objects are equal.'''
        return self._name == other._name and self._mark == other._mark

##################################################################

def insertion_sort_1(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.
    
    NOTE: THIS IMPLEMENTATION INTENTIONALLY CONTAINS A BUG, 
    WHICH YOUR TESTS ARE SUPPOSED TO DETECT.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            if key(a[j-1]) < key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

def insertion_sort(a,key=lambda x: x):
    n = len(a)
    for i in range(1, n):
        current = a[i]
        k = i
        while k > 0:
            if key(current) < key(a[k - 1]):
                a[k] = a[k - 1]
            else:
                break
            k = k - 1
        a[k] = current



def merge(l, r, key=lambda x: x):
    a = []
    i, k = 0, 0
    Nl, Nr = len(l), len(r)
    while i < Nl and k < Nr:
        if key(l[i]) <= key(r[k]):
            a.append(l[i])
            i = i + 1
        else:
            a.append(r[k])
            k = k + 1
    a = a + l[i:Nl] + r[k:Nr]
    return a


def merge_sort(a,key):
    N = len(a)
    if N == 1:
        return a
    else:
        a_left = a[0:N // 2]
        a_right = a[N // 2:N]

        l_sorted = merge_sort(a_left, key)
        r_sorted = merge_sort(a_right, key)

        if key == 'zahl':
            a_sorted = merge(l_sorted, r_sorted, int)
        elif key == 'name':
            a_sorted = merge(l_sorted, r_sorted, key=Student.get_name)

        elif key == 'mark':
            a_sorted = merge (l_sorted, r_sorted,key=Student.get_mark)

        return a_sorted

##################################################################

@pytest.fixture
def arrays():
    '''Create a dictionary holding test data.'''

    data = dict()
    
    # integer arrays
    data['int_arrays'] = [
        [],           # empty array
        [1],          # one element
        [2,1],        # two elements
        [3,2,3,1],    # the array from the exercise text
        [randint(0, 4) for k in range(10)], # 10 random ints
        [randint(0, 4) for k in range(10)]  # another 10 random ints
    ]

    # Student arrays
    data['student_arrays'] = [
       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.0),
        Student('Greg', 1.7),
        Student('Jill', 2.7),
        Student('Judy', 3.0),
        Student('Mike', 2.3),
        Student('Patt', 5.0)], # without replicated marks

       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.3),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Judy', 1.0),
        Student('Mike', 2.3),
        Student('Patt', 1.3)], # with replicated marks, alphabetic

       [Student('Bert', 2.0),
        Student('Mike', 2.3),
        Student('Elsa', 1.3),
        Student('Judy', 1.0),
        Student('Patt', 2.0),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Adam', 1.3)] # with replicated marks, random order
    ]
    
    return data

##################################################################

def test_checks():
    # test that the check_ functions actually find the desired errors
    ... # your code here
    check_integer_sorting([2,3,1],[1,2,3])


    check_student_sorting(
        [Student('Bert', 2.0),
        Student('Mike', 2.3),
        Student('Elsa', 1.3),
        Student('Judy', 1.0),
        Student('Patt', 2.0),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Adam', 1.3)],

        [Student('Judy', 1.0),
        Student('Greg', 1.0),
         Student('Elsa', 1.3),
        Student('Adam', 1.3),

        Student('Jill', 1.7),
        Student('Bert', 2.0),
        Student('Patt', 2.0),
        Student('Mike', 2.3)],
        'mark')

def test_builtin_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        ... # your code here (test that array is sorted)
        intSorted = sorted(original)
        check_integer_sorting(original, intSorted)


    # test the Student arrays
    for original in arrays['student_arrays']:
        ... # your code here (test that array is stably sorted)
        intSorted = sorted(original, key=Student.get_name)
        check_student_sorting(original, intSorted, 'name')
        intSorted = sorted(original, key=Student.get_mark)
        check_student_sorting(original, intSorted, 'mark')

def test_insertion_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        ... # your code here (test that array is sorted)
        intSorted = original
        insertion_sort_1(intSorted)
        check_integer_sorting(original, intSorted)

    # test the Student arrays
    for original in arrays['student_arrays']:
        ... # your code here (test that array is stably sorted)
        intSorted = original
        insertion_sort_1(intSorted, key=Student.get_name)
        check_student_sorting(original, intSorted, 'name')
        intSorted = original
        insertion_sort_1(intSorted, key=Student.get_mark)
        check_student_sorting(original, intSorted, 'mark')

        intSorted = original
        insertion_sort(intSorted, key=Student.get_name)
        check_student_sorting(original, intSorted, 'name')
        intSorted = original
        insertion_sort(intSorted, key=Student.get_mark)
        check_student_sorting(original, intSorted, 'mark')

def test_merge_sort(arrays):

    for original in arrays['int_arrays']:
        ... # your code here (test that array is sorted)
        intSorted = original
        merge_sort(intSorted, 'zahl')
        check_integer_sorting(original, intSorted)
    # test the Student arrays
    for original in arrays['student_arrays']:
        intSorted = original
        merge_sort(intSorted, 'name')
        check_student_sorting(original, intSorted, 'name')
        intSorted = original
        merge_sort(intSorted, 'mark')
        check_student_sorting(original, intSorted, 'mark')

def check_integer_sorting(original, result):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.'''
    ... # your code here
    assert len(original) == len(result)
    originalSet = set(original)
    resultSet = set(result)
    assert originalSet.difference(resultSet) == set()
    assert result == sorted(result)

def check_student_sorting(original, result, key):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.
    'key' is the attribute defining the order.
    '''
    ... # your code here
    assert len(original) == len(result)
    # Vergleichen der Elemente fehlt
    if (key == 'name'):
        assert result == sorted(result, key=Student.get_name)
    elif (key == 'mark'):
        assert result == sorted(result, key=Student.get_mark)
    if (key == 'mark'):
        assert result == sorted(original,key=Student.get_mark)
    elif (key == 'mark'):
        assert result == sorted(original, key=Student.get_mark)



'''Aufgabe 2 a) test_ sind die Test-Funktionen die von Pytest aufgerufen werden
                check_ sind Funktionen in denen man Tests definieren kann, die man dann in einem test_ aufrufen kann,
                sie werden aber von Pytest nicht automatisch aufgerufen.
                Fixtures können die Daten initialisieren, die für die Tests gebraucht werden,
                so kann man die selben Daten für alle Tests benutzen und sorgt so für kürzeren Code
                und konsistente Ergebnisse.
'''
