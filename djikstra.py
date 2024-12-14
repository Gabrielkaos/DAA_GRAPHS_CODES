import heapq


def djikstra(graph):
    vertices = [key for key in graph]

    source = vertices[0]


    distances = {node:float('inf') for node in graph}
    distances[source] = 0

    predeccesors = {node:None for node in graph}


    pq = [(0, source)]


    while pq:
        curr_weight, curr_node = heapq.heappop(pq)


        if curr_weight > distances[curr_node]:
            continue

        
        connection = graph[curr_node]
        for i,weight in enumerate(connection):
            if weight < 1:
                continue

            distance = curr_weight + weight
            neighbor = vertices[i]
            if distance < distances[vertices]:
                distances[neighbor] = distance
                predeccesors[neighbor] = curr_node
                heapq.heappush(pq, (distance, neighbor))


    shortest_path = {}

    for node in graph:
        if node != source:
            path = []
            curr_node = node
            while curr_node is not None:
                path.append(curr_node)
                curr_node = predeccesors[curr_node]
        
            path.reverse()
            shortest_path[node] = (distances[node], path)

            
            