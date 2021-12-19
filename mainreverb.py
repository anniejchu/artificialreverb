""" SIDE 2: algorithmic reverb -- schroeder, freeverb """
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

""" INITIATING FREEVERB CLASS INSTANCE"""
Preset_Freeverb = ahp.new_fverb(
   0.2, #gc
   0.84, #sgc 
   [1557, 1617, 1491, 1422, 1277, 1356, 1188, 1116], #dc -- freeverb alg has typical 8 lpfb comb filters in parallel
   0.5, #gap 
   [225, 556, 441, 341],#dap -- freeverb alg has typical 4 all pass filters in series 
   0.1,     #gx
)

""" INITIATING SCHROEDER CLASS INSTANCE: SATREV """
Preset_Schroeder = ahp.Schroeder(
   [0.805, 0.827, 0.783, 0.764], #gc
   [901, 778, 1011, 1123], #dc
   [0.7, 0.7, 0.7], #gap
   [125, 42, 12], #dap
   0.7 #gx
)

""" READING IN AUDIO FILE -- assumes STEREO""" 
audiofile = "/Users/anniechu/Documents/artificialreverb/samples/CantinaBand3.wav"

def artreverb(revclass, audiofile, playout = True):
    data, fs = hp.makestereo(audiofile)
    revclass.x = data
    revclass.scale_fs = fs
    reverbed = revclass.out_mix()
    if playout == True:
        play_obj = sa.play_buffer(reverbed, 2, 2, fs)

#--- testing different artificial reverb types
# artreverb(Preset_Schroeder, audiofile)
artreverb(Preset_Freeverb, audiofile)


"""
SIDE B: CONVOLUTION REVERB
"""
def convreverb(in_sig, in_IR):
    sig_i, fs_in = hp.makestereo(in_sig)
    ir_i, fs_ir = hp.makestereo(in_IR)

    sig_inorm, ir_inorm = hp.norm_signals(sig_i, ir_i)

    upsampled_sig1, sig2, upsamp_factor = hp.upsample(sig_inorm, fs_in, ir_inorm, fs_ir)

    wet_sig = convolveit(upsampled_sig1, sig2)

    wet_sig = wet_sig/np.max(np.abs(wet_sig)) * np.max(upsampled_sig1)
    
    wet_sig_ds = downsampif(upsamp_factor, wet_sig)
    
    drysig_padded = padit(sig_inorm, wet_sig_ds)
    
    wetvsdry = 0.3 #change 1 knob to 2 knobs?
    mixed = (wetvsdry*wet_sig_ds) + (1-wetvsdry)*drysig_padded

    wet_sig_int = utility.float2pcm(wet_sig_ds, 'int16')
    mixed_int = utility.float2pcm(mixed, 'int16')  
    
    # mix = sa.play_buffer(mixed_int, 2, 2, fs_in)
    wet = sa.play_buffer(wet_sig_int, 2, 2, fs_in)
    # dry = sa.play_buffer(data_in, 1, 2, fs_in)
    

# todo - USER INPUT
input_sig1 = '/Users/anniechu/Documents/artificialreverb/samples/CantinaBand3.wav'
input_sig2 = 'preset 2'
input_sig3 = 'preset 3'

# -------- impulse response ------------
# todo - USER INPUT
IR_classroom = '/Users/anniechu/Documents/artificialreverb/samples/classroom5.wav'
IR_hallway = '/Users/anniechu/Documents/artificialreverb/samples/hallway2.wav'
IR_computerlab = '/Users/anniechu/Documents/artificialreverb/samples/computerlab3.wav'

# convreverb(input_sig1, IR_classroom)
convreverb(input_sig1, IR_hallway)


