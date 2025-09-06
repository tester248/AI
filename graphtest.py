from collections import deque


dq = deque("abcdef")

print(dq)

dq.append("g")
dq.appendleft("z")
print(dq)
dq.pop()
dq.popleft()
print(dq)



#graph creation
graph = {}
n = int(input("Enter number of Nodes in the graph: "))
for i in range(n):
    graph[i] = []
print(graph)
print("Empty Graph initialized")
e = int(input("Enter number of Edges in the graph: "))

for i in range(e):
    print(f"Enter edge {i+1} (source destination):")
    edge = input().split()

    u = int(edge[0])
    v = int(edge[1])
    
    if 0 <= u < n and 0 <= v <=n:
        graph[u].append(v)
        graph[v].append(u)
    else:
        print(f"Input not in range  0 to {n-1}")

print("Graph Created.")
print("Adjacency List:")
print(graph)


#adjacency matrix

adj_matrix = []
for i in range(n):
    row = []
    for j in range (n):
        row.append(0)
    adj_matrix.append(row)

print("Adjacency matrix initialized")
print(adj_matrix)

##populating the matrix

for node, neighbours in graph.items():
    for n in neighbours:
        adj_matrix[node][n] = 1
        adj_matrix[n][node] = 1

print("Populated Adjacency Matrix:")
for row in adj_matrix:
    print(row)





#adjacency list 