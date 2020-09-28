import random
from _collections import deque

def print__pos(p):
    counter = 0
    for i in p:
        if i == ' ':
            print ("  ",i,end='')
        elif i < 10:
            print ("  ",i,end='')
        else:
            print( " ",i, end='')
        counter += 1
        if counter % 4 == 0:
            print ()

def up(p, pos):
    if pos >= 12:
        return pos
    p[pos], p[pos+4] = p[pos+4], p[pos]
    pos = pos + 4
    return pos
def down(p, pos):
    if pos <= 3:
        return pos
    p[pos], p[pos-4] = p[pos-4], p[pos]
    pos = pos - 4
    return pos
def right(p, pos):
    if pos%4 == 0:
        return pos
    p[pos], p[pos-1] = p[pos-1], p[pos]
    pos = pos - 1
    return pos
def left(p, pos):
    if pos%4 == 3:
        return pos
    p[pos], p[pos+1] = p[pos+1], p[pos]
    pos = pos + 1
    return pos
def move(p, pos, r):
    if r == 1:
        pos = up(p, pos)
        return pos
    elif r == 2:
        pos = down(p, pos)
        return pos
    elif r == 3:
        pos = right(p, pos)
        return pos
    elif r == 4:
        pos = left(p, pos)
        return pos
    else:
        return pos
def check_move(pos, r, lastMove):
    if r == 1:
        if pos >= 12:
            return False
        elif lastMove == 2:
            return False
        else:
            return True
    elif r == 2:
        if pos <= 3:
            return False
        elif lastMove == 1:
            return False
        else:
            return True
    elif r == 3:
        if pos%4 == 0:
            return False
        elif lastMove == 4:
            return False
        else:
            return True
    elif r == 4:
        if pos%4 == 3:
            return False
        elif lastMove == 3:
            return False
        else:
            return True
    else:
        return False

def shuffle_pos(N):
    pA = [' ',1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    pos = 0


    i = 0
    lastMove = 0
    while (i < N):
        r = random.randint(1,4)
        if check_move(pos, r, lastMove):
            pos = move(pA, pos, r)
            lastMove = r
            i  = i +1
    return pA

def solve_pos(p, maxmove):
    pA = [' ',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    parents = {str(p): p}
    q = deque()
    pCopy = p[:]
    q.append(pCopy)

    pos = 0
    lastMove = 0
    n = maxmove
    j = 0
    g = 1
    while len(q) > 0 and n != 0:
        node = q.popleft()



        for i in range(0, 16):
            if node[i] == ' ':
                pos = i

        for r in range(1,5):
            nodeCopy = node[:]

            if check_move(pos, r, lastMove):
                move(nodeCopy, pos, r)
                if str(nodeCopy) not in parents:
                    parents[str(nodeCopy)] = node
                    q.append(nodeCopy)
                    j = j+1
                if (nodeCopy) == pA:
                    n= 0
                    break
        g = g -1
        if g == 0:
            n = n -1
            if n > 0:
                g = j
                j = 0

    if str(pA) in parents:
        m = 0
        x = pA
        solution = []
        while x != p:
            solution.append(x)
            x = parents[str(x)]
            m = m +1
        solution.append(p)
        print ("Solved in " ,m , " moves!")
        print()
        for d in reversed(solution):
            print__pos(d)
            print()
    else:
        print__pos(p)
        print ("unsolved")

def main():
    pA = [' ',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    pA = shuffle_pos(15)

    solve_pos(pA, 15)


main()