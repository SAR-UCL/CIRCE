import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In'
#path = r'//Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/Post-Vibe' 

'''Opens all the files as 8bit'''
for filename in glob.glob(os.path.join(path, '*.pkt')):    
    with open(os.path.join(os.getcwd(), filename), 'rb') as f:
        open_bits = list("{:08b}".format(c) for c in f.read()) #Opens as hex
#print('Total bites in:', len(open_bites))

'''Prints the number of packets inside the files'''
num_of_pkts = (len(open_bits)//264)
print('Number of packets:', num_of_pkts)

'''Splits array into original packets'''
z = np.array_split(open_bits, num_of_pkts)
div_pkts = []
for x in z:
    y = list((x[90::])) #Removes the 90byte header (will need at later date)
    div_pkts.append(y)
#print ('Packets without headers into arrays', div_pkts)

'''Splits into single bits'''
split_pkts = []
for i in div_pkts:
    joined_pkts = "".join(j for j in i)
    relist_pkts = (list(j for j in joined_pkts))
    split_pkts.append(relist_pkts)

def extractBurstMain():

    def getIndexFromBurstGroup(startIndex):
        burst_group = []
        for i in split_pkts:
            burst_index = i[(startIndex + 0):(startIndex + 192)]
            burst_group.append(burst_index)
        return burst_group

    burst_0 = getIndexFromBurstGroup(42)
    burst_1 = getIndexFromBurstGroup(234)
    burst_2 = getIndexFromBurstGroup(426)
    burst_0b = getIndexFromBurstGroup(628)
    burst_1b = getIndexFromBurstGroup(820)
    burst_2b = getIndexFromBurstGroup(1012)

    def getIntegersFromBurstGroup(burst_group):
        burst = []
        for i in burst_group:
            burst_index = i[0:192]
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
            burst.append(burst_twelves)
            convert_to_int = [int(i,2) for j in burst for i in j]
        return convert_to_int

    burst_0_int = getIntegersFromBurstGroup(burst_0)
    burst_1_int = getIntegersFromBurstGroup(burst_1)
    burst_2_int = getIntegersFromBurstGroup(burst_2)
    burst_0b_int = getIntegersFromBurstGroup(burst_0b)
    burst_1b_int = getIntegersFromBurstGroup(burst_1b)
    burst_2b_int = getIntegersFromBurstGroup(burst_2b)

    print('Burst old', burst_1_int)

    def getIntegersFromBurstGroup2(startIndex):
        burst = []
        for i in split_pkts:
            burst_index = i[(startIndex + 0):(startIndex + 192)]
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
            burst.append(burst_twelves)
            convert_to_int = [int(i,2) for j in burst for i in j]
        return convert_to_int
    
    burst_0 = getIntegersFromBurstGroup2(42)
    burst_1 = getIntegersFromBurstGroup2(234)
    burst_2 = getIntegersFromBurstGroup2(426)
    burst_0b = getIntegersFromBurstGroup2(628)
    burst_1b = getIntegersFromBurstGroup2(820)
    burst_2b = getIntegersFromBurstGroup2(1012)
    print('Burst new', burst_test)

extractBurstMain()

def extractBurstMaximum():
    
    def getIndexFromBurstMax(startIndex):
        burst_max = []
        for i in split_pkts:
            burst_max_index = i[(startIndex + 0):(startIndex + 36)]
            burst_max.append(burst_max_index)
        return burst_max

    burst_max_1 = getIndexFromBurstMax(1214)
    burst_max_2 = getIndexFromBurstMax(1260)
    burst_max_3 = getIndexFromBurstMax(1306)
    burst_max_4 = getIndexFromBurstMax(1352)
    
    def getIntegersFromBurstMax(burst_group):
        burst = []
        for i in burst_group:
            burst_index = i[0:36]
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
            burst.append(burst_twelves)
            convert_to_int_max = [int(i,2) for j in burst for i in j]
        return convert_to_int_max

    burst_max_int_1 = getIntegersFromBurstMax(burst_max_1)
    burst_max_int_2 = getIntegersFromBurstMax(burst_max_2)
    burst_max_int_3 = getIntegersFromBurstMax(burst_max_3)
    burst_max_int_4 = getIntegersFromBurstMax(burst_max_4)

    print ('Burst Maximum 1 (Function)', burst_max_int_4)

extractBurstMaximum()


