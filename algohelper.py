import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import simpleaudio as sa
from matplotlib.pyplot import figure
import math

def comb(x_n, g, d):
    # x_n is numpy array of initial samples
    y_n = np.zeros(len(x_n))
    if type(d) == int:
        for i in range(len(x_n)):
            if i-d < 0:
                y_n[i] = x_n[i]
            else:
                y_n[i] = x_n[i] + g*y_n[i-d]
    elif type(d) == float:
        for i in range(len(x_n)):
            down = math.floor(i-d)
            up = math.ceil(i-d)
            y_mid = y_n[down] + (((y_n[up] - y_n[down])/(up - down)) * ((i-d) - down)) 
            if i-d < 0:
                y_n[i] = x_n[i]
            else:
                y_n[i] = x_n[i] + g*y_mid
                
            
                print(F" n = {i} | d = {d} | n-d = {i-d}")
#                 print(F" Round Down {i-1.5} : {down} | Round Up {i-1.5} : {up}")
#                 print(F" Y({down}): {y_n[down]} | Y({up}): {y_n[up]}")
#                 print(F" Y({i-1.5}) = {0.5*(y_n[up] + y_n[down])}")
#                 print('-----')

    return y_n

def allpass(x_n, g, d):
    # x_n is numpy array of initial samples
    y_n = np.zeros(len(x_n));
    
    if type(d) == int:
        for i in range(len(x_n)):
            if i-d < 0:
                y_n[i] = g*x_n[i]
            else:
                y_n[i] = g*x_n[i] + x_n[i-d] - g*y_n[i-d]
            
    elif type(d) == float: 
        for i in range(len(x_n)):
            down = math.floor(i-d)
            up = math.ceil(i-d)
            
            if i-d < 0:
                y_n[i] = g*x_n[i]

            else:
                x_mid = x_n[down] + ((x_n[up] - x_n[down]) * ((i-d) - down))
                y_mid =  y_n[down] + ((y_n[up] - y_n[down]) * ((i-d) - down))
                y_n[i] = g*x_n[i] + x_mid - g*y_mid

    return y_n


def lp_comb(x_n, g, d, sg):
    """
    # x_n -> numpy array of initial samples
    # g -> damp = initialdamp*scaledamp
        `damping'' parameter controls how rapidly T60 shortens as a function of increasing frequency.
        
    # sg -> lowpass scale factor = room size = initialroom*scaleroom + offsetroom
        - RoomSize (range: 0 to 1) -- controls the length of the reverb, a higher value means longer reverb
        - The feedback variable f (sg here) mainly determines reverberation time at low-frequencies 
            at which the feedback lowpass has negligible effect. 
        The feedback lowpass causes the reverberation time to decrease with frequency, which is natural.
        room size'' parameter can be interpreted as setting the low-frequency T60 (time to decay 60 dB) 
    
    https://ccrma.stanford.edu/~jos/Reverb/Freeverb_Parameters.html
    """
    y_n = np.zeros(len(x_n));
    
    if type(d) == int:
#         print("y_n[i] = x_n[i] - g*x_n[i-1] + g*y_n[i-1] + sg*(1-g)*y_n[i-d]")
        for i in range(len(x_n)):
            if i-d < 0 and i-1 < 0:
                y_n[i] = x_n[i]
#                 print(F"C1: I = {i} D = {d} | I-D = NEG = {i-d} | i-1 = NEG = {i-1}")
#                 print(F"CHECKING... y_n[{i}] = {y_n[i]} SHOULD = {x_n[i]}")
            elif i-d < 0 and i-1 >= 0:
                y_n[i] = x_n[i] - g*x_n[i-1] + g*y_n[i-1]
#                 print(F"C2: I = {i}  D = {d}| I-D = NEG = {i-d} | i-1 = >= 0 = {i-1}")
#                 print(F"CHECKING...y_n[{i}] =  {y_n[i]} SHOULD = {x_n[i]} - 0.5*{x_n[i-1]} + 0.5*{y_n[i-1]}")
            else:
                y_n[i] = x_n[i] - g*x_n[i-1] + g*y_n[i-1] + sg*(1-g)*y_n[i-d]
