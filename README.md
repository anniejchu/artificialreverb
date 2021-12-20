# Artificial Reverb Generator
## Annie Chu | Olin College of Engineering

This program takes in a user's input .wav file and outputs a reverbed version of their choosing. The user has the ability to choose what type of reverb they would like -- convolution vs algorithmic. 

Convolution reverb uses digital recordings of an existing space's impulse response (IR) and convolves it with the original audio file, simulating what the original audio would sound like in that space. 

Algorithmic reverb uses a network of mathematically-defined filters, delay lines, gains, etc to simulate a reveberant space. This allows for much more flexibility and customization as its non-reliant of an impulse response of an existing physical space. 