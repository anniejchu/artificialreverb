""" 
HELPER FUNCTIONS -- for displaying, converting data types, interpolating, etc
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import simpleaudio as sa
from matplotlib.pyplot import figure
from scipy.interpolate import interp1d
import math
import utility
import os

"""FUNCTION: display_data() -- checking data contents (mono vs stereo)
take in local filename (ex. 'CantinaBand3.wav', not '../.../XYZ/CantinaBand3.wav'
""" 
#works both mono & stereo
def display_data(audiofile, showgraphs = False):
    # audiofile = os.path.join(os.getcwd(), filename)
    fs_in, data_in = wavfile.read(audiofile)
    print(f".Wav Contents = {data_in}")
    print(f".Wav Samples Length = {data_in.shape[0]}")
    print(f".Wav Channel(s) = {len(data_in.shape)}")
    length = data_in.shape[0] / fs_in
    print(f".Wav Length = {length}s")
    print(f"Sampling Rate= {fs_in} Hz")
    print(f"bit depth= {type(data_in[0])}")
    print(f"sampling rate = {fs_in} Hz, length = {data_in.shape[0]} samples => {data_in.shape[0]/fs_in} s, channels = {len(data_in.shape)}")

    if showgraphs == True:
        figure();
        plt.plot(data_in);
        plt.title(str(audiofile));
        plt.xlabel("Samples");
        plt.ylabel("Amplitude");
    print("-------------")

"""make files stereo if mono"""
def makestereo(audiofile):
    stereodata = 0
    # audiofile = os.path.join(os.getcwd(), filename)
    fs, data = wavfile.read(audiofile)
    chan_num = len(data.shape)
    if chan_num == 1:
        stereodata = np.stack((data, data), axis=-1)
    else: #if chan_num == 2, stereo
        stereodata = data
    return stereodata, fs

"""function to read sound depending on # of channels in input signal .wav file
Takes in fspcm,audiopcm of fspcm,audiopcm  = wavfile.read(filepath)
"""
def play_sound(audiopcm, fspcm):
    num_chan = len(audiopcm.shape)
    if num_chan == 1:
        playwav = sa.play_buffer(audiopcm, 1, 2, fspcm)
        return playwav
    elif num_chan == 2:
        playwav = sa.play_buffer(audiopcm, 2, 2, fspcm)
        return playwav
        
"""
FUNCTION match_fs: calculating diff in fs factor, returns upsampling factor & which data to upsample
"""

def match_fs(input_fs, IR_fs, input_sig, IR):
    upsamp= IR_fs/input_fs; #IR fs divided by fs_in -- if > 1, IR has higher fs; if < 1 data_in has higher fs
    upsamp_data = 0;
    baseline = 0;
    data_name = 0;
    if input_fs > IR_fs: #if samp rate of data is greater than samp rate of IR, take reciprocal
        upsamp = 1/upsamp;
        upsamp_data = IR;
        data_name = "ir_i";
        baseline = input_sig;
#         print("upsample_data: data_IR")
    else:
        upsamp_data = input_sig;
        data_name = "sig_i";
        baseline = IR;
#         print("upsample_data: data_in")
    return int(upsamp), upsamp_data, data_name, baseline

#pcm2float
"""
FUNCTION: using utility to convert int16 to float32 as convolving large numbers takes up too long
"""
def norm_signals(sig, IR):
    normalized_sig = utility.pcm2float(sig, "float32")
    normalized_IR = utility.pcm2float(IR, "float32")

    return normalized_sig, normalized_IR


"""
upsampling dataset as given by match_fs function
"""
def upsample(sig1, sig1_fs, sig2, sig2_fs, showgraphs = False):
    upsamp, up_data, up_dataname, baseline_data = match_fs(sig1_fs, sig2_fs, sig1, sig2)
    
    k = np.arange(len(up_data))
    print(f"k = {k}")
    print(f"up_data[:,0] = {up_data[:,0]}")

    #inserting zeros in between original sample
    n = up_data.shape
    size = n[0]
    zeroed = np.zeros(upsamp*size, dtype = float)
    print(f"zeros = {zeroed}")
    zeroed = np.stack((zeroed, zeroed), axis = -1)
    zeroed[:,0][::upsamp] = up_data[:,0]
    print(f"updata[:,0] = {up_data[:,0]} ")
    zeroed[:,1][::upsamp] = up_data[:,1]
    print(f"zeroed inserted = {zeroed}")
    k_up = np.arange(len(zeroed))
    print(k_up)
    # print(k_up[zeroed[0]!=0])

    #upsampling & interpolation
    interp_L = np.interp(k_up, k_up[zeroed[:,0]!=0], zeroed[:,0][zeroed[:,0]!=0])
    interp_R = np.interp(k_up, k_up[zeroed[:,1]!=0], zeroed[:,1][zeroed[:,1]!=0])
    data_interp = np.stack((interp_L, interp_R) , axis = -1)
    print(f"New Upsamp&Interp Data = {data_interp}, upsamp factor = {upsamp}" )

    print(data_interp.dtype)
    if showgraphs==True:
        plt.figure() #original signal
        plt.plot(k,up_data)
        plt.ylim([-4000, 4000])
        plt.xlabel('Sample [k]')
        plt.ylabel('amplitude')
        plt.title('original signal')
        
        plt.figure() #upsampled signal -- inserted 0s
        plt.plot(k_up,out)
        plt.ylim([-4000, 4000])
        plt.xlabel('Sample [k]')
        plt.ylabel('amplitude')
        plt.title('upsampled signal')
        
        plt.figure() #interpolated signal -- output
        plt.plot(k_up,out)
        plt.plot(k_up, data_interp)
        plt.xlim([15000, 16000])
        plt.ylim([-4000, 4000])
        plt.xlabel('Sample [k]')
        plt.ylabel('amplitude')
        plt.title('interpolated signal')
        plt.legend(['upsampled', "interpolated"])
    return data_interp, baseline_data, upsamp

def convolveit(sig1, sig2):
    wet_sig_L = signal.convolve(sig1[:,0], sig2[:,0], mode='full', method='auto')
    wet_sig_R = signal.convolve(sig1[:,1], sig2[:,1], mode='full', method='auto')
    wet_sig = np.stack((wet_sig_L, wet_sig_R), axis = -1)
    return wet_sig
    
def downsampif(upsamp_factor, sig):
    if upsamp_factor != 1: #&is 2
        wet_sig_ds = [sig[i] for i in range(len(sig)) if i % upsamp_factor== 0]
        wet_sig_ds = np.asarray(wet_sig_ds)
    else:
        wet_sig_ds = sig
    return wet_sig_ds

def padit(smaller, pad_sig_to):
    shape = np.shape(smaller)
    drysig_padded = np.stack((np.zeros((len(pad_sig_to))), np.zeros((len(pad_sig_to)))), axis = -1)
    drysig_padded[:,0][:shape[0]] = smaller[:,0] #dry sig is padded data_in
    drysig_padded[:,1][:shape[0]] = smaller[:,1] #dry sig is padded data_in
    return drysig_padded


def signal_comparison(dry, dry_pad, wet, mixed, fs_in):
    plt.plot(wet, label = "Wet Signal");
    plt.plot(dry, label = "Dry Signal");
    plt.legend();
    plt.xlabel("Samples");
    plt.ylabel("Amplitude");
    plt.title("Dry vs Wet: Sample Comparison")

    t_dry = np.arange(0, len(dry)/fs_in, (len(dry)/fs_in)/len(dry))
    t_wet = np.arange(0, len(wet)/fs_in, (len(wet)/fs_in)/len(wet))
    t_mix = np.arange(0, len(dry_pad)/fs_in, (len(dry_pad)/fs_in)/len(dry_pad))

    plt.figure()
    plt.plot(t_wet,wet, label = "Wet");
    plt.plot(t_dry, dry, label = "Dry");
    plt.legend();
    plt.xlabel("Time (s)");
    plt.ylabel("Amplitude");
    plt.title("Dry vs Wet(downsampled): Time Comparison")

    plt.figure()
    plt.plot(t_mix, mixed, label = "Mixed")
    plt.plot(t_dry, dry, label = "Dry (downsampled)");
    plt.legend();
    plt.xlabel("Time (s)");
    plt.ylabel("Amplitude");
    plt.title(f"Dry vs Mixed: Time Comparison | G_w = ");

