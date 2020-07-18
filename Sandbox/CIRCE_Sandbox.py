'''External modules'''
import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In'
#path = r'//Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/Post-Vibe' 

#hexy = ['1', 'a', '05']
#hexy = ['1a05']
#hexy = ['0e0', '000', '000']
biny = ['010011101011']
hexy = hex(int('010011101011',2))
print (hexy)
#endiann = [int(h, 16) for h in hexy]
#print(endiann)



def hex_header():
    pair_hex = []
    for filename in glob.glob(os.path.join(path, '*.pkt')):    
        with open(os.path.join(os.getcwd(), filename), 'rb') as f:
            a = ["{:02x}".format(c) for c in f.read()] #Opens as hex
            pair_hex.append(a)
    #print (pair_hex)
    #print(len(pair_hex))

    flatten_hex = [i for i in pair_hex for i in i]
    packet_num = (len(flatten_hex)//264)
    z = np.array_split(flatten_hex, packet_num)
    split_packets = []
    for x in z:
        y = (list(x[90::])) #Remove header
        #print('Packet without header',y)
        split_packets.append(y)
    print('Number of packets:', len(split_packets))

    joined = []
    for a in split_packets:
        b = "".join(s for s in a)
        f = (list(m for m in b))
        #f = ["','".join(m for m in b)]
        joined.append(f)
    print ('Im pre split', joined)
    print('Pre split length:', len(joined[0]))

    burst_a = []
    burst_b = []
    for q in joined:
        #a = (list(q[42:618]))
        a = (list(q[11:153]))
        a_0 = a[0:192]
        a_0_joined = str("".join(s for s in a_0))
        split_strings = [a_0_joined[index : index + 3] for index in range(0, len(a_0_joined), 3)]
        burst_a.append(split_strings)
    print (burst_a)
    print(len(burst_a[0]))
    #print(len(burst_a[0]))

    flattened_burst = [i for i in burst_a for i in i]
    endian = [int(h, 16) for h in flattened_burst]
    print(endian)
    print(len(endian))
    resplit = np.array_split(endian, 2)
    x = (list(resplit))
    print(len(x[1])//16)
    #print(x)

#hex_header()

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
        a_0 = a[0:192]
        a_0_joined = str("".join(s for s in a_0))
        #split_strings = list([a_0_joined[index : index + 12] for index in range(0, len(a_0_joined), 12)])
        split_strings = [a_0_joined[index : index + 12] for index in range(0, len(a_0_joined), 12)]
        #hex_convert = (int(str(split_strings),12))
        endian = [int(h, 12) for h in split_strings]
        #big_endian = int.from_bytes(12, 'big')
        #big_endian = int.from_bytes([int(h for h in split_strings)], 'big')

        a_1 = a[192:384]
        a_2 = a[384:576]

        b = (list(q[628:1204]))

        burst_a.append(a)
        burst_b.append(b)

    #print(burst_a)
    #print(burst_a)
    #print('Burst A_0', a_0, 'Burst A_1', a_1, 'Burst A_2', a_2)
    
    print (split_strings)
    print(endian)

    flatten_list = [i for i in split_packets for i in i]
    #print(flatten_list)
    joined = "".join(flatten_list)
    #print(flatten_list)
    listed = list(joined)
    print('Total bites in files:', len(listed))
    s = np.array_split(listed, 8)


    #Split into 16
    composite_list = [burst_a[x:x+16] for x in range(0, len(burst_a),16)]
    #print(composite_list)

#strip_header()

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
