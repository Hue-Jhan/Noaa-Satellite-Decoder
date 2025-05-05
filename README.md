# Noaa Satellite Decoder & Enhancer
NOAA Apt data Satellite decoder and image quality enhancer in python. NOAAs are american weather satellites, you can intercept them at 137mhz and receive live data from space, the data is mostly images. You can parse the images with several tools, this one focuses on quality enhancing.

# 📡 Antennas & Materials
The materials i used are:
- RTL SDR v4, or any other sdr receiver that operates at 137mhz; <img src="media/sdr" align="right" width="300">
- V-Dipole antenna, or any other antenna that recieves at uhf/vhf; <img src="media/antenna" align="right" width="300">
- Sdrpp software, or any other software that allows you to record incoming signals and save them in wav 16-bit 20800hz file format.
- (optional) Satdump software, if you want to entirely replace my code.

# 💻 Code
The code takes the wav recording file, builds an image out of it, and enhances it to make it look better. 
- First we take the wav file and turns it into 200800hz format if it isn't already.
- Then

