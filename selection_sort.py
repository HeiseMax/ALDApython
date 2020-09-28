import random


def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        m = i
        for k in range(i + 1, n):
            if a[k] < a[m]:
                m = k
        a[i], a[m] = a[m], a[i]


def insertion_sort(a):
    n = len(a)
    for i in range(1, n):
        current = a[i]
        k = i
        while k > 0:
            if current < a[k - 1]:
                a[k] = a[k - 1]
            else:
                break
            k = k - 1
        a[k] = current


def merge(l, r):
    a = []
    i, k = 0, 0
    Nl, Nr = len(l), len(r)
    while i < Nl and k < Nr:
        if l[i] <= r[k]:
            a.append(l[i])
            i = i + 1
        else:
            a.append(r[k])
            k = k + 1
    a = a + l[i:Nl] + r[k:Nr]
    return a


def merge_sort(a):
    N = len(a)
    if N == 1:
        return a
    else:
        a_left = a[0:N // 2]
        a_right = a[N // 2:N]
        l_sorted = merge_sort(a_left)
        r_sorted = merge_sort(a_right)
        a_sorted = merge (l_sorted, r_sorted)
        return a_sorted

def partition(a, l , r ):
    pivot = a[l]
    i = l; k = r
    while True:
        while i < r and a[i]<= pivot:
            i = i + 1
        while k>l and a[k] >= pivot:
            k = k-1
        if i < k:
            a[i],a[k] = a[k],a[i]
        else:
            break
    a[l] = a[i-1]
    a[i-1] = pivot
    return i

def partition_random(a, l , r ):
    p = random.randint(l,r)
    a[p], a[l] = a[l], a[p]
    pivot = a[l]
    i = l; k = r
    while True:
        while i < r and a[i]<= pivot:
            i = i + 1
        while k>l and a[k] >= pivot:
            k = k-1
        if i < k:
            a[i],a[k] = a[k],a[i]
        else:
            break
    a[l] = a[i-1]
    a[i-1] = pivot
    return i

def quick_sort_impl(a, l,r ):
    if r<= l :
        return
    k = partition_random(a, l, r)
    quick_sort_impl(a, l, k-1)
    quick_sort_impl(a, k+1,r)

def quick_sort(a):
    quick_sort_impl(a, 0 ,(len(a) -1))


a = [7, 9, 3, 5, 9, 2]
#l = [2, 4, 6, 9]
#r = [1, 4, 5, 8]

# selection_sort(a)
# insertion_sort(a)
#a = merge_sort(a)
#quick_sort(a)
# a = merge(l,r)
# a.sort()

print(a)