from collections import deque


def bfs(graph, start_node):
    queue = deque([start_node])  # Initialize queue with the start_node
    visited = {start_node}       # Mark start_node as visited
    traversal_order = [start_node]  # Add start_node to the traversal order

    print("Starting BFS from node:", start_node)
    while queue:
        current_node = queue.popleft()

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                traversal_order.append(neighbor)  # Add neighbor to traversal order when discovered

    return traversal_order


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

    start_node = int(input("Enter starting node: "))
    if 0 <= start_node < n:
        bfs_result = bfs(graph, start_node)
        print("BFS Traversal of Graph: ")
        print(bfs_result)
    else:
        print(f"Invalid starting node. Please enter a node between 0 and {n-1}.")


if __name__ == "__main__":
    main()