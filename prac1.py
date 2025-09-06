from collections import deque

def bfs(graph, start_node):
    queue = deque([start_node])  
    visited = {start_node}  
    traversal_order = [start_node]  

    print("Starting BFS from node:", start_node)
    while queue:
        current_node = queue.popleft()

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                traversal_order.append(neighbor) 

    return traversal_order

def dfs(graph, start_node, visited=None, traversal_order=None):
    if visited is None:
        visited = set()
        traversal_order = []
        print("Starting DFS from node:", start_node)
    
    visited.add(start_node)
    traversal_order.append(start_node)
    
    for neighbor in graph.get(start_node, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, traversal_order)
    
    return traversal_order

def print_adjacency_matrix(graph, n):
    print("\nGraph Adjacency Matrix:")
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for node in graph:
        for neighbor in graph[node]:
            matrix[node][neighbor] = 1
    
    print("   ", end="")
    for i in range(n):
        print(f"{i}", end=" ")
    print()
    
    for i in range(n):
        print(f"{i}", end="  ")
        for j in range(n):
            print(f"{matrix[i][j]}", end=" ")
        print()

def main():
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

        if 0 <= u < n and 0 <= v < n:  
            graph[u].append(v)
            graph[v].append(u)
        else:
            print(f"Input not in range 0 to {n-1}")

    print("Graph Created.")
    print("Adjacency List:")
    print(graph)
    
    print_adjacency_matrix(graph, n)

    while True:
        print("\nMenu:")
        print("1. BFS")
        print("2. DFS")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "3":
            print("Exiting...")
            break
        elif choice in ["1", "2"]:
            start_node = int(input("Enter starting node: "))
            
            if 0 <= start_node < n:
                if choice == "1":
                    result = bfs(graph, start_node)
                    print("BFS Traversal of Graph: ")
                elif choice == "2":
                    result = dfs(graph, start_node)
                    print("DFS Traversal of Graph: ")
                print(result)
            else:
                print(f"Invalid starting node. Please enter a node between 0 and {n-1}.")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()