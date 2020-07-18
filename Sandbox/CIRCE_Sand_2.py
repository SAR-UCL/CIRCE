import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In'
#path = r'//Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/Post-Vibe' 

'''Opens all the files as 8bit'''
for filename in glob.glob(os.path.join(path, '*.pkt')):    
    with open(os.path.join(os.getcwd(), filename), 'rb') as f:
        open_bites = list("{:08b}".format(c) for c in f.read()) #Opens as hex
print('Total bites in:', len(open_bites))

'''Validates the open by dividing all packets into packet size'''
num_of_pkts = (len(open_bites)//264)
print('Number of packets:', num_of_pkts)

'''splits array into original packets'''
z = np.array_split(open_bites, num_of_pkts)
div_pkts = []
for x in z:
    y = list((x[90::]))
    div_pkts.append(y)
#print ('Packets without headers into arrays', div_pkts)

'''splits bits'''
split_pkts = []
for i in div_pkts:
    joined_pkts = "".join(j for j in i)
    relist_pkts = (list(j for j in joined_pkts))
    split_pkts.append(relist_pkts)
#print ('This the full 1392 bits per pkt', split_pkts)


''' First Group'''
burst_group_a = []
for i in split_pkts:
    skip_to_burst = (list(i[42:618]))
    burst_group_a.append(skip_to_burst)
#print('The first 42 bits have been removed',burst_group_a)

'''Burst 0'''
for i in burst_group_a:
    burst = i[0:192]
    burst_join = str("".join(i for i in burst))
    burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
#print('First Twelve Values', burst_twelves)
convert_to_int = [int(i,2) for i in burst_twelves]
print('Burst 0', convert_to_int)

'''Burst 1'''
for i in burst_group_a:
    burst = i[193:384]
    burst_join = str("".join(i for i in burst))
    burst_twelves_2 = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
#print('First Twelve Values', burst_twelves_2)
convert_to_int_1 = [int(i,2) for i in burst_twelves_2]
print('Burst 1', convert_to_int_1)

'''Burst 2'''
for i in burst_group_a:
    burst = i[385:576]
    burst_join = str("".join(i for i in burst))
    burst_twelves_3 = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
#print('First Twelve Values', burst_twelves_3)
convert_to_int_2 = [int(i,2) for i in burst_twelves_3]
print('Burst 2', convert_to_int_2)

'''Second Group'''
burst_group_b = []
for j in split_pkts:
    skip_to_burst = (list(j[628:1204]))
    burst_group_b.append(skip_to_burst)
#print('The first 42 bits have been removed',burst_group_a)

for i in burst_group_b:
    burst = i[0:192]
    burst_join = str("".join(i for i in burst))
    burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
#print('First Twelve Values', burst_twelves)
convert_to_int = [int(i,2) for i in burst_twelves]
print('Burst 0_b', convert_to_int)

'''Burst 1'''
for i in burst_group_b:
    burst = i[192:384]
    burst_join = str("".join(i for i in burst))
    burst_twelves_2 = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
#print('First Twelve Values', burst_twelves_2)
convert_to_int_1 = [int(i,2) for i in burst_twelves_2]
print('Burst 1_b', convert_to_int_1)

'''Burst 2'''
for i in burst_group_b:
    burst = i[385:576]
    burst_join = str("".join(i for i in burst))
    burst_twelves_3 = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
#print('Burst 2_b', burst_twelves_3)
convert_to_int_2 = [int(i,2) for i in burst_twelves_3]
print('Burst 2_b', convert_to_int_2)


