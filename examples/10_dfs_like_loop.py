# Purpose: Graph‑like traversal → metadata: O(V+E)
def dfs_like(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                stack.append(neighbor)

    return visited
