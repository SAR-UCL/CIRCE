'''External modules'''
import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In'
#path = r'//Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/Post-Vibe' 



def strip_header():
    pair_hex = []
    rsp_ids = []
    for filename in glob.glob(os.path.join(path, '*.pkt')):    
        with open(os.path.join(os.getcwd(), filename), 'rb') as f:
            a = ["{:08b}".format(c) for c in f.read()] #Opens as hex
            b = a[90::264] #Remove 90B Header
            pair_hex.append(a)
            rsp_ids.append(b)
    #print (rsp_ids)
    print ('The number of files:', len(pair_hex))

    flatten_hex = [i for i in pair_hex for i in i]
    packet_num = (len(flatten_hex)//264)
    #print(packet_num)
    z = np.array_split(flatten_hex, packet_num)
    split_packets = []
    for x in z:
        y = (list(x[90::])) #Remove header
        #print('Packet without header',y)
        split_packets.append(y)
    print('Number of packets:', len(split_packets))
    #print('SPLITED PACKETS:', split_packets)
    #print('Binary Files:', split_packets)

    joined = []
    for a in split_packets:
        b = "".join(s for s in a)
        f = (list(m for m in b))
        #f = ["','".join(m for m in b)]
        joined.append(f)
    #print (joined)
    #print('Files processed', len(joined))

    burst_a = []
    burst_b = []
    for q in joined:
        a = (list(q[42:618]))
        

        b = (list(q[628:1204]))
        burst_a.append(a)
        burst_b.append(b)
    #print(burst_a)
    print("Burst Length A:",len(burst_a[0])//3//12)
    print("Burst Length B:",len(burst_b[0])//3//12)

    flatten_list = [i for i in split_packets for i in i]
    #print(flatten_list)
    joined = "".join(flatten_list)
    #print(flatten_list)
    listed = list(joined)
    print('Total bites in files:', len(listed))
    s = np.array_split(listed, 2)


    #Split into 16
    composite_list = [burst_a[x:x+16] for x in range(0, len(burst_a),16)]
    #print(composite_list)

strip_header()

def burst_data():
    pair_hex = []
    rsp_ids = []
    for filename in glob.glob(os.path.join(path, '*.pkt')):    
                with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                    a = ["{:02x}".format(c) for c in f.read()] #Opens as hex
                    b = a[90::264] #Remove 90B Header
                    pair_hex.append(a)
                    rsp_ids.append(b)
    print (rsp_ids)

#burst_data()
