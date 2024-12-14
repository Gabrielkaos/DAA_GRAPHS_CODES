


def kruskal(graph):

    edges = [] #weight, node1, node2
    vertices = [key for key in graph]
    for node in graph:
        connections = graph[node]
        for i,weight in enumerate(connections):
            if weight < 1:
                continue

            if (weight, vertices[i], node) not in edges:
                edges.append((weight, node, vertices[i]))

    edges.sort(key = lambda edge:edge[0])

    parent = {node:node for node in graph}
    rank = {node:0 for node in graph}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)

        if rank[root1]> rank[root2]:
            parent[root2] = root1
        elif rank[root1] < rank[root2]:
            parent[root1] = root2
        else:
            parent[root2] = root1
            rank[root1] +=1

    mst = []

    for weight, node1, node2 in edges:
        if find(node1) != find(node2):
            union(node1, node2)

            mst.append((weight, node1, node2))

    return mst