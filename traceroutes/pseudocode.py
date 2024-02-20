'''
Processes traceroutes into an adjacency list format.

Input:
	traceroutes: list[list[string]]
		a list of traceroutes with each list in the traceroute representing a hop in the traceroute
		ie: [[IP1] -> [IP2a, IP2b] -> [IP3]]
		each ip should be in a string. missing hops should be represented as ["*"]
Output:
	adjacency_list: dict{list[string]}
		an adjacency list with the the nodes in the traceroute and the neighbors of each node
'''
def process_traceroutes(traceroutes):
	adjacency_list = {}
	for traceroute in traceroutes:
		last = None
		for ips in traceroute:
			if not ips or ips[0] == "*":
				last = None
				continue
			if last:
				for last_ip in last:
					for ip in ips:
						adjacency_list[last_ip].append(ip)
			for ip in ips:
				if ip not in adjacency_list:
					adjacency_list[ip] = []

	return adjacency_list
