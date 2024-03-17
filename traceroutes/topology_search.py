import json
import random
from collections import deque
from pprint import pprint

import TracerouteProcessor


class Topology_Search:

    def __init__(self, traceroute_processor=None):
        if type(traceroute_processor) == dict:
            self.adj_list = traceroute_processor
        else:
            self.adj_list = traceroute_processor.get_adjacency_list()

    # Generic Topology Search
    def search_topology(self, node):
        network = self.adj_list
        q = deque()
        q.append(node)
        visited = set()

        while q:
            node = q.popleft()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in network[node]:
                if neighbor not in visited:
                    q.append(neighbor)
        
        return visited

    # Simple BFS that runs for n layers
    def search_topology_by_node(self, node, n):
        network = self.adj_list
        q = deque()
        q.append(node)
        visited = set()
        g = {}

        while q and n > 0:
            for _ in range(len(q)):
                node = q.popleft()
                if node in visited:
                    continue
                visited.add(node)
                g[node] = network[node].copy()
                for neighbor in network[node]:
                    if neighbor not in visited:
                        q.append(neighbor)
                        g[neighbor] = []
            n -= 1
        
        pprint(g)

        return json.dumps(g)
    
    # Picks a random IP address and runs an n layer BFS from that node
    def search_topology_random(self, n):
        network = self.adj_list

        random_node = random.choice(list(network.keys()))

        res = self.search_topology_by_node(random_node, n)

        return json.dumps(res)
    
    # Discovers the number of connected components in the network and the number of nodes in each component
    # Technically 
    def find_components(self):
        network = self.adj_list
        ALL_LAYERS = float('inf')
        # Components maps the starting IP to the number of nodes explored from there
        components = {}
        visited = set()

        for node in network:
            if node not in visited:
                res = self.search_topology(node)
                visited = visited.union(res)
                components[node] = len(res)
        
        return components

if __name__ == "__main__":
    adj_list = json.load(open('adjlist.json'))
    search = Topology_Search(adj_list)

    #search.search_topology_by_node('4.69.150.186', 10)
    search.search_topology_by_node('192.42.115.1', 10)
    #search.search_topology_random(10)
    #components = search.find_components()

    #pprint(len(components.keys()))