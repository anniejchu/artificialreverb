import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import write
import simpleaudio as sa
from matplotlib.pyplot import figure
import math
import algohelper as ahp 
import convhelper as hp
import utility
import os
"""
SIDE A: ALGORITHMIC REVERB
"""

""" INITIATING DEFAULT FREEVERB CLASS INSTANCE"""
Preset_Freeverb = ahp.Freeverb(
   0.2, #gc
   0.84, #sgc 
   [1557, 1617, 1491, 1422, 1277, 1356, 1188, 1116], #dc -- freeverb alg has typical 8 lpfb comb filters in parallel
   0.5, #gap 
   [225, 556, 441, 341],#dap -- freeverb alg has typical 4 all pass filters in series 
   0.1,     #gx
)

""" INITIATING DEFAULT SCHROEDER CLASS INSTANCE: SATREV """
Preset_Schroeder = ahp.Schroeder(
   [0.805, 0.827, 0.783, 0.764], #gc
   [901, 778, 1011, 1123], #dc
   [0.7, 0.7, 0.7], #gap
   [125, 42, 12], #dap
   0.7 #gx
)

def artreverb(revclass, audiofile, playout = True):
    data, fs = hp.makestereo(audiofile)
    revclass.x = data
    revclass.scale_fs = fs
    reverbed = revclass.out_mix()

    if playout == True:
        if len(data.shape) == 2:
            play_obj = sa.play_buffer(reverbed, 2, 2, fs)
        else:
            play_obj = sa.play_buffer(reverbed, 1, 2, fs)
    return fs, reverbed, data


"""
SIDE B: CONVOLUTION REVERB
"""
def convreverb(in_sig, in_IR, mixamt, playout = True):
    #making both signals stereo
    sig_i, fs_in = hp.makestereo(in_sig)
    ir_i, fs_ir = hp.makestereo(in_IR)
    #converting PCM (int) to float64 & normalizing
    sig_inorm, ir_inorm = hp.norm_signals(sig_i, ir_i)
    #upsampling if fs don't match
    upsampled_sig1, sig2, upsamp_factor = hp.upsample(sig_inorm, fs_in, ir_inorm, fs_ir)
    #convolving signals
    wet_sig = hp.convolveit(upsampled_sig1, sig2)
    #post-convolution normalization
    wet_sig = wet_sig/np.max(np.abs(wet_sig)) * (np.max(upsampled_sig1)*2)

    #downsampling if initial fs don't match
    wet_sig_ds = hp.downsampif(upsamp_factor, wet_sig)
    #padding original signal (optional -- useful for plotting)
    drysig_padded = hp.padit(sig_inorm, wet_sig_ds)
    
    #mixing dry and wet signal
    wetvsdry = mixamt #wet to dry ratio
    mixed = (wetvsdry*wet_sig_ds) + (1-wetvsdry)*drysig_padded
    #converting float back to PCM for playout
    wet_sig_int = utility.float2pcm(wet_sig_ds, 'int16')
    mixed_int = utility.float2pcm(mixed, 'int16')  
    
    #playing out new sound
    if playout == True:
        mix = sa.play_buffer(mixed_int, 2, 2, fs_in)
        # wet = sa.play_buffer(wet_sig_int, 2, 2, fs_in)
        # dry = sa.play_buffer(data_in, 1, 2, fs_in)
        
    return fs_in, mixed_int, sig_i

# ft = 'Silom'
# fsz = 12
SMALL_SIZE = 9
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', family='Arial')
plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE) 

def plotty(original, mixed, fs_in):
    fig = plt.figure()
    gs = fig.add_gridspec(2, hspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
    fig.suptitle('Audio Comparison: Original vs Mixed', weight= 'bold')
    t_m = np.arange(0, len(mixed)/fs_in, (len(mixed)/fs_in)/len(mixed))
    t_o = np.arange(0, len(original)/fs_in, (len(original)/fs_in)/len(original))
    axs[0].set_title('Original', weight = 'bold')
    axs[0].plot(t_o, original)
    axs[1].set_title('Mixed', weight = 'bold')
    axs[1].plot(t_m, mixed)
    for ax in axs.flat:
        ax.set(xlabel='Time (s)', ylabel='PCM Amplitude (int16)')
    for ax in axs:
        ax.label_outer()
    plt.show()

def findlocal(filename):
    localpath = os.path.join(os.getcwd(), "samples", filename)
    return localpath

# todo - USER INPUT
input_sig1 = findlocal('1CantinaBand3.wav') #mono
input_sig2 = findlocal('2FrenchHorn.wav') #stereo
input_sig3 = findlocal('twochannel.wav')
in_presets = [input_sig1, input_sig2, input_sig3, 0]
# -------- impulse response ------------
# todo - USER INPUT
IR_classroom = findlocal('classroom5.wav')
IR_hallway = findlocal('hallway2.wav')
IR_computerlab = findlocal('computerlab3.wav')
IR_presets = [IR_classroom, IR_hallway, IR_computerlab, 0]


#--- testing testing 1 2
# fs, data = wavfile.read(input_sig1)
# print(fs)
# play_obj = sa.play_buffer(data, 2, 2, fs)

# artreverb(Preset_Schroeder, input_sig1)
# artreverb(Preset_Freeverb, input_sig3)
# convreverb(input_sig2, IR_classroom)
# convreverb(input_sig1, IR_hallway, .9)
# convreverb(input_sig1, IR_hallway, .1)


def download(samplerate, data):
    # save_path = '/Downloads'
    save_file = "reverbed.wav"
    # total = os.path.join(save_path, file_name)
    write(save_file, samplerate, data)
