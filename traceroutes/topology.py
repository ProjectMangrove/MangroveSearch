import warts
from warts.traceroute import Traceroute

with open('amsterdam-traces.warts', 'rb') as f:
    record = warts.parse_record(f)
    while not isinstance(record, Traceroute):
        record = warts.parse_record(f)
    
    if record.src_address:
        print("Traceroute source address:", record.src_address)
    if record.dst_address:
        print("Traceroute destination address:", record.dst_address)
    print("Number of hops:", len(record.hops))
    print(record.hops)
