
class Traceroute_Processor():
	'''
	Processes Traceroutes.
	'''
	def Traceroute_Processor(self):
		self.adjacency_list = None
		pass


	def process_traceroutes(self, traceroutes):
		'''
		Processes traceroutes into an adjacency list format.

		### Parameters
			1. traceroutes: list[list[string]]
				a list of traceroutes with each list in the traceroute representing a hop in the traceroute
				ie: [[IP1] -> [IP2a, IP2b] -> [IP3]]
				each ip should be in a string. missing hops should be represented as ["*"]

		### Returns
			adjacency_list: dict{list[string]}
				an adjacency list with the the nodes in the traceroute and the neighbors of each node
		'''
		self.adjacency_list = {}
		for traceroute in traceroutes:
			last = None
			for ips in traceroute:
				if not ips or ips[0] == "*":
					last = None
					continue
				if last:
					for last_ip in last:
						for ip in ips:
							self.adjacency_list[last_ip].append(ip)
				for ip in ips:
					if ip not in self.adjacency_list:
						self.adjacency_list[ip] = []

		return self.adjacency_list

	def get_adjacency_list(self):
		'''
		Returns the adjacency list.

		### Returns
			adjacency_list: dict{list[string]}
				an adjacency list with the the nodes in the traceroute and the neighbors of each node
		'''
		return self.adjacency_list