#                 print(F"C3: I = {i}  D = {d}| I-D = pos = {i-d} | i-1 = pos = {i-1}")
#                 print(F"CHECKING...y_n[{i}] =  {y_n[i]} SHOULD = {x_n[i]} - 0.5*{x_n[i-1]} + 0.5*{y_n[i-1]}+ 1*0.5*{y_n[i-d]}")
        
    elif type(d) == float:
        for i in range(len(x_n)):            
            if i-d < 0 and i-1 < 0:
#                 print("case 0: y_n[i] = x_n[i] ")
                y_n[i] = x_n[i]
            elif i-d < 0 and i-1 > 0:
#                 print("case 1: y_n[i] = x_n[i] - g*x_1 + g*y_1")
                down1 = math.floor(i-1)
                up1 = math.ceil(i-1) 
                x_1 = 0.5*(x_n[up1] + x_n[down1])
                y_1 = 0.5*(y_n[up1] + y_n[down1])
                x_1 = x_n[down1] + ((x_n[up1] - x_n[down1]) * ((i-1) - down1))
                y_1 =  y_n[down1] + ((y_n[up1] - y_n[down1]) * ((i-1) - down1)) 
                y_n[i] = x_n[i] - g*x_1 + g*y_1
#                 print(f"y_n[{i}] = {x_n[i]} - {g*x_1} + {g*y_1}")
            elif i-d >=0: 
#                 print("case 2: both pos, ")
                down = math.floor(i-d)
                up = math.ceil(i-d)
                down1 = math.floor(i-1)
                up1 = math.ceil(i-1) 
                x_1 = x_n[down1] + ((x_n[up1] - x_n[down1]) * ((i-1) - down1))
                y_1 =  y_n[down1] + ((y_n[up1] - y_n[down1]) * ((i-1) - down1)) 
                
                x_mid = x_n[down] + ((x_n[up] - x_n[down]) * ((i-d) - down))
#                 print(f"x_mid[{i}] = {x_mid} = {x_n[down]} + (({x_n[up]} - {x_n[down]}) * (({i-d}) - {down})")

                y_mid =  y_n[down] + ((y_n[up] - y_n[down]) * ((i-d) - down)) 
#                 print(f"y_mid[{i}] = {y_mid} = {y_n[down]} + (({y_n[up]} - {y_n[down]})) * (({i-d}) - {down})")
                
                
                y_n[i] = x_n[i] - g*x_1 + g*y_1 + sg*(1-g)*y_mid
#                 print(f" y_n[{i}] = {y_n[i]} = {x_n[i]} - g*{x_1} + g*{y_1} + sg*(1-g)*{y_mid}")
#                 print(y_n)
        
    return y_n

"""
---------- FREEVERB CLASS  -------------
""" 

class Freeverb:
    def __init__(self, comb_g, comb_sg, comb_d, ap_g, ap_d, x_g):
        self.comb_g = comb_g
        self.comb_sg = comb_sg
        self.comb_d = comb_d
        self.ap_g = ap_g
        self.ap_d = ap_d
        self.x_g = x_g
        self.right_d = 23
        #set once audio file is read in
        self.x = 0
        self.scale_fs = 0
                    
    '''SCALING DELAYS WITH INPUT SIGNAL SAMPLING FREQUENCY'''
    def scale_delays(self):
        s_comb_d = (self.scale_fs/44100)*np.array(self.comb_d)
        s_ap_d = (self.scale_fs/44100)*np.array(self.ap_d)
        s_right_d = (self.scale_fs/44100)*self.right_d
        return s_comb_d, s_ap_d, s_right_d
    
    '''SPLITTING L/R CHANNEL INFO AND ADDING SCALED L/R DELAYS'''
    def set_chparam(self, ch):
        s_comb_d, s_ap_d, s_right_d = self.scale_delays()
        if (ch == "left"):
            x_ch = self.x[:,0]
            sch_comb_d = s_comb_d
            sch_ap_d = s_ap_d
        elif (ch == "right"):
            x_ch = self.x[:,1]
            sch_comb_d = s_comb_d + s_right_d
            sch_ap_d = s_ap_d + s_right_d

        return x_ch, sch_comb_d, sch_ap_d
    
    def apply_reverb(self, ch): #ch either "left" or "right"
        chan, comb_delay, ap_delay = self.set_chparam(ch)
