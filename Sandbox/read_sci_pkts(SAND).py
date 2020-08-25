'''External modules'''
import glob 
import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

'''Directory'''
#path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM1/2020-07-30_INMS_Script_HVLite' #Good, Science 100pkts
path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM1/2020-07-30_INMS_Script_DITL_FM_6v1' #Good, Science 420pkts

'''Main class for extracting science data from pkts'''
class extractScience():
    '''Opens and prepares the files'''
    def openFiles(self):
        '''Opens all files in path as 8-bit'''
        all_files_binary = []
        resp_ids = []
        for filename in glob.glob(os.path.join(path, '*.pkt')):    
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                open_bits = list("{0:08b}".format(c) for c in f.read()) #Opens as hex
                open_resps = open_bits[90::264]
                filenames = os.path.basename(f.name) #Filenames

                all_files_binary.append(open_bits)
                resp_ids.append(open_resps)
        print ('File name:', filenames)
        print('Number of files:', len(all_files_binary))
        

        '''Determines the number of packets inside the different files'''
        flatten_binary = [i for j in all_files_binary for i in j]
        num_of_pkts = (len(flatten_binary)//264)
        print('Number of packets in files:', num_of_pkts)

        '''Prints the response id's with in a dictionary for ease of indexing'''
        '''IN DEVELOPMENT AS ID's NEED CONVERTING TO HEX'''
        #resp_index = list(range(0, len(flatten_binary)))
        #resp_flattened = [i for j in resp_ids for i in j]
        #resp_timestamp_dict = dict(zip(resp_index, resp_flattened))
        #print('Index + Response ID',resp_timestamp_dict)

        '''Extracts the pkt info ONLY'''
        pkt_size = np.array_split(flatten_binary, num_of_pkts)
        div_pkts = []
        for x in pkt_size:
            y = list(x[90::]) #CIRCE header is 90B. Change as necessary
            div_pkts.append(y)
        #print ('(Number of) packets without headers', (div_pkts))

        '''Extracts the header info ONLY (IN DEVELOPMENT)'''
        div_header = []
        for x in pkt_size:
            y = list(x[0:90]) #CIRCE header is 90B. Change as necessary
            div_header.append(y)
        #print ('Header information:', div_header)

        '''Identifies science pkts only'''
        self.sci_only = []
        for i in div_pkts:
            if i [0] == '00001000': #this is 08 in hex
                joined_pkts = "".join(j for j in i) #merge into single string
                relist_pkts = (list(j for j in joined_pkts)) #split into list
                self.sci_only.append(relist_pkts)
        #print ('Number of science pkts:', len(self.sci_only))

        self.checkforScience()

    '''Checks if there are science pkts'''
    def checkforScience(self):#
        if not self.sci_only:
            print('There are no science pkts')
        else:
            print ('Number of science pkts:', len(self.sci_only))
            self.extractScienceData()

    '''This function extracts the science data and plots into a histogram'''
    def extractScienceData(self):

        '''Get 12-bit integers from main burst groups'''
        def getIntegersFromBurstGroup(startIndex):
        
            burst = []
            for i in self.sci_only:  
                burst_index = i[(startIndex + 0):(startIndex + 192)] #12(bit) * 16(counts) = 192
                burst_join = str("".join(i for i in burst_index)) 
                burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)] #Creates 12-bit binary
                burst.append(burst_twelves)
                
            twelvebit_bigendian = []
            for j in burst:
                convert_to_int = [int(i,2) for i in j] #Converts to from 12-bit binary to integer
                twelvebit_bigendian.append(convert_to_int)
            
            '''Comment out print to remove numbers'''
            #print("Main Burst", twelvebit_bigendian)
            return(twelvebit_bigendian)
            

        '''Plot the data for the main burst groups'''
        def callGroupBurstData():

            '''Map the function to the index positions'''
            burst_0 = getIntegersFromBurstGroup(42)
            burst_1 = getIntegersFromBurstGroup(234)
            burst_2 = getIntegersFromBurstGroup(426)
            burst_0b = getIntegersFromBurstGroup(628)
            burst_1b = getIntegersFromBurstGroup(820)
            burst_2b = getIntegersFromBurstGroup(1012)


            '''Plot the data'''
            burst_group_data = burst_0 + burst_1 + burst_2 + burst_0b + burst_1b + burst_2b
            plt.hist(burst_group_data, bins = 75, alpha = 1)
            plt.title('DITL Energy, Burst Count 0-16, Groups 1-6')
            plt.xlabel('Energy (eV)')
            plt.ylabel('Counts')
            plt.show()

        callGroupBurstData()

        '''Get 12-bit integers from max burst groups'''
        def getIntegersFromBurstMax(startIndex):
            
            burst = []
            for i in self.sci_only:
                burst_index = i[(startIndex + 0):(startIndex + 36)] #12(bit) * 3(counts) = 36
                burst_join = str("".join(i for i in burst_index))
                burst_twelves = [burst_join[index:index+12] for index in range(0,len(burst_join),12)] #Creates 12-bit binary
                burst.append(burst_twelves)

            twelvebit_bigendian_max = []
            for j in burst:
                convert_to_int_max = [int(i,2) for i in j] #Converts to from 12-bit binary to integer
                twelvebit_bigendian_max.append(convert_to_int_max)
            
            '''Comment out print to remove numbers'''
            print('Burst Max',twelvebit_bigendian_max)
            return(twelvebit_bigendian_max)
            
        '''Plot the data for the max burst groups'''
        def callMaxBurstData():
            
            '''Map the function to the index positions'''
            burst_max_int_1 = getIntegersFromBurstMax(1214)
            burst_max_int_2 = getIntegersFromBurstMax(1260)
            burst_max_int_3 = getIntegersFromBurstMax(1306)
            burst_max_int_4 = getIntegersFromBurstMax(1352)

            burst_max_data = burst_max_int_1 + burst_max_int_2 + burst_max_int_3 + burst_max_int_4
        

            '''Extract specific data (IN DEVELOPMENT)'''
            #for i in burst_max_data:
            #    burst_max_single_data = i[0]
            #print (burst_max_single_data)

            '''Plot the data'''
            burst_max_hist = [i for j in burst_max_data for i in j] 
            burst_max_hist_no_zero = [i for j in burst_max_data for i in j if i != 0] #Flatten and remove zero values
            plt.hist(burst_max_hist, bins = 75, alpha = 1)
            
            #print('The number of 204 is:', burst_max_data.count(204))
            print('Number of all counts plotted:',len(burst_max_hist))
            print('Number of non-zero plotted:',len(burst_max_hist_no_zero))
       

            plt.title('HV-Lite 2020-07-30 \n payload_packets_20200730_151448.pkt\n  Bursts Count 0-3, Groups 1-4')
            plt.xlabel('Energy (eV)')
            plt.ylabel('Counts')
            plt.show()
        
        #callMaxBurstData()

'''Creates an instance of the class (an Object)'''     
go_science = extractScience()
go_science.openFiles()
