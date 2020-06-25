import random
from matplotlib import pyplot as plt
from itertools import islice
import glob
import os
import itertools

path = '/Users/SAR/Desktop/CIRCE/Testing/Responses/Post-Vibe/'
pair_hex = []
rsp_ids = []
for filename in glob.glob(os.path.join(path, '*.pkt')):    
    with open(os.path.join(os.getcwd(), filename), 'rb') as f:
        a = ["{:02x}".format(c) for c in f.read()]
        b = a[90::264]
        pair_hex.append(a)
        rsp_ids.append(b)
#print(pair_hex)
flatten_hex = [item for items in pair_hex for item in items]
#print(rsp_id)
#print (len(pair_hex))
#print (len(rsp_id))


'''Directory for .pkt files. Change as required'''
#dp_directory = "/Users/SAR/Desktop/INMS/payload_packets_20200524_094852.pkt" 
#dp_directory = "/Users/SAR/Desktop/INMS/payload_packets_20200524_094026.pkt"
#dp_directory = "/Users/SAR/Desktop/INMS/payload_packets_20200524_105024.pkt"

'''Open the .pkt files, and split into hex pairs'''
#with open(dp_directory, 'rb') as f:
#    read_hex = f.read().hex()
#pair_hex = [read_hex[i:i+2] for i in range(0, len(read_hex), 2)]
#rsp_ids = pair_hex[90::264]
#print (pair_hex)

def identify_packets():
    #Check for the number and type of packet outputs
    print ("This file has %d data packets, which are broken down into:" %(len(rsp_ids)))
    if any('04' in s for s in rsp_ids):
        print(rsp_ids.count('04'), "stimulation packets (04)")
    if any('06' in s for s in rsp_ids):
        print(rsp_ids.count('06'), "health check packets (06)")
    if any('07' in s for s in rsp_ids):
        print(rsp_ids.count('07'), "calibration packets (07)")
    if any('08' in s for s in rsp_ids):
        print(rsp_ids.count('08'), "science packets (08)")
    if any('09' in s for s in rsp_ids):
        print(rsp_ids.count('09'), "house keeping packets (09)")
    if any('0a' in s for s in rsp_ids):
        print(rsp_ids.count('0a'), "stm packets (0a)")
    if any('0b' in s for s in rsp_ids):
        print(rsp_ids.count('0b'), "dump packets (0b)")
    if any('bb' in s for s in rsp_ids):
        print (rsp_ids.count('bb'), "error packets (bb)")
    if any('fa' in s for s in rsp_ids):
        print (rsp_ids.count('fa'), "obc error packets (fa)")

#identify_packets()

class packets_index():
    def get_packets_index(self,listOfElements, element):
        indexPosList = []
        indexPos = 0

        while True:
            try:
                # Search for item in list from indexPos to the end of list
                indexPos = listOfElements.index(element, indexPos)
                # Add the index position in list
                indexPosList.append(indexPos)
                indexPos += 1
            except ValueError as e:
                break
        return indexPosList

    def print_packets_index(self):
        rsp_id = '04'
        x = self.get_packets_index(rsp_ids, rsp_id)
        print ("The index position for", rsp_id, "is", x)
        print ("The distribution of all responses is", rsp_ids)

a = packets_index()
a.print_packets_index()

class stim_packets():

    def find_packets(self):
        result = []
        for idx, item in enumerate(flatten_hex):
            if item == '04' and flatten_hex[idx+1] == '00':
                result.append(flatten_hex[idx+2:idx+2+172])
        #print(result)
        flatten = [item for items in result for item in items]
        #print (result)
        #print(flatten)
        #print(len(result))

        endian_pairs = [i+j for i,j in zip(flatten[::2], flatten[1::2])] #pairs into groups of four
        self.endian = [int(h[2:4] + h[0:2], 16) for h in endian_pairs] #swap the halves and convert to Little Endian UINT16
        #print(endian_pairs)
        #print(len(endian_pairs))
        #print(self.endian)
        print(len(self.endian))
        
        self.plot_stim_data()

    
    def packets_range(self):
        stim_pack1 = pair_hex[354+2:528:1]
        stim_pack2 = pair_hex[882+2:1056:1]
        stim_pack3 = pair_hex[1938+2:2112:1]
        stim_pack4 = pair_hex[2466+2:2640:1]
        stim_pack5 = pair_hex[3522+2:3696:1]
        stim_pack6 = pair_hex[4050+2:4224:1]
        stim_pack7 = pair_hex[5106+2:5280:1]

        stim_packs = stim_pack1 + stim_pack2 + stim_pack3 + stim_pack4 + stim_pack5 + stim_pack6 + stim_pack7
        #print(stim_packs)

        '''Printed value should be 172. Used for validation'''
        #print((len(stim_packs))/rsp_ids.count('04'))

        '''Create endian pairs'''
        endian_pairs = [i+j for i,j in zip(stim_packs[::2], stim_packs[1::2])] #pairs into groups of four
        self.endian = [int(h[2:4] + h[0:2], 16) for h in endian_pairs] #swap the halves and convert to Little Endian UINT16
        #print(self.endian)
        #print (len(self.endian))

        self.plot_stim_data()

    def plot_stim_data(self):
        data = self.endian
        
        plt.ylim([min(data)-5, max(data)-63000])
        plt.xlim([min(data)+100, max(data)-62000])
        plt.hist(data, bins=800, alpha=0.5)

        #plt.title('STIM Packet, Count Distribution')
        plt.xlabel('Time')
        plt.ylabel('Count')
        
        try:
            plt.savefig("CIRCE_figs/STIM-04_FM1-2_b800.png", bbox_inches='tight')
            print ("File saved")
        except IOError:
            print ("File creation failed")
        
        #plt.show()

j = stim_packets()
j.find_packets()