#         print(f"channel is {ch}, gives {chan}, SCALED: comb_d {comb_delay}, ap_d {ap_delay}")
        yc = [0]*len(comb_delay)
        yap = [0]*len(ap_delay)
        yc_out = 0
        yap_out = 0
        
        '''1) Comb Filter Stage (Parallel)'''
        for i in range(len(comb_delay)):
            yc[i] = lp_comb(chan, self.comb_g, float(comb_delay[i]), self.comb_sg) #creating 8 comb filters 
            yc_out += yc[i] #adding 8 comb filters in parallel
#             print(f"yc{i} = {yc[i]}")
#             print(f"yc_out = {yc_out}")

        ''' 2) All Pass Filter Stage (Series)'''
        for i in range(len(ap_delay)):
            #creating 4 all pass filters
            if i == 0:
                yap[i] = allpass(yc_out, self.ap_g, float(ap_delay[i]))
            else:
                yap[i] = allpass(yap[i-1], self.ap_g, float(ap_delay[i]))
#             print(f"yap[{i}] = {yap[i]}")

        yap_out = yap[len(ap_delay)-1]

        return chan, yap_out, yap, yc_out, yc #last 2 not used, for testing

    def raw_mix(self):
        Lchan, Lyap_out, Lyap_test, Lyc_out_test, Lyc = self.apply_reverb("left")
        Rchan, Ryap_out, Ryap_test, Ryc_out_test, Ryc = self.apply_reverb("right")
        lMix_out = Lyap_out  + (self.x_g*Lchan) #SHOULD BE FLOATS
        rMix_out = Ryap_out  + (self.x_g*Rchan) 
        
        return lMix_out, rMix_out
    
    def norm_mix(self):
        Lmix, Rmix = self.raw_mix()
        Lmix_norm = np.int16(Lmix/np.max(np.abs(Lmix)) * 32767)
        #Lmix_norm = np.int16(Lmix/np.max(np.abs(Lmix)* np.max(self.x)) * 32767)

        Rmix_norm = np.int16(Rmix/np.max(np.abs(Rmix)) * 32767)
        #Rmix_norm = np.int16(Rmix/np.max(np.abs(Rmix)* np.max(self.x)) * 32767)

        return Lmix_norm, Rmix_norm
    
    def out_mix(self):
        Lmix_norm, Rmix_norm = self.norm_mix()
        out_mix = np.stack((Lmix_norm, Rmix_norm), axis=-1)
        return out_mix
    '''
    TEST BENCHES
    '''
    def __repr__(self): 
        return "Test combd:% s" % (self.comb_d) 
    def test_scale_delays(self):
        cd, apd, right_d = self.scale_delays()
        print(f"scaling fs = {self.scale_fs}")
        print(f"scaled dc is {cd} should be {self.scale_fs/44100} * {self.comb_d}")
        print(f"ap delay is {apd} should be {self.scale_fs/44100} * {self.ap_d}")
        print(f"right delay is {right_d} should be {self.scale_fs/44100} * {self.right_d}")
    def test_set_chparam(self):
        x_chan, combd_scaled, apd_scaled = self.set_chparam("left")
        x_chan1, combd_scaled1, apd_scaled1 = self.set_chparam("right")
        print(f"Channel: L | Channel Data should be {self.scale_fs/44100} * {self.x[:,0]}, IS {x_chan}")
        print(f"Channel: L | comb_d should be {self.scale_fs/44100} * {self.comb_d}, IS  {combd_scaled}")
        print(f"Channel: L | ap_d should be {self.scale_fs/44100} * {self.ap_d}, IS  {apd_scaled}")
        print("---------------------------------------------------------------------")
        print(f"Channel: R | Channel Data should be {self.scale_fs/44100} * {self.x[:,1]}, IS {x_chan1}")
        print(f"Channel: R | comb_d should be {self.scale_fs/44100} * ({self.comb_d} + {self.right_d}), IS  {combd_scaled1}")
        print(f"Channel: R | ap_d should be {self.scale_fs/44100} * ({self.ap_d} + {self.right_d}), IS  {apd_scaled1}")
    def test_apply_reverb(self, ch):
        chan, yap_out, yap_test, yc_out_test, yc_test = self.apply_reverb(ch)
        print(f"{ch} channel data ==> {chan}")
        print("----> initiating reverb process...")
              
        print("-----------> printing comb filter stage results...")  
        for i in range(len(yc_test)):
            print(f"yc{i} = {yc_test[i]}")
              
        print("-----------> comb filter stage output...")  
        print(f"yc_out = {yc_out_test}")
              
        print("-----------> printing all-pass filter stage...")  
        for i in range(len(yap_test)):
            print(f"yap{i} = {yap_test[i]}")
                
        print("-----------> comb filter stage output...")  
        print(f"yap_out = {yap_out}")
    def test_raw_mix(self):
        Lmix_out, Rmix_out = self.raw_mix()
        print(f"Left Mix (Rev + Original) = {Lmix_out}")
        print(f"Right Mix (Rev + Original) = {Rmix_out}")
    def test_norm_mix(self):
        Lmix_norm, Rmix_norm = self.norm_mix()
        print(f"Left Mix (Normalized) = {Lmix_norm}")
        print(f"Right Mix (Normalized) = {Rmix_norm}")
    def test_out_mix(self):
        outmix = self.out_mix()
        print(f"Out Signal = {outmix}")
        print(f"Left Side = {outmix[:,0]}")
        print(f"Right Side = {outmix[:,1]}")
        


