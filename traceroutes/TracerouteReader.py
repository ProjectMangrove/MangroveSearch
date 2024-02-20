import warts
from warts.traceroute import Traceroute


DEBUG = False
def DebugPrint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class TracerouteReader:
    def __init__(self, filename):
        self.filename = filename

    def print_traceroutes(self, lines):
        ctr = 0
        with open(self.filename, 'rb') as f:
            while ctr < lines:
                record = warts.parse_record(f)
                if record is None:
                    break
                
                if not isinstance(record, Traceroute):
                    warts.parse_record(f)
                    continue
                
                if record.src_address:
                    DebugPrint("Traceroute source address:", record.src_address)
                if record.dst_address:
                    DebugPrint("Traceroute destination address:", record.dst_address)
                DebugPrint("Number of hops:", len(record.hops))
                DebugPrint("Hops:", record.hops, end='\n\n')
                DebugPrint(vars(record.hops[0]))
                ctr += 1
    
    def generate_traceroute_list(self):
        ctr = 0
        traceroute_list = []
        with open(self.filename, 'rb') as f:
            while True:
                record = warts.parse_record(f)
                if record is None:
                    break
                
                if not isinstance(record, Traceroute):
                    warts.parse_record(f)
                    continue
                
                traceroute = []

                if record.src_address:
                    traceroute.append(record.src_address)

                for hop in record.hops:
                    traceroute.append(hop.address)

                traceroute_list.append(traceroute)
                ctr += 1
        
        return traceroute_list
