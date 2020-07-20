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
        #skip_to_burst = (list(i[42:618]))
        skip_to_burst = i[42:618]
        burst_group_a.append(skip_to_burst)
    #print('The first 42 bits have been removed',burst_group_a)

    '''Burst 0'''
    joined_pkts = []
    for i in burst_group_a:
        burst = i[0:192]
        burst_join_1 = str("".join(i for i in burst))
        relist_pkts = (list(j for j in burst_join_1))
        joined_pkts.append(relist_pkts)
        
        burst_twelves = [joined_pkts[index:index+12] for index in range(0,len(joined_pkts),12)] #Rejoins as a twelve bit int
        #burst_twelves = [burst_join_1[index:index+12] for index in range(0,len(burst_join_1),12)] #Rejoins as a twelve bit int
    
    print('Burst Joined Length',burst_twelves)
    #print('First Twelve Values', burst_twelves)
    #convert_to_int_1 = [int(i,2) for i in burst_twelves]
    #convert_to_int_1 = [int(i,2) for i in burst_twelves]
    for y in burst_twelves:
        for x in y:
            convert_to_int_1 = [int(str(x),2)]
    print('Burst 0', convert_to_int_1)

    '''Burst 1'''
    for i in burst_group_a:
        burst = i[193:384]
        burst_join_2 = str("".join(i for i in burst))
        burst_twelves_2 = [burst_join_2[index:index+12] for index in range(0,len(burst_join_2),12)]
    #print('First Twelve Values', burst_twelves_2)
    convert_to_int_2 = [int(i,2) for i in burst_twelves_2]
    #print('Burst 1', convert_to_int_2)

    '''Burst 2'''
    for i in burst_group_a:
        burst = i[385:576]
        burst_join_3 = str("".join(i for i in burst))
        burst_twelves_3 = [burst_join_3[index:index+12] for index in range(0,len(burst_join_3),12)]
    #print('First Twelve Values', burst_twelves_3)
    convert_to_int_3 = [int(i,2) for i in burst_twelves_3]
    #print('Burst 2', convert_to_int_3)

    '''Second Group'''
    burst_group_b = []
    for j in split_pkts:
        skip_to_burst_2 = (list(j[628:1204]))
        burst_group_b.append(skip_to_burst_2)
    #print('The first 42 bits have been removed',burst_group_a)

    for i in burst_group_b:
        burst = i[0:192]
        burst_join_4 = str("".join(i for i in burst))
        burst_twelves_4 = [burst_join_4[index:index+12] for index in range(0,len(burst_join_4),12)]
    #print('First Twelve Values', burst_twelves_4)
    convert_to_int_4 = [int(i,2) for i in burst_twelves_4]
    #print('Burst 0_b', convert_to_int_4)

    '''Burst 1'''
    for i in burst_group_b:
        burst = i[192:384]
        burst_join_5 = str("".join(i for i in burst))
        burst_twelves_5 = [burst_join_5[index:index+12] for index in range(0,len(burst_join_5),12)]
    #print('First Twelve Values', burst_twelves_5)
    convert_to_int_5 = [int(i,2) for i in burst_twelves_5]
    #print('Burst 1_b', convert_to_int_5)

    '''Burst 2'''
    for i in burst_group_b:
        burst = i[385:576]
        burst_join_6 = str("".join(i for i in burst))
        burst_twelves_6 = [burst_join_6[index:index+12] for index in range(0,len(burst_join_6),12)]
    #print('Burst 2_b', burst_twelves_6)
    convert_to_int_6 = [int(i,2) for i in burst_twelves_6]
    #print('Burst 2_b', convert_to_int_6)


    '''Plot the data'''
    #sci_data = convert_to_int_1 + convert_to_int_2 + convert_to_int_3 + convert_to_int_4 + convert_to_int_5 + convert_to_int_5 

    #plt.hist(sci_data, bins = 10000)
    #plt.xlabel ('Energy')
    #plt.ylabel ('Counts')

extract_burst_main()

def extract_burst_maximum():
    
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