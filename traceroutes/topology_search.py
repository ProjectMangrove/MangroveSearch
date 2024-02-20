import json
import random
from collections import deque

import traceroute_processor


class Topology_Search:

    def __init__(self, traceroute_processor=None):
        self.processor = traceroute_processor

    # Simple BFS that runs for n layers
    def search_topology_by_node(self, node, n):
        network = self.processor.get_adjacency_list()
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
        
        return json.dumps(g)
    
    def search_topology_random(self, n):
        network = self.processor.get_adjacency_list()

        random_node = random.choice(list(network.keys()))

        res = self.search_topology_by_node(random_node)

        return json.dumps(res)