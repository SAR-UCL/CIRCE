'''External modules'''
import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt
import datetime

'''Directory testing from 29-07-20 in response to DSTL and BCT'''
#path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM1/2020-07-30_INMS_Script_HVLite' #Good, Science 100pkts
#path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM1/2020-07-30_INMS_Script_DITL_FM_6v1' #Good, Science 420pkts
path = r'/Users/SAR/OneDrive - University College London/PhD/CIRCE/TVAC/FM2/BCT-INMS FM2 Post Rework Functional - 21 Aug 2020/07_INMS' 


'''This class extracts the packets from the files and prepares them for reading'''
class GetPackets():

    def load_packets(self):
        self.pair_hex = []
        self.rsp_ids = []
        for filename in glob.glob(os.path.join(path, '*.pkt')):    
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                a = ["{:02x}".format(c) for c in f.read()] #Opens as hex
                b = a[90::264] #Remove 90B Header
                #b = a[30::204] #Remove 30B Header
                self.filenames = os.path.basename(f.name) #Print all filenames (Not working yet)
                self.pair_hex.append(a)
                self.rsp_ids.append(b)
        #print ('Packet responses in order of appearance:',self.rsp_ids) #prints responce ID's in order
        self.prepare_packets()

    def prepare_packets(self):
        flatten_hex = [item for items in self.pair_hex for item in items]
        self.packet_num = (len(flatten_hex)//(90+174))
        #self.packet_num = (len(flatten_hex)//(30+174))
        z = np.array_split(flatten_hex, self.packet_num) 
        self.split_packets = []
        for x in z:
            y = (list(x[90::])) #Remove 90B Header
            self.split_packets.append(y)
        #print (self.split_packets)
        

'''This class identifies the number and different types of packets'''
class PacketInfo():

    def basic_info(self):
        info_s = GetPackets() #call GetPackets class
        info_s.load_packets()

        print("Filename:", info_s.filenames)
        print("Number of files:", len(info_s.pair_hex))
        print("Number of packets in files:", info_s.packet_num)

        self.identify_packets()

    ''' Check for the number and type of packet outputs'''
    def identify_packets(self):

        info_s = GetPackets() #call GetPackets class
        info_s.load_packets()

        flattened_rsp = [item for items in info_s.rsp_ids for item in items]
        #print ("Number of different packets:")
        if any('04' in s for s in flattened_rsp):
            print("Stimulation packets (04):", flattened_rsp.count('04'))
        if any('06' in s for s in flattened_rsp):
            print("Health check packets (06):", flattened_rsp.count('06'))
        if any('07' in s for s in flattened_rsp):
            print("Calibration packets (07):", flattened_rsp.count('07'))
        if any('08' in s for s in flattened_rsp):
            print("Science packets (08):", flattened_rsp.count('08'))
        if any('09' in s for s in flattened_rsp):
            print("House keeping packets (09):", flattened_rsp.count('09'))
        if any('0a' in s for s in flattened_rsp):
            print("Stm packets (0a):", flattened_rsp.count('0a'))
        if any('0b' in s for s in flattened_rsp):
            print("Dump packets (0b):", flattened_rsp.count('0b'))
        if any('bb' in s for s in flattened_rsp):
            print ("Error packets (bb):", flattened_rsp.count('bb'))
        if any('fa' in s for s in flattened_rsp):
            print ("OBC error packets (fa):", flattened_rsp.count('fa'))
        print ('\n')

        '''Order of response IDs'''
        index_rsps = list(range(0,len(flattened_rsp)))
        dict_rsp = dict(zip(index_rsps, flattened_rsp))
        print('Response ID order + Index:', dict_rsp)

'''Creates an instance of the class (an Object)'''      
go_pkt_info = PacketInfo()
go_pkt_info.basic_info()

def getTimeStamps():
    
    '''opens the files and prepares them for reading'''
    pair_hex = []
    rsp_ids = []
    for filename in glob.glob(os.path.join(path, '*.pkt')):    
        with open(os.path.join(os.getcwd(), filename), 'rb') as f:
            a = ["{:02x}".format(c) for c in f.read()] #Opens as hex
            b = a[90::264] #Remove 90B Header
            filenames = os.path.basename(f.name) #Print all filenames (Not working yet)
            pair_hex.append(a)
            rsp_ids.append(b)
    #print ('Packet responses in order of appearance:', rsp_ids)
    #self.prepare_packets()

    '''isolates the time stamp information'''
    flatten_hex_2 = [item for items in pair_hex for item in items]
    packet_num_2 = (len(flatten_hex_2)//(90+174))
    z = np.array_split(flatten_hex_2, packet_num_2) 
    timestamp_packets = []
    for x in z:
        y = (list(x[6:10])) #Time Stamp
        timestamp_packets.append(y)
    #print (timestamp_packets)
    
    '''flattens 4 hex (8x4) values into 1 32bit int'''
    burst = []
    for i in timestamp_packets:
        burst_join = str("".join(i for i in i))    
        burst_thirtytwo = [burst_join[index:index+32] for index in range(0,len(burst_join),32)] #Creates 12-bit binary
        burst.append(burst_thirtytwo)
    #print('Group of 4 hex',burst)
    
    '''converts to big endian'''
    thirstytwobit_bigendian = []
    for j in burst:
        convert_to_int = [int(i,16) for i in j] #Converts to from 12-bit binary to integer
        thirstytwobit_bigendian.append(convert_to_int)
    #print(thirstytwobit_bigendian)
    print('Packet Headers Analysed:', len(thirstytwobit_bigendian)) #sanity check: this should be the same as packet_num
                
    '''dictionary and timestamps'''
    x = [i for j in thirstytwobit_bigendian for i in j] #Flattened into one list
    #print ('X values',x)
    y = list(range(0, len(thirstytwobit_bigendian)))
    num_values = dict(zip(y, x))
    #print('Index + Time Stamps', num_values)

    '''dictionary and response id'''
    flattened_rsps = [i for j in rsp_ids for i in j]
    resp_timestamp_dict = dict(zip(y, flattened_rsps))
    print('Index + Response ID',resp_timestamp_dict)
    
    '''plots the time stamp data'''
    fig = plt.figure()
    ax = fig.add_subplot(111)

    '''Stop 0.5 on axis'''
    #plt.yticks(range(0,len(thirstytwobit_bigendian)))
    #plt.xticks(range(0,len(thirstytwobit_bigendian)))

    plt.title( 'Time Stamp Seconds (TAI) - INMS Packet Header \n Byte 6-10 - HV-Lite-2' )
    plt.xlabel('Time Stamp')
    plt.ylabel('Number of Packets')

    #plt.plot(x, y, color='green', linestyle='dashed', linewidth=2, markersize=12)
    #plt.plot(thirstytwobit_bigendian, y, color='green', linestyle='dashed', linewidth=2, markersize=12)
    plt.hist(x, bins =  100, alpha = 1)
    
    '''adds labels'''
    #for i,j in zip(x,y):
    #    ax.annotate(str(j),xy=(i,j-1)) #adds data labels
    plt.show()

#getTimeStamps() 