import math
import matplotlib.pyplot as plt

'''
Aufgabe 3 a):
    P1 = p1
    P2 = p1 + (p2-p1)/3
    P3 = p1 + (p2-p1)/2 + u * l/L # u = (p2-p1)"erte Zeile", -(p2-p1)"zweite Zeile") # L = Abstaand zwischen 2 p # l = sqrt((L/3)^2 - (L/6)^2)
    P4 = p1 + 2(p2-p1)/3
    P5 = p2
'''

def koch_snowflake(level):
    points_x = [0,1,1/2,0]
    points_y = [0,0,(math.sqrt(3)/2),0]
    for i in range(1,level+1):
        x = []
        L = abs((points_x[0] - points_x[1]))
        l = math.sqrt(((L / 3) * (L / 3) - ((L / 6) * (L / 6))))
        for n in range(len(points_x)-1):
            p = [points_x[n],points_y[n]]
            x.append(p)
            p = [points_x[n]+(points_x[n + 1]-points_x[n])/3,points_y[n]+(points_y[n + 1]-points_y[n])/3]
            x.append(p)
            p = [points_x[n]+(points_x[n + 1]-points_x[n])/2 + (points_y[n + 1]-points_y[n]) * (l/L) ,points_y[n]+(points_y[n + 1]-points_y[n])/2 - (points_x[n + 1]-points_x[n])* (l/L)]
            x.append(p)
            p = [points_x[n] + (2*(points_x[n + 1] - (points_x[n])) / 3), points_y[n] + 2*(points_y[n + 1] - points_y[n]) / 3]
            x.append(p)

        points_x = []
        points_y = []
        for m in range(len(x)):
            points_x.append(x[m][0])
            points_y.append(x[m][1])
        points_x.append(0)
        points_y.append(0)
    return points_x, points_y


points_x, points_y = koch_snowflake(4)

plt.plot(points_x, points_y)
plt.gca().set_aspect('equal')
plt.savefig('snowflake.svg')

f = open("snowflake.txt","w+")
for i in range(len(points_x)):
     f.write(str(points_x[i]))
     f.write(" ")
     f.write(str(points_y[i]))
     f.write("\n")
f.close()