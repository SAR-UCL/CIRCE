import glob
import os
import numpy as np
from matplotlib import pyplot as plt

path = '/Users/SAR/Desktop/CIRCE/Testing/Responses/post-vibe'
pair_hex = []
rsp_ids = []
for filename in glob.glob(os.path.join(path, '*.pkt')):    
    with open(os.path.join(os.getcwd(), filename), 'rb') as f:
        a = ["{:02x}".format(c) for c in f.read()]
        b = a[90::264]
        pair_hex.append(a)
        rsp_ids.append(b)

print("Number of files:", len(pair_hex))
print("List of ID's", rsp_ids)

flatten_hex = [item for items in pair_hex for item in items]
packet_num = (len(flatten_hex)//(90+174))
print("Number of packets in files:", packet_num)

#print(flatten_hex)
#print(len(flatten_hex))


#Takes the entire array and divides it based on the number of packets. 
#This results in lots of lists each 174 in length
#https://kite.com/python/answers/how-to-split-a-list-into-n-parts-in-python
#four_split = np.array_split(pair_hex[0], packet_num)
four_split = np.array_split(flatten_hex, packet_num)
p_list = []
for array in four_split:
    new_array = (list(array[90::]))
    p_list.append(new_array)
#print(p_list)
#print(len(p_list))


list_a = []
for i in p_list:
    if i[0] == '04':
        #print (i[2::])
        #print(len(i))
        new_v = i[2::]
        list_a.append(new_v)
#print(len(list_a))
#print(list_a)


flatten = [item for items in list_a for item in items]
print(len(flatten))
endian_pairs = [i+j for i,j in zip(flatten[::2], flatten[1::2])] #pairs into groups of four
endian = [int(h[2:4] + h[0:2], 16) for h in endian_pairs] #swap the halves and convert to Little Endian UINT16
#print(len(endian))
print ("Total Packets:", packet_num, ", Packets In:", len(list_a), ", Packets Processed:", (len(endian)//172))

data = endian
        
#plt.ylim([min(data)-5, max(data)-63000])
#plt.xlim([min(data)+100, max(data)-62000])
plt.hist(data, bins=10, alpha=0.5)

#plt.title('STIM Packet, Count Distribution')
plt.xlabel('Time')
plt.ylabel('Count')

#plt.show()

'''
try:
    plt.savefig("CIRCE_figs/STIM-04_FM1-2_b800.png", bbox_inches='tight')
    print ("File saved")
except IOError:
    print ("File creation failed")
'''
