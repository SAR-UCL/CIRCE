'''External modules'''
import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

'''Set directory and extract basic info'''
#path = r'/Users/SAR/Documents/2. Academia/2. UCL/PhD/CIRCE/Data In/Testing/Responses/Science'
path = r'PATH' 

class GetPackets():

    def load_packets(self):
        self.pair_hex = []
        self.rsp_ids = []
        for filename in glob.glob(os.path.join(path, '*.pkt')):    
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                a = ["{:02x}".format(c) for c in f.read()] #Opens as hex
                b = a[90::264] #Remove 90B Header
                self.pair_hex.append(a)
                self.rsp_ids.append(b)
        #print (self.rsp_ids)
        self.prepare_packets()

    def prepare_packets(self):
        flatten_hex = [item for items in self.pair_hex for item in items]
        self.packet_num = (len(flatten_hex)//(90+174))
        z = np.array_split(flatten_hex, self.packet_num) 
        self.split_packets = []
        for x in z:
            y = (list(x[90::])) #Remove 90B Header
            self.split_packets.append(y)
        #ßprint (self.split_packets)

class PacketInfo():

    def basic_info(self):
        info_s = GetPackets() #call GetPackets class
        info_s.load_packets()

        print("Number of files:", len(info_s.pair_hex))
        print("Number of packets in files:", info_s.packet_num, '\n')

        self.identify_packets()

    ''' Check for the number and type of packet outputs'''
    def identify_packets(self):

        info_s = GetPackets() #call GetPackets class
        info_s.load_packets()

        flattened_rsp = [item for items in info_s.rsp_ids for item in items]
        print ("Number of different packets:")
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

class StimPackets():

    def prepare_stim_packs(self):
        info = GetPackets() #call GetPackets class
        info.load_packets()
        
        stim_only = []
        for i in info.split_packets:
            if i [0] == '04':
                j = i[2::] #Removes id and seq count
                stim_only.append(j)
        
        flatten_stim = [item for items in stim_only for item in items]
        endian_pairs = [i+j for i,j in zip(flatten_stim[::2], flatten_stim[1::2])] #Pairs into fours
        self.little_endian = [int(h[2:4] + h[0:2], 16) for h in endian_pairs] #Converts to Little Endian
        
        #print("Number of STIM Packets:", len(flatten_stim)//172)

        self.plot_stim_packs()

    def plot_stim_packs(self):
        stim_data = self.little_endian
        
        plt.hist(stim_data, bins=30, alpha=1)
        plt.xlabel('Time')
        plt.ylabel('Count')
        
        plt.show()

        '''
        try:
            File format: TBD   
            plt.savefig("Figures/STIM-04_FM1-2_b800.png", bbox_inches='tight')
            print ("File saved")
        except IOError:
            print ("File creation failed")
        '''

class HouseKeepingPackets():
    
    def prepare_HK_packs(self):

        info = GetPackets() #call GetPackets class
        info.load_packets()

        stim_only = []
        for i in info.split_packets:
            if i [0] == '09':
                j = i[2::] #Removes id and seq count
                stim_only.append(j)
        
        flatten_stim = [item for items in stim_only for item in items]
        endian_pairs = [i+j for i,j in zip(flatten_stim[::2], flatten_stim[1::2])] #Pairs into fours
        self.little_endian = [int(h[2:4] + h[0:2], 16) for h in endian_pairs] #Converts to Little Endian
        
        print("Number of House Keeping Packets:", len(flatten_stim)//172)

        #self.plot_stim_packs()

    def plot_HK_packs(self):
        stim_data = self.little_endian
        
        plt.hist(stim_data, bins=10, alpha=1) #alpha is transparency
        plt.xlabel('Time')
        plt.ylabel('Count')
        
        plt.show()

        '''
        try:
            plt.savefig("CIRCE_figs/STIM-04_FM1-2_b800.png", bbox_inches='tight')
            print ("File saved")
        except IOError:
            print ("File creation failed")
        '''

class SciencePackets():
    
    def prepare_HK_packs(self):

        info = GetPackets() #call GetPackets class
        info.load_packets()

        stim_only = []
        #burst_only = []
        for i in info.split_packets:
            if i [0] == '08':
                j = i[2::] #Removes id and seq count
                stim_only.append(j)
        
        flatten_stim = [item for items in stim_only for item in items]
        endian_pairs = [i+j for i,j in zip(flatten_stim[::2], flatten_stim[1::2])] #Pairs into fours
        self.little_endian = [int(h[2:4] + h[0:2], 16) for h in endian_pairs] #Converts to Little Endian
        
        print("Number of House Keeping Packets:", len(flatten_stim)//172)

        #self.plot_stim_packs()

    def plot_HK_packs(self):
        stim_data = self.little_endian
        
        plt.hist(stim_data, bins=10, alpha =1)
        plt.xlabel('Time')
        plt.ylabel('Count')
        
        plt.show()

        
        try:
            '''File format: TBD'''    
            plt.savefig("Figures/Science_1.png", bbox_inches='tight')
            print ("File saved")
        except IOError:
            print ("File creation failed")
        
main_info = PacketInfo()
main_info.basic_info()

#stim = StimPackets()
#stim.prepare_stim_packs()

#hk = HouseKeepingPackets()
#hk.prepare_HK_packs()