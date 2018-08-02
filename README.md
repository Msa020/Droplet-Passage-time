# Droplet-Passage-time
I have developed this code to calculate the passage time of a droplet in a channel, passing through some optical LED detectors. 
The challenge here is to read the input experimetal data correctly and to select the experimetal parameters like pressure, temperature exactly at each individual passage of the droplet from the detectors. 

Input data is a .tdms file, which has been written by collaborators by a LABVIEW program.

After collectly selected part of input signals, the passage time is calculated by a cross correlation analysis of the signals.

At the end, a csv data file is produced, to neatly see the extracted experimental data, e.g. droplet passage time, pressure, temperature, etc.

In another type of experimet, we might have two dropelts moving in the channel. Here, we should also distinguish the data for these two droplets and analyse them separately.
