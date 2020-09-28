
maze = [[1],[3,2,0],[1],[5,4,1],[3],[7,6,3],[5],[10,8,5],[10,9,7],[8],[11,8,7],[13,12,10],[11],[15,14,11],[13],[13]]

def way_out(graph, startnode, targetnode):
    visited = [False]*len(graph)  # Flags, welche Knoten bereits besucht wurden
    de=[0]
    def visit(node):              # rekursive Hilfsfunktion, die den gegebenen Knoten und dessen Nachbarn besucht
        if not visited[node]:     # Besuche node, wenn er noch nicht besucht wurde
            visited[node] = True  # Markiere node als besucht
            print(node)           # Ausgabe der Knotennummer - pre-order
            if len(graph[node]) == 1 and node != startnode:
                print("dead end")
                print("backtrack")
                de[0] += 1
            for neighbor in graph[node]:   # Besuche rekursiv die Nachbarn
                if neighbor == targetnode:
                    print(neighbor)
                    print("target reached")
                    print("Anzahl der Sackgassen:")
                    print(de[0])
                    break
                visit(neighbor)

    visit(startnode)

#way_out(maze, 15, 0)

print("--------------------------------")

def way_out_stack(graph, startnode, targetnode):
    stack = [[startnode, 0]]
    de = [0]
    while len(stack) > 0:
        k = stack.pop()
        node = k[0]
        current_neighbor = k[1]
        print(node)
        if node == targetnode:
            print("target reached")
            print("Anzahl Sackgassen:")
            print(de[0])
            break
    
        else:
            if current_neighbor < len(graph[node]):
                stack.append([node,current_neighbor+1])
            else:
                print("dead end")
                de [0] += 1
                print("back track")
            stack.append([graph[node][current_neighbor],0])

            

way_out_stack(maze, 15, 0)