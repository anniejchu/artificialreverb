# Artificial Reverb Generator
### Annie Chu | Olin College of Engineering
### Independent Study Advisor: Prof. Andrew Davis | Wellesley College

## Introduction
---------------
This program takes in a user's input .wav file and outputs a reverbed version of their choosing. The user has the ability to choose what type of reverb they would like -- Convolution vs Algorithmic. 

Convolution reverb uses digital recordings of an existing space's impulse response (IR) and convolves it with the original audio file, simulating what the original audio would sound like in that space. 

Algorithmic reverb uses a network of mathematically-defined filters, delay lines, gains, etc to simulate a reveberant space. This allows for much more flexibility and customization as its non-reliant of an impulse response of an existing physical space. 

## Program Features
--------------------
The user first chooses which artificial reverb type they want by tab selection: Convolution or Algorithmic.
In each, the following are offered:

CONFIGURATION OPTIONS
BOTH Convolution & Algorithmic
- Audio Input (.wav file)
    - 3 x Preset .wav files
    - User's choice: local .wav file
- Mix Amount (amount of wet to dry signal in the final mix)

Convolution
- Impulse Response
    - Classroom, Hallway, Computer Lab (*impulse responses recorded at Wellesley College via balloon popping)

Algorithmic
- Algorithm: Schroeder or Freeverb
    - 2 x Preset Algorithms: Schroeder Preset, Freeverb Preset
    - Option to customize: Custom Schroeder, Custom Freeverb

OUTPUT OPTIONS
- REVERB IT => plays output mix 
- DOWNLOAD => download output mix as a .wav file
- PLOT => plots comparison between original audio and output mix

## Requirements
---------------
To install all required packages, run
'''
pip install -r requirements.txt
'''

## Running the Program
----------------------
To execute the program, run Terminal command
'''
python MAINFRAME.py
''' 

## References
---------------
[Stanford CCRMA Reverb Material](https://ccrma.stanford.edu/~jos/Reverb/)
[McGill Audio Samples](http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples.html)
[UIC Audio Samples](https://www2.cs.uic.edu/~i101/SoundFiles/)
