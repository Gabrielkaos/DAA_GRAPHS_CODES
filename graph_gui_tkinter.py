import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq



class GraphApp:
    def __init__(self,root):

        #node_pos - stores (x, y) with key node name
        self.node_pos = {}
        #stores weighted connection between edges
        #key = node
        #value = dict with key node and value weight
        self.graph = {}


        self.root = root

        #create canvas
        #pack it both and expandable
        self.canvas = tk.Canvas(root, bg="white",height=600,width=600)
        self.canvas.pack(fill=tk.BOTH,expand=True)

        #now bind canvas to mouse clicks
        self.canvas.bind("<Button-1>",self.canvas_click)


        self.prim_button = tk.Button(root,text="Prim", command=self.prim_algo)
        self.prim_button.pack(side=tk.LEFT)

        self.kruskal_button = tk.Button(root,text="Kruskal", command=self.kruskal_algo)
        self.kruskal_button.pack(side=tk.LEFT)

        self.djikstra_button = tk.Button(root,text="Djikstra", command=self.djikstra_algo)
        self.djikstra_button.pack(side=tk.LEFT)

    def kruskal_algo(self):
        if not self.graph:
            messagebox.showerror("Error","No valid graph")
            return
        

        kruskal_window = tk.Toplevel(self.root)
        canvas = tk.Canvas(kruskal_window, bg="white",height=600, width=600)
        canvas.pack(fill=tk.BOTH,expand=True)

        edges = []
        for node, neighbors in self.graph.items():
            for neigbor, weight in neighbors.items():
                if (node, neigbor, weight) not in edges:
                    edges.append((neigbor,node,weight))

        
        edges.sort(key=lambda edge:edge[2])

        parent = {node:node for node in self.graph}
        rank   = {node:0 for node in self.graph}

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]
        
        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)

            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root2] > rank[root1]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1]+=1

        for node1, node2, weight in edges:
            if find(node1) != find(node2):
                union(node1, node2)

                x1, y1 = self.node_pos[node1]
                x2,y2  = self.node_pos[node2]

                canvas.create_line(x1,y1,x2,y2,tags='edge',arrow=tk.LAST)
                canvas.create_text((x1+x2)/2,(y1+y2)/2,text=weight,tags='edge_weight')

    def djikstra_algo(self):

        source = simpledialog.askstring("Source Node","Enter source node")
        if source not in self.graph:
            messagebox.showerror("Source node entered not in graph")
            return

        distances = {node:float('inf') for node in self.graph}
        distances[source] = 0
        predecessors = {node:None for node in self.graph}
        pq = [(0,source)]

        while pq:
            curr_distance, curr_node = heapq.heappop(pq)

            if curr_distance > distances[curr_node]:
                continue

            for neighbor, weight in self.graph[curr_node].items():
                distance = curr_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = curr_node
                    heapq.heappush(pq,(distance, neighbor))
        
        shortest_path = {}
        for node in self.graph:
            if node != source:
                path = []
                curr_node = node
                while curr_node is not None:
                    path.append(curr_node)
                    curr_node = predecessors[curr_node]
                path.reverse()

                shortest_path[node] = (distances[node],path)

        text = f"Shortest path from {source}\n"

        for node, (distance, path) in shortest_path.items():
            text+=f"{node}:{distance}:{"->".join(path)}\n"

        messagebox.showinfo("Shortest paths",text)
    
    def prim_algo(self):
        if not self.graph:
            messagebox.showerror("Error","No valid graph")
            return

        prim_window = tk.Toplevel(self.root)
        canvas = tk.Canvas(prim_window, bg="white",height=600, width=600)
        canvas.pack(fill=tk.BOTH,expand=True)

        source = list(self.graph.keys())[0]

        visited = set()
        pq = [(0,source, None)]

        while pq:
            curr_weight, curr_node, previous = heapq.heappop(pq)

            if curr_node in visited:
                continue

            visited.add(curr_node)

            if previous:
                x1, y1 = self.node_pos[(previous)]
                x2,y2  = self.node_pos[(curr_node)]

                canvas.create_line(x1,y1,x2,y2,tags='edge',arrow=tk.LAST)
                canvas.create_text((x1+x2)/2,(y1+y2)/2,text=curr_weight,tags='edge_weight')
            
            for neigbor, weight in self.graph[curr_node].items():
                if neigbor not in visited:
                    heapq.heappush(pq,(weight,neigbor, curr_node))

    def canvas_click(self, event):
        x, y = event.x, event.y

        clicked_node = self.nearest_node(x, y)

        if clicked_node:
            self.prompt_node(clicked_node)
        else:
            name = simpledialog.askstring("New Node","Enter name of Node")
            if name:
                self.node_pos[name] = (x, y)
                self.graph[name] = {}
                self.canvas.create_oval(x-10,y-10,x+10,y+10, fill="blue",tags=name)
                self.canvas.create_text(x,y,tags=name, text=name)
                self.prompt_node(name)   

    def nearest_node(self, x, y):

        for node, (node_x, node_y) in self.node_pos.items():
            distance = ((x - node_x)**2 + (y - node_y)**2) ** 0.5
            if distance < 15:
                return node
        return None
    
    def prompt_node(self, selected_node):

        if len(self.graph) > 1:
            connect_to = simpledialog.askstring("Connection", f"Connect {selected_node} to which node?")

            if connect_to:
                if connect_to in self.graph:
                    weight = simpledialog.askinteger("Weight of Edge","Enter weight of edge")
                    if weight is not None:
                        directed = messagebox.askyesno("Direction","Do you want the edge to be directed")
                        self.graph[selected_node][connect_to] = weight

                        if not directed:
                            self.graph[connect_to][selected_node] = weight
                        x1,y1 = self.node_pos[selected_node]
                        x2,y2 = self.node_pos[connect_to]

                        if directed:
                            self.canvas.create_line(x1,y1,x2,y2, arrow=tk.LAST,tags="edge")
                        else:
                            self.canvas.create_line(x1,y1,x2,y2,tags="edge")
                        
                        midx = (x1+x2) / 2
                        midy = (y1+y2) / 2

                        self.canvas.create_text(midx,midy, text=str(weight), tags="edge_weight")
                else:
                    messagebox.showerror("Error","Entered node not found!")


if __name__=="__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()