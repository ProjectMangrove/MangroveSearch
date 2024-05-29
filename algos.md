# Thinking
## Overall thoughts
### Vocabulary
IPS: source ip \
IPD: Destination ip
### Use case
Say we don't have information regarding IPS to IPD, but we have information about another traceroute from an IP in the source AS to another IP in the destination AS.
### In words
Back up through IPS to the source AS. Check if the source AS has information about the destination AS. Grab the intermediary IPs.
### Output
source AS ... intermediary IPs ... destination AS
## Assumptions
We assume that the IP paths between ASs are probably quite similar. As such, we can probably group traceroutes based on AS level granularity.
## Pseudocode
Refer to **algorithm_thinking.py**
### Setting up
'''\
for each traceroute:\
    for each IP:\
        back up to find AS\
        grab destination AS\
        increment traceroutes in between by +1

traceroute[ip[+1]]

Basically, keep a running account of how many times we've seen
this intermediary path. This will allow us to give the "best"
possible path as in the path we've seen the most between two ASs.
IP level granularity in between.
Can resolve to AS resolution to compare with BGP dump information.
Combine for "best". Science needed\
'''\
Time complexity:\
O(n) iterate through each traceroute\
For each two IPS, we'll need to grab the IPs in the middle. Effectively n traceroutes x k ips per traceroute squared\
O(1) look up to increment, O(heapify) to reheap
Total will be n * k^2 * heapify

### Algorithm
'''\
back up to find source AS\
back up to find destination AS\
lookup destinationAS in sourceAS[dict]\
grab the intermediary path with the most counter\
Return source AS, intermediary, destination AS with confidence level\
'''\
Time complexity:\
O(1) lookup of source AS to find destination AS, if we use priority queue, we can get O(1) most popular route selection.

## Other thoughts
Don't really have much inference.\
Also could be way too simple. No flash involved??