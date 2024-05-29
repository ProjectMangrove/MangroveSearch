'''
for each traceroute:
    for each IP:
        back up to find AS
        grab destination AS
        increment traceroutes in between by +1

traceroute[ip[+1]]

Basically, keep a running account of how many times we've seen
this intermediary path. This will allow us to give the "best"
possible path as in the path we've seen the most between two ASs.
IP level granularity in between.
Can resolve to AS resolution to compare with BGP dump information.
Combine for "best". Science needed
'''

'''
back up to find source AS
back up to find destination AS
lookup destinationAS in sourceAS[dict]
grab the intermediary path with the most counter
Return source AS, intermediary, destination AS with confidence level

O(1) lookup to find
'''