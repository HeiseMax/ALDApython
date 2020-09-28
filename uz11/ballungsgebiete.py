import json
import heapq
from _collections import deque
import matplotlib.pyplot as plt
import math


def create_graph(data):
    '''Erstellt den Graphen und die benoetigten property maps'''

    # Erstelle leere Adjazenzliste
    size = len(data)
    graph = [ [] for _ in range(size) ]

    # Erstelle leere property maps
    vertex_property_map = [""]*size
    edge_property_map = {}

    # Iteration über data um die Kanten der Adjazenzliste zu erstellen
    for city, item in data.items():
        i = item["Index"]
        vertex_property_map[i] = city
        for neighbour, distance in item["Nachbarn"].items():
            j = data[neighbour]["Index"]
            graph[i].append(j)
            edge_property_map[(i, j)] = float(distance)

    return graph, vertex_property_map, edge_property_map

def prim(graph, weights, start):
    parents = [None] * len(graph)
    q = []
    heapq.heappush(q,(0.0,start,start))
    sum = 0
    while len(q) > 0:
        length, node, parent = heapq.heappop(q)

        if parents[node] == None:
            parents[node] = parent
        else:
            continue
        sum += length
        for nachbar in graph[node]:
            if parents[nachbar] == None:
                heapq.heappush(q,(weights[(node, nachbar)], nachbar, node))
    return parents, sum

def kruskal(graph, weights):
    def find_anchor(anchors, node):
        start = node
        while node != anchors[node]:
            node = anchors[node]
        anchors[start] = node
        return node
    q = []
    sum = 0
    anchors = list(range(len(graph)))
    #print(anchors)
    result =[]
    for kante in weights:
        #print (kante)
        heapq.heappush(q, (weights[kante], kante))
    while len(q) > 0:
        length, edge = heapq.heappop(q)
        a1 = find_anchor(anchors, edge[0])
        a2 = find_anchor(anchors, edge[1])
        if a1 != a2:
            anchors[a2] = a1
            result.append(edge)
            sum += length
    #print(anchors)
    return result, sum

def mst_edges_kruskal(graph, weights):
    edges, length = kruskal(graph, weights)
    mst = dict()
    for i in range(0,len(graph)):
        for j in range(0, len(graph)):
            if (i, j) in edges:
                mst[(i,j)] = True
                mst[(j, i)] = True
            elif (j, i) in edges:
                mst[(i,j)] = True
                mst[(j, i)] = True
            else:
                mst[(i, j)] = False
    return mst

def mst_edges_prim(graph, weights):
    parents, length = prim(graph, weights, 0)
    edges = []
    for x in range(0,len(parents)):
        edges.append((x, parents[x]))
    mst = dict()
    for i in range(0,len(graph)):
        for j in range(0, len(graph)):
            if (i, j) in edges:
                mst[(i, j)] = True
                mst[(j, i)] = True
            elif (j, i) in edges:
                mst[(i, j)] = True
                mst[(j, i)] = True
            else:
                mst[(i, j)] = False
        mst[(0,0)] = False
    return mst

def cluster(graph, mst, weights, threshold):
    forest = []
    for n in range(len(graph)):
        nachbarn = []
        for m in range(len(graph)):
            if mst[(n,m)] == True:
                if weights[(n,m)] <= threshold:
                    nachbarn.append(m)
        forest.append(nachbarn)
    return forest

def components(forest):
    labels = [None] * len(forest)
    count = -1
    stack = deque()
    for x in range(len(forest)):
        if labels[x] == None:
            stack.append(x)
            count += 1
        #print(x)
        while len(stack) > 0:
            #print(stack)
            node = stack.pop()
            #print(stack)
            #print(node)
            if labels[node] == None:
                labels[node] = count
                for nachbar in forest[node]:
                    if labels[nachbar] == None:
                        stack.append(nachbar)
            else:
                continue
        #print(x)

    stack.append

    return labels, count+1

def main():
    with open('entfernungen.json', encoding='utf-8') as json_file:
        distance_dict = json.load(json_file)
    for i, city in enumerate(distance_dict):
        distance_dict[city]["Index"] = i
    graph, names, weights = create_graph(distance_dict)

    mst_parents, prim_len = prim(graph, weights, 0)
    mst_kanten , length = kruskal(graph,  weights)

    mst = mst_edges_kruskal(graph, weights)
    #print(mst)

    threshold = 150
    forest = cluster(graph, mst, weights, threshold)
    print(forest)
    print(len(forest))
    labels, count = components(forest)
    print(labels)
    print(count)
    threshold = 55
    forest = cluster(graph, mst, weights, threshold)
    print(forest)
    print(len(forest))
    labels, count = components(forest)
    print(labels)
    print(count)

    points_x = []
    points_y = []
    for x in range(0, 151):
        forest = cluster(graph, mst, weights, x)
        points_x.append(x)
        points_y.append(components(forest)[1])

    #plt.plot(points_x, points_y)
    #plt.gca().set_aspect('equal')
    #plt.savefig('ballungsgebiete.PNG')

    forest = cluster(graph, mst, weights, 30)
    labels, count = components(forest)
    ballung =[]
    #print (ballung)
    sum = 0
    for x in range(count):
        stadt = []
        if labels[x] == None:
            print("NOTFALL", x)
        for m in range(len(forest)):
            if labels[m] == x:
                stadt.append(names[m])
        ballung.append(stadt)
    print(ballung)

    ballung2 = []
    for x in range(count):
        stadt = []
        if labels[x] == None:
            print("NOTFALL", x)
        for m in range(len(forest)):
            if labels[m] == x:
                stadt.append(m)
        ballung2.append(stadt)
    print(ballung2)



    stadt_koordinaten = []
    breiten = []
    laengen = []
    for stadt in distance_dict:
        koordB = distance_dict[stadt]["Koordinaten"]["Breite"]
        koordB = int(koordB[0:2]) + (int(koordB[3:5]) / 60)
        #koordB = koordB / 180 * (math.pi)


        breiten.append(koordB)

        koordL = distance_dict[stadt]["Koordinaten"]["Länge"]
        koordL = int(koordL[0:2]) + (int(koordL[3:5]) / 60)
        #koordL = koordL / 180 * (math.pi)
        #stadt_koordinaten.append([koordB, koordL])
        laengen.append(koordL)
        plt.plot(koordL, koordB)
    print (stadt_koordinaten)

    #plt.plot(laengen, breiten)
    plt.gca().set_aspect('equal')

    plt.plot(linestyle='None')
    plt.savefig('map.PNG')
main()