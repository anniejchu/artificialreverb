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
from algohelper import Schroeder

""" INITIATING FREEVERB CLASS INSTANCE"""
test = ahp.new_fverb(
   0.2, #gc
   0.84, #sgc 
   [1557, 1617, 1491, 1422, 1277, 1356, 1188, 1116], #dc -- freeverb alg has typical 8 lpfb comb filters in parallel
   0.5, #gap 
   [225, 556, 441, 341],#dap -- freeverb alg has typical 4 all pass filters in series 
   0.1,     #gx
)

""" READING IN AUDIO FILE -- assumes STEREO""" 
audiofile = "/Users/anniechu/Desktop/MutedPop.wav"
fs, data = wavfile.read(audiofile)

""" SETTING INPUT AUDIO DATA AS INPUT TO CLASS """
test.x = data
test.scale_fs = fs

""" REVERBING IT """
rv_data = test.out_mix()

""" PLAYING IN OUT """
# play_obj = sa.play_buffer(data, 2, 2, fs)
# play_obj = sa.play_buffer(rv_data, 2, 2, fs)


"""--------------------------------------------------------"""
""" INITIATING SCHROEDER CLASS INSTANCE """
SATREV = Schroeder(
   [0.805, 0.827, 0.783, 0.764], #gc
   [901, 778, 1011, 1123], #dc
   [0.7, 0.7, 0.7], #gap
   [125, 42, 12], #dap
   0.7 #gx
)

SATREV.x = data
SATREV.scale_fs = fs
ahh = SATREV.out_mix()

play_obj = sa.play_buffer(data, 2, 2, fs)
play_obj = sa.play_buffer(ahh, 2, 2, fs)



