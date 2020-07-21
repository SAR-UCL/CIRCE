import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In'
#path = r'//Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/Post-Vibe' 

'''Opens all the files as 8bit'''
all_files_binary = []
for filename in glob.glob(os.path.join(path, '*.pkt')):    
    with open(os.path.join(os.getcwd(), filename), 'rb') as f:
        open_bits = list("{0:08b}".format(c) for c in f.read()) #Opens as hex
        all_files_binary.append(open_bits)
#print('Total bites in:', len(open_bits))
print('Total files in:', len(all_files_binary))

'''Prints the number of packets inside the files'''
#num_of_pkts_OLD = (len(open_bits)//264)
#print('Number of packets:', num_of_pkts_OLD)

flatten_binary = [i for j in all_files_binary for i in j]
num_of_pkts = (len(flatten_binary)//264)
print('Number of packets:', num_of_pkts)

'''Splits array into original packets'''
#z = np.array_split(open_bits, num_of_pkts)
pkt_size = np.array_split(flatten_binary, num_of_pkts)
div_pkts = []
for x in pkt_size:
    y = list((x[90::])) #Removes the 90byte header (will need at later date)
    div_pkts.append(y)
#print ('Packets without headers into arrays', div_pkts)

'''Splits into single bits'''
split_pkts = []
for i in div_pkts:
    joined_pkts = "".join(j for j in i)
    relist_pkts = (list(j for j in joined_pkts))
    split_pkts.append(relist_pkts) 

'''at the end of split_pkts, we have the correct number of lists'''


def getIntegersFromBurstGroup(startIndex):

    burst = []
    for i in split_pkts:     
        burst_index = i[(startIndex + 0):(startIndex + 192)]
        burst_join = str("".join(i for i in burst_index)) 
        burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
        burst.append(burst_twelves)
        #convert_to_int = [int(i,2) for j in burst for i in j]
        
    twelvebit_bigendian = []
    for j in burst:
        convert_to_int = [int(i,2) for i in j]
        twelvebit_bigendian.append(convert_to_int)

    #return(twelvebit_bigendian)
    print(twelvebit_bigendian)


burst_0 = getIntegersFromBurstGroup(42)
burst_1 = getIntegersFromBurstGroup(234)
burst_2 = getIntegersFromBurstGroup(426)
burst_0b = getIntegersFromBurstGroup(628)
burst_1b = getIntegersFromBurstGroup(820)
burst_2b = getIntegersFromBurstGroup(1012)


def getIntegersFromBurstMax(startIndex):
    
    burst = []
    for i in split_pkts:
        burst_index = i[(startIndex + 0):(startIndex + 36)]
        burst_join = str("".join(i for i in burst_index))
        burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
        burst.append(burst_twelves)
        convert_to_int_max = [int(i,2) for j in burst for i in j]

    twelvebit_bigendian_max = []
    for j in burst:
        convert_to_int_max = [int(i,2) for i in j]
        twelvebit_bigendian_max.append(convert_to_int_max)

    #return(twelvebit_bigendian)
    print(twelvebit_bigendian_max)

burst_max_int_1 = getIntegersFromBurstMax(1214)
burst_max_int_2 = getIntegersFromBurstMax(1260)
burst_max_int_3 = getIntegersFromBurstMax(1306)
burst_max_int_4 = getIntegersFromBurstMax(1352)



