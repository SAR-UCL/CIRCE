'''External modules'''
import glob 
import os 
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

'''Set directory'''
path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM1/2020-07-30_INMS_Script_HVLite' #Good, Science 100pkts
#path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM1/2020-07-30_INMS_Script_DITL_FM_6v1' #Good, Science 420pkts

'''Class for extracting science data from pkts'''
class extractScience():
    '''Opens and prepares the files'''
    def openFiles(self):
        global pkt_filename
        '''Opens all files in path as 8-bit'''
        all_files_binary = []
        resp_ids = []
        for filename in glob.glob(os.path.join(path, '*.pkt')):    
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                open_bits = list("{0:08b}".format(c) for c in f.read()) #Opens as hex
                open_resps = open_bits[90::264]
                pkt_filename = os.path.basename(f.name) #pkt_filename

                all_files_binary.append(open_bits)
                resp_ids.append(open_resps)
        print('Number of files:', len(all_files_binary))
        #print('List of response ids:', resp_ids)

        '''Prints the file name for validation'''
        print ('File name:', pkt_filename)

        '''Determines the number of packets inside the different files'''
        flatten_binary = [i for j in all_files_binary for i in j]
        num_of_pkts = (len(flatten_binary)//264)
        print('Number of packets in files:', num_of_pkts)

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
    def checkforScience(self):
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
            #return(twelvebit_bigendian)
            return ([a for b in twelvebit_bigendian for a in b]) #flattens out results
        
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
            #print('Burst Max',twelvebit_bigendian_max)
            #return(twelvebit_bigendian_max)
            return ([a for b in twelvebit_bigendian_max for a in b]) #flattens out results
            

        ''''Gets the burst data for both the groups and maximums'''
        def getBurstData():
            global extracted_filename

            '''Map the function to the index positions'''
            nb_0 = getIntegersFromBurstGroup(42)
            nb_1 = getIntegersFromBurstGroup(234)
            nb_2 = getIntegersFromBurstGroup(426)
            ib_0 = getIntegersFromBurstGroup(628)
            ib_1 = getIntegersFromBurstGroup(820)
            ib_2 = getIntegersFromBurstGroup(1012)

            nbm_1 = getIntegersFromBurstMax(1214)
            ibm_1 = getIntegersFromBurstMax(1260)
            nbm_2 = getIntegersFromBurstMax(1306)
            ibm_2 = getIntegersFromBurstMax(1352)

            '''Convert to Panda Dataframes'''
            group_burst_data = {'nb0':nb_0,'nb1':nb_1,'nb2':nb_2,'ib0':ib_0,'ib1':ib_1,'ib2':ib_2}
            max_burst_data = {'nbm1':nbm_1,'ibm1':ibm_1,'nbm2':nbm_2,'ibm2':ibm_2}
            groupBurstPandaConv = pd.DataFrame(group_burst_data)
            maxBurstPandaConv = pd.DataFrame(max_burst_data)
            
            #groupBurstPandaConv = pd.DataFrame()
            #groupBurstPandaConv ["Burst 0"] = burst_0 #if flattened
            #groupBurstPandaConv ["Burst 1"] = burst_1 #if flattened 

            #groupBurstPandaConv ["Burst 0"] = [a for b in burst_0 for a in b]
            #groupBurstPandaConv ["Burst 1"] = [a for b in burst_1 for a in b]
            #groupBurstPandaConv ["Burst 2"] = [a for b in burst_2 for a in b]
            #groupBurstPandaConv ["Burst 0b"] = [a for b in burst_0b for a in b]
            #groupBurstPandaConv ["Burst 1b"] = [a for b in burst_1b for a in b]
            #groupBurstPandaConv ["Burst 2b"] = [a for b in burst_2b for a in b]

            #maxBurstPandaConv = pd.DataFrame()
            #maxBurstPandaConv ["Burst Max 0"] = [a for b in burst_max_int_1 for a in b]
            #maxBurstPandaConv ["Burst Max 1"] = [a for b in burst_max_int_2 for a in b]
            #maxBurstPandaConv ["Burst Max 2"] = [a for b in burst_max_int_3 for a in b]
            #maxBurstPandaConv ["Burst Max 3"] = [a for b in burst_max_int_4 for a in b]
            
            '''Merge dataframes and export as .csv'''
            merge_burst_data = pd.concat([groupBurstPandaConv, maxBurstPandaConv], axis=1)
            extracted_filename = path + "/" + pkt_filename[:-4] + ".csv" # -4 removes '.pktß'
            merge_burst_data.to_csv(extracted_filename, index = False, header = True)
            #print ("Exported burst csv data: \n", merge_burst_data)

        getBurstData()
            
'''Class for plotting science data from extractScience() class'''     
class visualiseScience():
    
    load_science = extractScience()
    load_science.openFiles()

    #burst_cats = ['Neut Burst 0','Neut Burst 1','Neut Burst 2','Ion Burst 0', 'Ion Burst 1', 'Ion Burst 2', 'Neut Max 1', 'Ion Max 1','Neut Max 2','Ion Max 2']
    #load_burst_csv_data = pd.read_csv(extracted_filename, names = burst_cats, skiprows=1)
    load_burst_csv_data = pd.read_csv(extracted_filename)
    #print('Imported burst csv data: \n', load_burst_csv_data)

    sci_pkt_hist = load_burst_csv_data['nb0']

    plt.hist(sci_pkt_hist, bins = 75, alpha = 1)
    plt.title('DITL Energy, Burst Count 0-16, Groups 1-6')
    plt.xlabel('Energy (eV)')
    plt.ylabel('Counts')
    plt.show()


go_science = visualiseScience()
