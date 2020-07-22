import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

#path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In'
path = r'//Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/EM1/08' 

'''Opens all files in path as 8-bit'''
all_files_binary = []
resp_ids = []
for filename in glob.glob(os.path.join(path, '*.pkt')):    
    with open(os.path.join(os.getcwd(), filename), 'rb') as f:
        open_bits = list("{0:08b}".format(c) for c in f.read()) #Opens as hex
        open_resps = open_bits[90::264]
        all_files_binary.append(open_bits)
        resp_ids.append(open_resps)
print('Number of files:', len(all_files_binary))
print('Different IDs are:', resp_ids)

'''Determines the number of packets inside the different files'''
flatten_binary = [i for j in all_files_binary for i in j]
num_of_pkts = (len(flatten_binary)//264)
print('Number of packets in files:', num_of_pkts)

'''Places packets into an np array and removes the header'''
pkt_size = np.array_split(flatten_binary, num_of_pkts)
div_pkts = []
for x in pkt_size:
    y = list((x[90::])) #CIRCE header is 90Bytes. Change as necessary
    div_pkts.append(y)
#print ('Packets without headers into arrays', div_pkts)

'''
sci_only = []
for j in div_pkts:
    if j [0] == '00001001':
        crop_sci = j[4::] #Remove id, seq count, i_ion and v_pk 
    
Splits pkts into individual bits (01b)
split_pkts = []
for i in div_pkts:
    joined_pkts = "".join(j for j in i)
    relist_pkts = (list(j for j in joined_pkts))
    split_pkts.append(relist_pkts)''' 

sci_only = []
for i in div_pkts:
    if i [0] == '00001001':
        joined_pkts = "".join(j for j in i)
        relist_pkts = (list(j for j in joined_pkts))
        sci_only.append(relist_pkts)
       
def extractScienceData():

    '''Get 12-bit integers from main burst groups'''
    def getIntegersFromBurstGroup(startIndex):

        burst = []
        for i in sci_only:  
        #for i in split_pkts:     
            burst_index = i[(startIndex + 0):(startIndex + 192)] #12(bit) * 16(counts) = 192
            burst_join = str("".join(i for i in burst_index)) 
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)] #Creates 12-bit binary
            burst.append(burst_twelves)
            
        twelvebit_bigendian = []
        for j in burst:
            convert_to_int = [int(i,2) for i in j] #Converts to from 12-bit binary to integer
            twelvebit_bigendian.append(convert_to_int)
        
        #print(twelvebit_bigendian)
        return(twelvebit_bigendian)
        

    '''Plot the data for the main burst groups'''
    def plotGroupBurstData():

        '''Map the function to the index positions'''
        burst_0 = getIntegersFromBurstGroup(42)
        burst_1 = getIntegersFromBurstGroup(234)
        burst_2 = getIntegersFromBurstGroup(426)
        burst_0b = getIntegersFromBurstGroup(628)
        burst_1b = getIntegersFromBurstGroup(820)
        burst_2b = getIntegersFromBurstGroup(1012)

        '''Plot the data'''
        burst_group_data = burst_0 + burst_1 + burst_2 + burst_0b + burst_1b + burst_2b
        burst_group_hist = [i for j in burst_group_data for i in j] #needs to be flattened
        plt.hist(burst_group_hist, bins = 75, alpha = 1)

        plt.title('O+ Energy, Main Burst 0-16, Groups 1-6')
        plt.xlabel('Energy')
        plt.ylabel('Count')
        plt.show()

    #plotGroupBurstData()

    '''Get 12-bit integers from max burst groups'''
    def getIntegersFromBurstMax(startIndex):
        
        burst = []
        #for i in split_pkts:
        for i in sci_only:
            burst_index = i[(startIndex + 0):(startIndex + 36)] #12(bit) * 3(counts) = 36
            burst_join = str("".join(i for i in burst_index))
            burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)] #Creates 12-bit binary
            burst.append(burst_twelves)

        twelvebit_bigendian_max = []
        for j in burst:
            convert_to_int_max = [int(i,2) for i in j] #Converts to from 12-bit binary to integer
            twelvebit_bigendian_max.append(convert_to_int_max)

        print(twelvebit_bigendian_max)
        return(twelvebit_bigendian_max)
        
    '''Plot the data for the max burst groups'''
    def plotMaxBurstData():

        burst_max_int_1 = getIntegersFromBurstMax(1214)
        burst_max_int_2 = getIntegersFromBurstMax(1260)
        burst_max_int_3 = getIntegersFromBurstMax(1306)
        burst_max_int_4 = getIntegersFromBurstMax(1352)

        '''Plot the data (In development)'''
        burst_max_data = burst_max_int_1 + burst_max_int_2 + burst_max_int_3 + burst_max_int_4

        burst_max_hist = [i for j in burst_max_data for i in j]
        plt.hist(burst_max_hist, bins = 75, alpha = 1)

        plt.title('O+ Energy, Max Counts 0-3, Groups 1-4')
        plt.xlabel('Energy')
        plt.ylabel('Count')
        plt.show()

    plotMaxBurstData()

extractScienceData()