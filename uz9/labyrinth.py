from _collections import deque


maze = [[1],[3,2,0],[1],[5,4,1],[3],[7,6,3],[5],[10,8,5],[10,9,7],[8],[11,8,7],[13,12,10],[11],[15,14,11],[13],[13]]


def way_out(graph, startnode, targetnode):
    parents = [None]* len(graph)
    sackgassen = 0

    def visit(node, parent, sackgassen):
        if parents[node] == None:
            print(node)
            parents[node] = parent
            if node == targetnode:
                print ("target reached")
                return sackgassen, 0
            if len(graph[node]) == 1 and parents[graph[node][0]] != None:
                print ("dead end")
                sackgassen = sackgassen +1
                return sackgassen, 1
            for neighbor in graph[node]:
                sackgassen, x = visit(neighbor, node, sackgassen)
                if x == 0:
                    return sackgassen, 0
                if x == 1:
                    print ("backtrack")
            if parents[neighbor] != None:
                print("backtrack")
        return sackgassen, None


    sackgassen = visit (startnode, startnode, sackgassen)
    print ("Ahzahl Sackgassen: ", sackgassen[0])

#print("way_out(maze, 15, 0):")
#way_out(maze, 15, 0)


def way_out_stack(graph, startnode, targetnode):
    node = startnode
    parents = [None]* len(graph)
    mystack = deque()
    mystack.append(node)
    #print (node)
    parents[node] = node
    sackgasse = 0

    while (len(mystack) != 0):
        node = mystack.pop()
        print(node)
        if node == targetnode:
            mystack = []
            print ("target reached")
            break
        if len(graph[node]) == 1 and parents[graph[node][0]] != None:
            print("dead end")
            sackgasse = sackgasse+1

        for neighbor in reversed(graph[node]):
            if parents[neighbor] == None:
                parents[neighbor] = node
                mystack.append(neighbor)
                #print ("append", neighbor)

    print("Anzahl Sackgassen: ", sackgasse)

way_out_stack(maze, 15,0)