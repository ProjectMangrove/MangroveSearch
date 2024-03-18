import json
from utils import pickle_list, unpickle_list
class TracerouteProcessor():
	'''
	Processes Traceroutes.
	...

	Attributes
	----------
		adjacency_list: dict{set[string]}
			an adjacency list with the the nodes in the traceroute and the neighbors of each node

	Methods
	-------
		process_traceroutes(traceroutes):
			processes a list of traceroutes into the adjacency list

	Each call of process_traceroutes() will add more traceroutes to the adjacency list.
	'''
	adjacency_list = {}

	def __init__(self, picklefile=None):
		'''
		Prcesses Traceroutes.

		### Parameters
			1. (optional) picklefile: string
				The file to unpickle the adjaceny_list from if testing.

		### Returns
			None
		'''
		self.adjacency_list = {}
		if picklefile:
			self.adjacency_list = unpickle_list(picklefile)
			for ip in self.adjacency_list:
				self.adjacency_list[ip] = set(self.adjacency_list[ip])

	def process_traceroutes(self, traceroutes, source):
		'''
		Processes a list of traceroutes into the adjacency list.

		### Parameters
			1. traceroutes: list[list[list[string]]]
				A list of traceroutes.
				Each list represents one singular traceroute.
				Each list in the traceroute representing a hop in the traceroute
				eg: [[[IP1], [IP2a, IP2b], [IP3]], [[IP1], [IP2]]]
				each ip should be in a string. missing hops should be represented as ["*"]

		### Returns
			None
		'''
		if source == 'caida':
			for traceroute in traceroutes:
				self.__process_traceroute(traceroute=traceroute)
		elif source == 'ripe':
			self.__process_ripe(traceroutes=traceroutes)
		else:
			pass

		pickle_list(self.adjacency_list, "adjlist.pk")

	def __process_ripe(self, traceroutes):
		'''
		Source built from: https://web.eecs.umich.edu/~harshavm/iplane/
		'''
		for line in traceroutes:
			src = line[0]
			dest = line[1]

			if src not in self.adjacency_list:
				self.adjacency_list[src] = set()

			self.adjacency_list[src].add(dest)

			if dest not in self.adjacency_list:
				self.adjacency_list[dest] = set()

			self.adjacency_list[dest].add(src)

	def __process_traceroute(self, traceroute):
		'''
		Processes traceroutes into the adjacency list format.

		### Parameters
			1. traceroute: list[list[string]]
				one singular traceroute. each list in the traceroute representing a hop in the traceroute
				ie: [[IP1] -> [IP2a, IP2b] -> [IP3]]
				each ip should be in a string. missing hops should be represented as ["*"]

		### Returns
			None
		'''
		last = None
		for ips in traceroute:
			if not ips or ips[0] == "*":
				last = None
				continue
			if last:
				for last_ip in last:
					for ip in ips:
						self.adjacency_list[last_ip].add(ip)
			for ip in ips:
				if ip not in self.adjacency_list:
					self.adjacency_list[ip] = set()
			last = ips

	def get_adjacency_list(self):
		'''
		Returns the adjacency list.

		### Returns
			adjacency_list: dict{set[string]}
				an adjacency list with the the nodes in the traceroute and the neighbors of each node
		'''
		return self.adjacency_list

	def dump_adjacency_list(self, filename):
		'''
		Dumps the adjacency list into the json file.

		### Parameters
			1. filename: string
				The filename to dump into. Should be a json.

		### Returns
			None
		'''
		adj_list = {}
		for ip in self.adjacency_list:
			adj_list[ip] = list(self.adjacency_list[ip])

		with open(filename, 'w') as f:
			json.dump(adj_list, f)

	def destroy_adjacency_list(self):
		'''
		Clears the adjacency list.
		'''
		self.adjacency_list = {}

	def in_adjacency_list(self, node):
		'''
		Check if node in adjacency list.

		### Parameters
			1. node : string
				A string representing the ip to be checked

		### Returns
			True if node in adjacency list
		'''
		return node in self.adjacency_list
