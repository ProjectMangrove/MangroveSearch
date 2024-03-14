'''
General purpose functions

-- Generate the topology
    for i in n:
        generate the component
        add it to arr
        add exit nodes to the arr

    Connect each component in the arr to each other via some random node on the graph

-- Generate the component
    Make sure that there are at least n/4 random exit node
    Pair every node in the graph to each of those node
    randomly assign the other nodes

    return the exit nodes

-- connect components
    Set all other exit nodes to their own set
    
    randomly assign each exit node to a valid "other" node in the larger set, and those nodes to each other and remove those nodes

-- find path
    Uses basic BFS to find "shortest" paths

-- Generate paths(n)
    randomly pick n source-dest pairs and find the shortest path between them

    return the list of paths

'''
import random
from collections import defaultdict, deque
from pprint import pprint


class TopologyGenerator:
    '''
    Constructor
    '''
    def __init__(self, num_components, num_nodes):
        random.seed(5)
        # VALUES
        self.num_components = num_components
        self.num_nodes = num_nodes
        self.total_nodes = num_components * num_nodes

        # Topology graph
        self.g = defaultdict(list)

        # "BGP" nodes for each graph
        self.exits = []


    def generate_topology(self):
        # Generate all individual components first
        for i in range(self.num_components):
            self.generate_component(i*self.num_nodes, (i+1)*self.num_nodes)

            if not self.check_component(i*self.num_nodes, (i+1)*self.num_nodes):
                print("FAILED")
                return
        

        available_nodes = [i for i in range(0, self.total_nodes)]
        
        for exit in self.exits:
            self.connect_components(exit, available_nodes)

        # pprint(self.g)

    def generate_component(self, first, last):
        # Pick the first n/4 nodes to be exit nodes
        nodes = [i for i in range(first, last)]
        exits = nodes[:self.num_nodes // 4]
        others = nodes[self.num_nodes // 4:]
        
        # Add exits first
        for exit in exits:
            for node in nodes:
                if node != exit:
                    self.g[exit].append(node)

        # Now randomly generate the other connections
        for other in others:
            random.shuffle(nodes)

            self.g[other].extend(nodes[:self.num_nodes // 3])
        
        # Add all exits to the exit list
        self.exits.extend(exits)

    def connect_components(self, exit, available_nodes):
        random.shuffle(available_nodes)
        exit_count = 2

        for i in range(len(available_nodes)):
            exit_component = exit // self.num_nodes
            node_component = available_nodes[i] // self.num_nodes

            # If the current node is not the exit AND it is in a different connected component
            if available_nodes[i] != exit and exit_component != node_component:
                self.g[exit].append(available_nodes[i])
                self.g[available_nodes[i]].append(exit)
                available_nodes.remove(available_nodes[i])
                exit_count -= 1

            if exit_count == 0:
                break

    # Checks to see if component is strongly connected
    def check_component(self, start, end):
        nodes = [i for i in range(start, end)]

        for node in nodes:
            res = self.bfs(node)

            if res != self.num_nodes:
                print("FAILED ON NODE", node, "with reachable", res)
                return False
        
        return True
    
    def bfs(self, n):
        res = 1
        visited = set()
        q = deque()
        
        q.append(n)
        visited.add(n)

        while q:
            curr = q.popleft()

            for neighbor in self.g[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)
                    res += 1
        
        return res

    # USE BFS TO GENERATE PATHS from this node to all other nodes in the graph
    def generate_as_path(self, source, dest):
        # Find the path
        path = self.find_path(source, dest)
        
        if not path:
            return []
    
        as_path = []

        for i in range(1, len(path)):
            curr_component = path[i] // self.num_nodes
            last_component =  path[i - 1] // self.num_nodes

            if curr_component != last_component:
                as_path.append((path[i - 1], last_component))
                as_path.append((path[i], curr_component))
        
        return as_path

    def find_path(self, source, dest):
        visited = set()
        q = deque()

        q.append([source])
        visited.add(source)

        while q:
            all_elements = len(q)

            for i in range(all_elements):
                curr_path = q.popleft()
                curr_node = curr_path[-1]

                for neighbor in self.g[curr_node]:
                    if neighbor == dest:
                        curr_path.append(dest)
                        return curr_path
                    elif neighbor not in visited:
                        new_path = curr_path.copy()
                        new_path.append(neighbor)
                        q.append(new_path)
                        visited.add(neighbor)
        
        return []

    def generate_paths(self, n):
        pass

if __name__ == "__main__":
    topo = TopologyGenerator(6, 12)
    topo.generate_topology()

    res = topo.find_path(10, 44)
    as_res = topo.generate_as_path(10, 44)
    print(res)
    print(as_res)