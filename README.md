# Artificial Reverb Generator

<img src="https://github.com/anniejchu/artificialreverb/blob/main/images/tab_conv.png" alt="conv" width="800"/>
<img src="https://github.com/anniejchu/artificialreverb/blob/main/images/tab_algo.png" alt="algo" width="800"/>

## Introduction

This program takes in a user's input .wav file and outputs a reverbed version of their choosing. The user has the ability to choose what type of reverb they would like -- Convolution vs Algorithmic. 

Convolution reverb uses digital recordings of an existing space's impulse response (IR) and convolves it with the original audio file, simulating what the original audio would sound like in that space. 

Algorithmic reverb uses a network of mathematically-defined filters, delay lines, gains, etc to simulate a reveberant space. This allows for much more flexibility and customization as its non-reliant of an impulse response of an existing physical space. 

## Program Features

The user first chooses which artificial reverb type they want by tab selection: Convolution or Algorithmic. From there, the user has the following options.

### Configuration Options

#### BOTH Convolution & Algorithmic
> - Audio Input (.wav file)
>    - 3 x Preset .wav files
>    - User's choice: local .wav file
> - Mix Amount (amount of wet to dry signal in the final mix)

#### Convolution
> - Impulse Response
>    - Classroom, Hallway, Computer Lab (*impulse responses recorded at Wellesley College)

#### Algorithmic
> - Algorithm: Schroeder or Freeverb
>     - 2 x Preset Algorithms: Schroeder Preset, Freeverb Preset
>     - Option to customize: Custom Schroeder, Custom Freeverb

### Output Options
> - REVERB IT => plays output mix 
> - DOWNLOAD => download output mix as a .wav file
> - PLOT => plots comparison between original audio and output mix

## Requirements
To install all required packages, run

<code>pip install -r requirements.txt</code>

## Running the Program
To execute the program, 1) run Terminal command


<code>python MAINFRAME.py</code>

2) Download the [**Samples**](https://github.com/anniejchu/artificialreverb/tree/main/samples) folder

## References
- [Stanford CCRMA Reverb Material](https://ccrma.stanford.edu/~jos/Reverb/)
- [McGill Audio Samples](http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples.html)
- [UIC Audio Samples](https://www2.cs.uic.edu/~i101/SoundFiles/)
- [utility.py](http://nbviewer.org/github/mgeier/python-audio/blob/master/audio-files/utility.py)

## Authors
Annie Chu | Olin College of Engineering

**IS Advisor:** Prof. Andrew Davis | Wellesley College
