import warts
from warts.traceroute import Traceroute


def print_traceroutes(filename, lines):
    ctr = 0
    with open(filename, 'rb') as f:
        while ctr < lines:
            record = warts.parse_record(f)
            if record is None:
                break
            
            if not isinstance(record, Traceroute):
                warts.parse_record(f)
                continue
            
            if record.src_address:
                print("Traceroute source address:", record.src_address)
            if record.dst_address:
                print("Traceroute destination address:", record.dst_address)
            print("Number of hops:", len(record.hops))
            print("Hops:", record.hops, end='\n\n')
            ctr += 1

print_traceroutes('amsterdam-traces.warts', 5)