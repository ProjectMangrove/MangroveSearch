import warts
from warts.traceroute import Traceroute
from TracerouteProcessor import TracerouteProcessor
from utils import pickle_list, unpickle_list


DEBUG = False
def DebugPrint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class TracerouteReader:
    '''
    A class to read traceroutes.

    Attributes
    ----------
        traceroute_list: list[list[list[str]]]
                A list of list of lists of strings.
                Each hop is a list (ECMP) of strings,
                each traceroute is a list of lists,
                and so all traceroutes is a list of list of lists.

    Methods
    -------
        generate_traceroute_list: None -> None
            generates a list of traceroutes from the warts file
        get_traceroute_list: None -> list[list[list[str]]]
            gets the traceroute list
    '''
    traceroute_list = []

    def __init__(self, filename, picklefile=None):
        '''
        A class to read traceroutes

        ### Parameters
            1. filename: string
                The name of the file to be parsed. Should be a .warts
            2. (optional) picklefile: string
                The name of the pickle file to unpickle the list from. Use if testing.
        '''
        self.filename = filename
        if picklefile:
            self.traceroute_list = unpickle_list(picklefile)

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
        '''
        Generates the list of traceroutes from a warts file
        '''
        ctr = 0
        with open(self.filename, 'rb') as f:
            while True:
                record = warts.parse_record(f)
                if record is None:
                    break

                if not isinstance(record, Traceroute):
                    warts.parse_record(f)
                    continue

                traceroute = []

                for hop in record.hops:
                    traceroute.append([hop.address])

                self.traceroute_list.append(traceroute)
                ctr += 1
                if ctr % 50000 == 0:
                    print(f'Traceroute {ctr} completed')

        pickle_list(self.traceroute_list, "trlist.pk")

    def get_traceroute_list(self):
        '''
        Gets the list of traceroutes

        ### Returns
            traceroute_list: list[list[list[str]]]
                A list of list of lists of strings.
                Each hop is a list (ECMP) of strings,
                each traceroute is a list of lists,
                and so all traceroutes is a list of list of lists.
        '''
        return self.traceroute_list

    def print_one_traceroute(self):
        with open(self.filename, 'rb') as f:
            record = warts.parse_record(f)
            while not isinstance(record, Traceroute):
                record = warts.parse_record(f)
            if record.src_address:
                print("Traceroute source address:", record.src_address)
            if record.dst_address:
                print("Traceroute destination address:", record.dst_address)
            print("Number of hops:", len(record.hops))
            print(record.hops)

if __name__ == "__main__":
    # this is a complete run
    tr = TracerouteReader("amsterdam.warts")
    tr.generate_traceroute_list()
    traceroute_list = tr.get_traceroute_list()
    print(traceroute_list[:5])

    tp = TracerouteProcessor()
    tp.process_traceroutes(traceroutes=traceroute_list)
    tp.dump_adjacency_list('adjlist.json')

    # if you've already ran the above and you're just doing some testing, you can run:
    # tr = TracerouteReader("amsterdam.warts", 'trlist.pk')
    # and then you can directly just use the traceroute list or you can run
    # tp = TracerouteProcessor('adjlist.pk')
    # and then you can directly use the adjacency list using getters

    # before using remember to pip3 install scamper-pywarts
    # https://github.com/drakkar-lig/scamper-pywarts
