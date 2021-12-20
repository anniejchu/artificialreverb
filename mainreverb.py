import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import simpleaudio as sa
from matplotlib.pyplot import figure
import math
import algohelper as ahp 
import convhelper as hp
import utility

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
    plt.plot(reverbed)    

    if playout == True:
        if len(data.shape) == 2:
            play_obj = sa.play_buffer(reverbed, 2, 2, fs)
        else:
            play_obj = sa.play_buffer(reverbed, 1, 2, fs)



"""
SIDE B: CONVOLUTION REVERB
"""
def convreverb(in_sig, in_IR):
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
    wet_sig = wet_sig/np.max(np.abs(wet_sig)) * (np.max(upsampled_sig1)*3)

    #downsampling if initial fs don't match
    wet_sig_ds = hp.downsampif(upsamp_factor, wet_sig)
    #padding original signal (optional -- useful for plotting)
    drysig_padded = hp.padit(sig_inorm, wet_sig_ds)
    
    #mixing dry and wet signal
    wetvsdry = 0.3 #wet to dry ratio
    mixed = (wetvsdry*wet_sig_ds) + (1-wetvsdry)*drysig_padded
    #converting float back to PCM for playout
    wet_sig_int = utility.float2pcm(wet_sig_ds, 'int16')
    mixed_int = utility.float2pcm(mixed, 'int16')  
    
    #playing out new sound
    # mix = sa.play_buffer(mixed_int, 2, 2, fs_in)
    wet = sa.play_buffer(wet_sig_int, 2, 2, fs_in)
    # dry = sa.play_buffer(data_in, 1, 2, fs_in)
    plt.plot(wet_sig_int)    

# todo - USER INPUT
input_sig1 = '/Users/anniechu/Documents/artificialreverb/samples/1CantinaBand3.wav' #mono
input_sig2 = '/Users/anniechu/Documents/artificialreverb/samples/2FrenchHorn.wav' #stereo
input_sig3 = '/Users/anniechu/Documents/artificialreverb/samples/twochannel.wav'

# -------- impulse response ------------
# todo - USER INPUT
IR_classroom = '/Users/anniechu/Documents/artificialreverb/samples/classroom5.wav'
IR_hallway = '/Users/anniechu/Documents/artificialreverb/samples/hallway2.wav'
IR_computerlab = '/Users/anniechu/Documents/artificialreverb/samples/computerlab3.wav'



#--- testing testing 1 2
fs, data = wavfile.read(input_sig3)
play_obj = sa.play_buffer(data, 2, 2, fs)

artreverb(Preset_Schroeder, input_sig3)
artreverb(Preset_Freeverb, input_sig3)
convreverb(input_sig3, IR_classroom)
convreverb(input_sig3, IR_hallway)


