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

'''splits array into original packets'''
z = np.array_split(open_bits, num_of_pkts)
div_pkts = []
for x in z:
    y = list((x[90::])) #Removes the 90byte header (will need at later date)
    div_pkts.append(y)
#print ('Packets without headers into arrays', div_pkts)

'''splits into single bits'''
split_pkts = []
for i in div_pkts:
    joined_pkts = "".join(j for j in i)
    relist_pkts = (list(j for j in joined_pkts))
    split_pkts.append(relist_pkts)

def extract_burst_main():
    
    ''' First Group'''
    burst_group_a = []
    for i in split_pkts:
        skip_to_burst = i[42:618]
        burst_group_a.append(skip_to_burst)

    '''Second Group'''
    burst_group_b = []
    for j in split_pkts:
        skip_to_burst_2 = (list(j[628:1204]))
        burst_group_b.append(skip_to_burst_2)

    def getIntegersFromBurstGroup(burst_group, startIndex):
        burst = []
        for i in burst_group:
            burst_index = i[(startIndex + 0):(startIndex + 192)]
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
            burst.append(burst_twelves)
            convert_to_int = [int(i,2) for j in burst for i in j]
        return convert_to_int

    burst_0 = getIntegersFromBurstGroup(burst_group_a, 0)
    burst_1 = getIntegersFromBurstGroup(burst_group_a, 193)
    burst_2 = getIntegersFromBurstGroup(burst_group_a, 385)

    burst_0b = getIntegersFromBurstGroup(burst_group_b, 0)
    burst_1b = getIntegersFromBurstGroup(burst_group_b, 193)
    burst_2b = getIntegersFromBurstGroup(burst_group_b, 385)

extract_burst_main()

def extract_burst_maximum():
    
    def getIntegersFromBurstMax(startIndex):
        burst_max = []
        for i in split_pkts:
            burst_max_index = i[(startIndex + 0):(startIndex + 36)]
            burst_max.append(burst_max_index)
        return burst_max

    burst_max_1 = getIntegersFromBurstMax(1214)
    burst_max_2 = getIntegersFromBurstMax(1260)
    burst_max_3 = getIntegersFromBurstMax(1306)
    burst_max_4 = getIntegersFromBurstMax(1352)
    
    def getIntegersFromBurstMax(burst_group):
        burst = []
        for i in burst_group:
            burst_index = i[0:36]
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
            burst.append(burst_twelves)
            convert_to_int = [int(i,2) for j in burst for i in j]
        return convert_to_int

    burst_max_int_1 = getIntegersFromBurstMax(burst_max_1)
    burst_max_int_2 = getIntegersFromBurstMax(burst_max_2)
    burst_max_int_3 = getIntegersFromBurstMax(burst_max_3)
    burst_max_int_4 = getIntegersFromBurstMax(burst_max_4)

    print ('Burst Maximum 1 (Function)', burst_max_int_4)

    '''
    def getIntegersFromBurstMax22(burst_group, startIndex):
        burst = []
        for i in burst_group:
            burst_index = i[(startIndex + 0):(startIndex + 36)]
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)]
            burst.append(burst_twelves)
            convert_to_int = [int(i,2) for j in burst for i in j]
        return convert_to_int
    '''

    burst_maximum_1 = []
    burst_maximum_2 = []
    burst_maximum_3 = []
    burst_maximum_4 = []
    
    for i in split_pkts:
        skip_to_burst = (list(i[1214:1250]))
        skip_to_burst_2 = (list(i[1260:1296]))
        skip_to_burst_3 = (list(i[1306:1342]))
        skip_to_burst_4 = (list(i[1352:1388]))
        
        burst_maximum_1.append(skip_to_burst)
        burst_maximum_2.append(skip_to_burst_2)
        burst_maximum_3.append(skip_to_burst_3)
        burst_maximum_4.append(skip_to_burst_4)

    for i in burst_maximum_1:
        burst = i[0:36]
        burst_join = str("".join(i for i in burst))
        burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)] #Rejoins as a twelve bit int
    #print('Binary Burst Maximum 1', burst_twelves)
    convert_to_int = [int(i,2) for i in burst_twelves]
    print('Burst Maximum 1', convert_to_int)

    for i in burst_maximum_2:
        burst = i[0:36]
        burst_join_2 = str("".join(i for i in burst))
        burst_twelves_2 = [burst_join_2[index:index+12] for index in range(0,len(burst_join_2),12)] #Rejoins as a twelve bit int
    #print('Binary Burst Maximum 2', burst_twelves_2)
    convert_to_int_2 = [int(i,2) for i in burst_twelves_2]
    print('Burst Maximum 2', convert_to_int_2)

    for i in burst_maximum_3:
        burst = i[0:36]
        burst_join_3 = str("".join(i for i in burst))
        burst_twelves_3 = [burst_join_3[index:index+12] for index in range(0,len(burst_join_3),12)] #Rejoins as a twelve bit int
    #print('Binary Burst Maximum 3', burst_twelves_3)
    convert_to_int_3 = [int(i,2) for i in burst_twelves_3]
    print('Burst Maximum 3', convert_to_int_3)

    for i in burst_maximum_4:
        burst = i[0:36]
        burst_join_4 = str("".join(i for i in burst))
        burst_twelves_4 = [burst_join_4[index:index+12] for index in range(0,len(burst_join_4),12)] #Rejoins as a twelve bit int
    #print('Binary Burst Maximum 4', burst_twelves_4)
    convert_to_int_4 = [int(i,2) for i in burst_twelves_4]
    print('Burst Maximum 4', convert_to_int_4)

extract_burst_maximum()


