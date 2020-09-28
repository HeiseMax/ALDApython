import json
import heapq
import math

def create_graph(distance_dict):
    names = []
    for stadt in distance_dict:
        names.append(stadt)

    graph = [None]* len(names)
    for x in range(len(names)):
        graph[x] = []
        for nachbar in distance_dict[names[x]]["Nachbarn"]:
            graph[x].append(names.index(nachbar))

    weights = [None] * len(names)  #weights wird auch als list zurückgegeben, der Indexzugriff ist dadurch komplizierter, aber funktioniert auch (bsp.: siehe line 79)
    index = 0
    for stadt in distance_dict:
        weights[index] = []
        for nachbar in distance_dict[stadt]["Nachbarn"]:
            weights[index].append(distance_dict[stadt]["Nachbarn"][nachbar])
        index += 1

    return graph, names, weights

def compute_air_distances(distance_dict):
    stadt_koordinaten = []
    for stadt in distance_dict:
        koordB = distance_dict[stadt]["Koordinaten"]["Breite"]
        koordB = int(koordB[0:2]) + (int(koordB[3:5])/60)
        koordB = koordB/180*(math.pi)

        koordL = distance_dict[stadt]["Koordinaten"]["Länge"]
        koordL = int(koordL[0:2]) + (int(koordL[3:5]) / 60)
        koordL = koordL / 180 * (math.pi)
        stadt_koordinaten.append([koordB, koordL])

    air_distance = dict()
    r = 6378.137
    for start in range(len(stadt_koordinaten)): #air_distance muss alle Paare enthalten, da A* von jedem Punkt zu dem er kommt eine Streckenabschätzung braucht.
        for ziel in range(len(stadt_koordinaten)):
            if start == ziel:
                air_distance[start, ziel] = 0.0
            else:
                air_distance[start,ziel] = r * math.acos(\
                                            math.sin(stadt_koordinaten[start][0]) * math.sin(stadt_koordinaten[ziel][0]) \
                                            + math.cos(stadt_koordinaten[start][0]) * math.cos(stadt_koordinaten[ziel][0]) \
                                            * math.cos(stadt_koordinaten[ziel][1] - stadt_koordinaten[start][1]))
    return air_distance

def test_air_distance(graph, names, weights, air_distance): #Testet, ob die air_distance zu jeder Stadt kleiner ist, als die von dijkstra berechnete
    for x in range(len(names)):
        for j in range(len(names)):
            dist = dijkstra(graph, names, weights, names[x], names[j])

            if dist[1] < air_distance[x,j]:
                print(names[x],names[j])
                return False

    print("Air_Distance kleiner als Strassen_Distance!")
    return True

def dijkstra(graph, names, weights, start, destination):
    start = names.index(start)
    destination = names.index(destination)
    parents = [None] * len(names)
    q = []
    heapq.heappush(q,(0.0, start, start))
    untersuchte_staedte = 0
    while len(q) > 0:
        length, node, parent = heapq.heappop(q)
        untersuchte_staedte += 1
        if parents[node] == None:
            parents[node] = parent
        if node == destination:
            break
        for nachbar in graph[node]:
            if parents[nachbar] is None:
                new_length = length + weights[node][graph[node].index(nachbar)]
                heapq.heappush(q, (new_length, nachbar, node))
    route = []
    route.append(node)
    while node != start:
        route.append(parents[node])
        node = parents[node]
    route = route[::-1]

    def print_route(route):
        for x in range(len(route)):
            if x == 0:
                print(names[route[x]], end='')
            else:
                print(" ==>", weights[route[x]][graph[route[x]].index(parents[route[x]])], "Km ==>", names[route[x]],
                      end='')
        print(" (insgesamt:", length, "Km)")
        print("(Dijk): Untersuchte Städte:", untersuchte_staedte)

    print_route(route)
    return route, length

def a_star(graph, names, weights, air_distance, start, destination):
    start = names.index(start)
    destination = names.index(destination)
    parents = [None] * len(names)
    q = []
    heapq.heappush(q, (air_distance[start,destination],0.0, start, start))
    untersuchte_staedte = 0
    while len(q) > 0:
        priority, length, node, parent = heapq.heappop(q)
        untersuchte_staedte += 1
        if parents[node] == None:
            parents[node] = parent
        if node == destination:
            break
        for nachbar in graph[node]:
            if parents[nachbar] is None:
                new_length = length + weights[node][graph[node].index(nachbar)]
                heapq.heappush(q, (air_distance[nachbar,destination] + new_length,new_length, nachbar, node))

    route = []
    route.append(node)
    while node != start:
        route.append(parents[node])
        node = parents[node]
    route = route[::-1]

    def print_route(route):
        for x in range(len(route)):
            if x == 0:
                print(names[route[x]], end='')
            else:
                print(" ==>", weights[route[x]][graph[route[x]].index(parents[route[x]])], "Km ==>", names[route[x]],
                    end='')
        print(" (insgesamt:", length, "Km)")
        print("(A*): Untersuchte Städte:", untersuchte_staedte)

    print_route(route)
    return route, length



def main():
    with open('entfernungen.json', encoding='utf-8') as json_file:
        distance_dict = json.load(json_file)
    graph, names, weights = create_graph(distance_dict)
    air_distance = compute_air_distances(distance_dict)

    #test_air_distance(graph, names, weights, air_distance) #returns True für air_distance

    dijkstra(graph, names, weights, "Aachen", "Passau")
    a_star(graph, names, weights, air_distance, "Aachen", "Passau")
    print("")
    dijkstra(graph, names, weights, "Saarbrücken", "Leipzig")
    a_star(graph, names, weights, air_distance, "Saarbrücken", "Leipzig")
    print("")
    dijkstra(graph, names, weights, "München", "Greifswald")
    a_star(graph, names, weights, air_distance, "München", "Greifswald")
    print("")
    dijkstra(graph, names, weights, "Konstanz", "Kassel")
    a_star(graph, names, weights, air_distance, "Konstanz", "Kassel")

    print("")
    print("A* findet die gleichen Strecken, braucht aber deutlich weniger Schritte.")

main()
