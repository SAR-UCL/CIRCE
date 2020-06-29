'''External modules'''
import glob 
import os 
import numpy as np
from matplotlib import pyplot as plt

'''Set directory and extract basic info'''
path = '/Users/SAR/Desktop/CIRCE/Testing/Responses/post-vibe'

class GetPackets():

    def load_packets(self):
        self.pair_hex = []
        self.rsp_ids = []
        for filename in glob.glob(os.path.join(path, '*.pkt')):    
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                a = ["{:02x}".format(c) for c in f.read()]
                b = a[90::264]
                self.pair_hex.append(a)
                self.rsp_ids.append(b)
        self.prepare_packets()

    def prepare_packets(self):
        flatten_hex = [item for items in self.pair_hex for item in items]
        self.packet_num = (len(flatten_hex)//(90+174))
        z = np.array_split(flatten_hex, self.packet_num) 
        self.split_packets = []
        for x in z:
            y = (list(x[90::])) #Removes the header
            self.split_packets.append(y)

class PacketInfo():

    def basic_info(self):
        info_s = GetPackets() #call GetPackets class
        info_s.load_packets()

        print("Number of Files:", len(info_s.pair_hex))
        print("Number of packets in files:", info_s.packet_num)

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
        
        print("Number of STIM Packets:", len(flatten_stim)//172)

        self.plot_stim_packs()

    def plot_stim_packs(self):
        stim_data = self.little_endian
        
        plt.hist(stim_data, bins=10, alpha=1)
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
        
        plt.hist(stim_data, bins=10, alpha =1)
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
        burst_only = []
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
        

#main_info = PacketInfo()
#main_info.basic_info()

stim = StimPackets()
stim.prepare_stim_packs()

#hk = HouseKeepingPackets()
#hk.prepare_HK_packs()