"""
---------- schroeder CLASS  -------------
""" 
class Schroeder:
    kind = 'schroeder'
    
    def __init__(self, gc, dc, gap, dap, gx):
        self.gc = gc
        self.dc = dc
        self.gap = gap
        self.dap = dap
        self.gx = gx
        self.x = 0

    def scale_delays(self):
        s_comb_d = (self.scale_fs/44100)*np.array(self.dc)
        s_ap_d = (self.scale_fs/44100)*np.array(self.dap)
        return s_comb_d, s_ap_d
    
    def apply_reverb(self, ch):
        if ch == "left":
            chan = self.x[:,0]
        else:
            chan = self.x[:,1]
        yc1 = comb(chan, self.gc[0], self.dc[0]) 
        yc2 = comb(chan, self.gc[1], self.dc[1])
        yc3 = comb(chan, self.gc[2], self.dc[2])
        yc4 = comb(chan, self.gc[3], self.dc[3])

        yc_out = yc1 + yc2 + yc3 + yc4

        yap1 = allpass(yc_out, self.gap[0], self.dap[0])
        yap2 = allpass(yap1, self.gap[1], self.dap[1])
        yap3 = allpass(yap2, self.gap[2], self.dap[2])

        y_final = yap3 + (self.gx*chan)
        return chan,y_final
    
    def raw_mix(self):
        Lchan, Lyap_out = self.apply_reverb("left")
        Rchan, Ryap_out = self.apply_reverb("right")
        lMix_out = Lyap_out  + (self.gx*Lchan) #SHOULD BE FLOATS
        rMix_out = Ryap_out  + (self.gx*Rchan) 
        
        return lMix_out, rMix_out
    
    def norm_mix(self):
        Lmix, Rmix = self.raw_mix()
        Lmix_norm = np.int16(Lmix/np.max(np.abs(Lmix)) * 32767)
        Rmix_norm = np.int16(Rmix/np.max(np.abs(Rmix)) * 32767)
        return Lmix_norm, Rmix_norm
    
    def out_mix(self):
        Lmix_norm, Rmix_norm = self.norm_mix()
        out_mix = np.stack((Lmix_norm, Rmix_norm), axis=-1)
        return out_mix