# Droplet-Speed
I have developed this code to calculate the speed of a droplet in a microchannel, passing through some optical LED detectors. 
The main challenge here is to clean the input data, and to read the input experimetal data correctly and to select the experimetal parameters like pressure, temperature exactly at each individual passage of the droplet from the detectors. 

Input data is a .tdms file, which has been written by experimental collaborators in a LABVIEW program.
Having selected the correct input signals for each experiment, the droplet's passage time between detectors, is calculated by a cross correlation analysis of the signals.

At the end, a csv data file is produced, to neatly see the extracted experimental data, e.g. droplet passage time, pressure, temperature, etc. This data file is now ready for further post processing. 

In another type of experimet, we might have two (more than one) dropelts moving in the channel. Here, we should also distinguish the data for these droplets and analyse them separately.
