import helper as hp
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


""" SIDE 1: convolution reverb -- recorded IR """

"""
------- laying out audio file options -------
"""

# --------- input audio -------------
# todo - USER INPUT
input_sig1 = '/Users/anniechu/Documents/artificialreverb/samples/CantinaBand3.wav'
input_sig2 = 'preset 2'
input_sig3 = 'preset 3'

# -------- impulse response ------------
# todo - USER INPUT
IR_classroom = '/Users/anniechu/Documents/artificialreverb/samples/classroom5.wav'
IR_hallway = '/Users/anniechu/Documents/artificialreverb/samples/hallway2.wav'
IR_computerlab = '/Users/anniechu/Documents/artificialreverb/samples/computerlab3.wav'

""" CHOOSING AUDIO FILES """
in_sig = input_sig1
in_IR = IR_classroom

""" 0. INITIATING DATA (optional)"""
fs_in, data_in = wavfile.read(in_sig)
fs_IR, data_IR = wavfile.read(in_IR)

# hp.display_data(in_sig, showgraphs=True)
# hp.display_data(in_IR, showgraphs=True)

""" 1. MAKING BOTH STEREO """
sig_i, sig_ifs = hp.makestereo(in_sig)
ir_i, ir_ifs = hp.makestereo(in_IR)

""" 2. CONVERT PCM2FLOAT (NORMALIZED) """
sig_inorm, ir_inorm = hp.norm_signals(sig_i, ir_i)

""" 3. INTERPOLATION IF DIFFERENT FS """
upsampled_sig1, sig2, upsamp_factor = hp.upsample(sig_inorm, sig_ifs, ir_inorm, ir_ifs)

""" 4. CONVOLVE! """
wet_sig_L = signal.convolve(upsampled_sig1[:,0], sig2[:,0], mode='full', method='auto')
wet_sig_R = signal.convolve(upsampled_sig1[:,1], sig2[:,1], mode='full', method='auto')
wet_sig = np.stack((wet_sig_L, wet_sig_R), axis = -1)

# figure()
# plt.plot(wet_sig[:,0], label = "wet sig stereo");
# plt.plot(upsampled_sig1[:,0]);
# plt.plot(sig2[:,0]);
# plt.title("Normalized Convolution");
# plt.xlabel("Samples");
# plt.ylabel("Amplitude");
# plt.legend(["Convolved (wet)", "sig1", "sig 2"])

""" 5. POST-CONVOLUTION NORMALIZATION """
wet_sig = wet_sig/np.max(np.abs(wet_sig)) * np.max(upsampled_sig1)

""" 5B. IF DIFF: DOWNSAMPLING IF DIFF (hardcoded to be 2)"""
wet_sig_ds = [wet_sig[i] for i in range(len(wet_sig)) if i % upsamp_factor== 0]
wet_sig_ds = np.asarray(wet_sig_ds)

""" 5c. zero padding"""
shape = np.shape(sig_inorm)
drysig_padded = np.stack((np.zeros((len(wet_sig_ds))), np.zeros((len(wet_sig_ds)))), axis = -1)
drysig_padded[:,0][:shape[0]] = sig_inorm[:,0] #dry sig is padded data_in
drysig_padded[:,1][:shape[0]] = sig_inorm[:,1] #dry sig is padded data_in

""" 6. MIXING """
wetvsdry = 0.3 #change 1 knob to 2 knobs?
mixed = (wetvsdry*wet_sig_ds) + (1-wetvsdry)*drysig_padded

""" 7. CONVERT BACK FLOAT2PCM"""
wet_sig_int = utility.float2pcm(wet_sig_ds, 'int16')
mixed_int = utility.float2pcm(mixed, 'int16')

""" 8. PLAYBACK, run 1 by 1"""
mix = sa.play_buffer(mixed_int, 2, 2, fs_in)
wet = sa.play_buffer(wet_sig_int, 2, 2, fs_in)
# dry = sa.play_buffer(data_in, 1, 2, fs_in)

""" 8b. visualize brUH why wont you work"""
# x = hp.signal_comparison(data_in, drysig_padded, wet_sig_int, mixed_int, fs_in)
# plt.plot(data_in)
