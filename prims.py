import heapq


def prims(graph):
    vertices = [key  for key in graph]


    random_src = vertices[0]


    mst = []
    visited = set()
    pq = [(0, random_src, None)]


    while pq:
        weight, node, previous = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if (weight, node, previous) not in mst:
            mst.append((weight, previous, node))

        for node in graph:
            connections = graph[node]
            for i,weight in enumerate(connections):
                if weight < 1:
                    continue
                neighbor = vertices[i]
                if neighbor not in visited:
                    heapq.heappush(pq,(0,neighbor,node))



