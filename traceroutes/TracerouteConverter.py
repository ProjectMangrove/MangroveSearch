import os
import glob

class TracerouteConverter():
    def __init__(self, filename):
        self.filename = filename
        self.ruleDicts = {}


    def convertTraceroutes(self):
        '''
        this is what it should look like with 0,1,2,3 being ips
        0 1 2 3

        file 0
        fw 3 32 (full ip) 1
        fw 2 32 1
        fw 1 32 1
        '''
        ruleDicts = {}
        with open(self.filename, 'r') as f:
            for traceroute in f.readlines():
                traceroute = traceroute[:-1].split(" ")
                for i in range(len(traceroute)):
                    if traceroute[i] not in ruleDicts:
                        ruleDicts[traceroute[i]] = {}
                    for j in range(i+1, len(traceroute)):
                        curr_dict = ruleDicts[traceroute[i]]
                        curr_ip = traceroute[j]
                        if curr_ip in curr_dict:
                            assert i+1 < len(traceroute), f"{i+1} < {len(traceroute)}"
                            # assert curr_dict[curr_ip] == traceroute[i+1], f"{curr_dict[curr_ip]} {curr_dict} {traceroute}"

                        curr_dict[curr_ip] = traceroute[i+1]

        self.ruleDicts = ruleDicts

    def writeFibs(self):
        files = glob.glob("generated_fibs/*")
        for f in files:
            os.remove(f)
        for key in self.ruleDicts:
            with open("generated_fibs/"+key+"_fib.txt","w") as f:
                for key2 in self.ruleDicts[key]:
                    f.write("fw "+ key2 + " 32 " + self.ruleDicts[key][key2] + "\n")

        print(f"{len(self.ruleDicts)} files created")


        '''
        for traceroute in f.readlines():

        dict of dicts = {
            0:dict0
        }
        dict0 = {
            3:1,
            2:1,
            1:1
        }

        for key in dictofdicts:
            make new file for key
            for each key2 in dictkey
                fw key2 32 dictkey[key2]
        '''

if __name__ == "__main__":
    tc = TracerouteConverter("data/traceroutes.txt")
    tc.convertTraceroutes()
    tc.writeFibs()