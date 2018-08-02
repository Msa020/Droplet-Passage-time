#two droplets code

import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from nptdms import tdms
from numpy import array,linspace,argmax
from scipy.signal import correlate
import pandas as pd
import csv
from scipy import ndimage
#-----------------------constants---------------------------------
#distance between detectors to the dtc1
#x10_1 = 100
#------------------------READ TDMS FILE-------------------------------------------
filenameS = "RESULTS_24-02-18_19-21-53.tdms"
tdms_file = TdmsFile(filenameS)
#=============temperature===================
temp = tdms_file.object("pressures&temperature [10Hz]","temperature")
temperature = temp.data
#-----------------------------FREQUENCY SET--------------------------------------------
frequency = 20000 #frequency for detectors
frequency1 = 10 #frequency for time(real time), presssure, temperature
#------------------------READING DETECTORS-------------------------------------
channel_object1 = tdms_file.object("detectors 2,00kHz", "detector #1")
det1 = channel_object1.data/100

channel_object5 = tdms_file.object("detectors 2,00kHz", "detector #5")
det5 = channel_object5.data/100

channel_object10 = tdms_file.object("detectors 2,00kHz", "detector #10")  #************
det10 = channel_object10.data/100
#----------------------------------REAL TIME-----------------------------------------
#real time:
time_real = tdms_file.object("pressures&temperature [10Hz]", "time [msec]") #milisec. [msec]********************msec or sec
time1 = time_real.data
#time1 = time1-time1[0]
time1=time1/1000       #1000 to convert msec to sec*******
#-----------------------------------------------------------

#--------------------------- TIME ------------------------------------------------
time = np.arange(det1.size) #(time for detectors)
time = time/(1.0*frequency)	#Time in seconds
#----------------------------------
#real time:
time_real = tdms_file.object("pressures&temperature [10Hz]", "time [msec]") #milisec. [msec]********************msec or sec
real_time = time_real.data
#time1 = time1-time1[0]
real_time =real_time /1000       #1000 to convert msec to sec*******************************
#------------------------------------------
start_time = tdms_file.object("experimental windows", "window start [msec]")  #************
time_start = start_time.data
time_start = time_start/1000
#print(time_start)
stop_time = tdms_file.object("experimental windows", "window stop [msec]")  #************
time_stop = stop_time.data
time_stop = time_stop/1000
#--------------------------PRESSURE----------------------------------------------------
channel_object = tdms_file.object("pressures&temperature [10Hz]", "channel 1")  #************ CHANNEL 1 should be read :D
pressure = channel_object.data
#---------------------------------
#adding artificial points in the beg.
det1[0]=30.01
det5[0]=30.01
det10[0]=30.01
#------------------PLOT ALL DETECTORS DATA---------------------
'''
plt.plot(time[:],det1[:] ,'-',label='dtc 1')
plt.plot(time[:],det5[:] ,'-',label='dtc 5')
plt.plot(time[:],det10[:] ,'-',label='dtc 10')
plt.title('signal from all detectors - data from file '+str(filenameS))
plt.xlabel('time [s]', rotation=0,fontsize=30)
plt.ylabel('voltage [V]', rotation=90,fontsize=30,labelpad=20)
plt.legend(frameon=False,loc=2)
fig = plt.figure(1)
# We define a fake subplot that is in fact only the plot.
plot = fig.add_subplot(111)
# We change the fontsize of minor ticks label
plot.tick_params(axis='both', which='major', labelsize=25)
plot.tick_params(axis='both', which='minor', labelsize=25)
plt.show()
'''
#-------PLOT PRESSURE--------
'''
plt.scatter(real_time[:], pressure[:])
plt.xlabel('Time [s]', rotation=0,fontsize=30)
plt.ylabel('Pressure [mbar]', rotation=90,fontsize=30,labelpad=20)
plt.legend(frameon=False,loc=2)
fig = plt.figure(1)
# We define a fake subplot that is in fact only the plot.
plot = fig.add_subplot(111)
# We change the fontsize of minor ticks label
plot.tick_params(axis='both', which='major', labelsize=25)
plot.tick_params(axis='both', which='minor', labelsize=25)
plt.show()
'''
#------------------a function---------------
#import numpy as np
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx
#-------------------------------------------
tmpr = np.zeros(len(time_start), dtype = object)
tmpr_dev = np.zeros(len(time_start), dtype = object)
p = np.zeros(len(time_start), dtype = object)
pp = np.zeros(len(time_start), dtype = object)
win_time = np.zeros(len(time_start), dtype = object)


itemindex_str = np.zeros(len(time_start), dtype = object)
itemindex_stp = np.zeros(len(time_start), dtype = object)


dtc1 = np.zeros(len(time_start), dtype = object)
dtc5 = np.zeros(len(time_start), dtype = object)
dtc10 = np.zeros(len(time_start), dtype = object)

drop1_psg_1_10 = np.zeros(len(time_start), dtype = object)
drop1_psg_1_5 = np.zeros(len(time_start), dtype = object)
drop2_psg_1_10 = np.zeros(len(time_start), dtype = object)
drop2_psg_1_5 = np.zeros(len(time_start), dtype = object)

drop1= np.zeros(len(time_start), dtype = object)
drop2= np.zeros(len(time_start), dtype = object)

choice= np.zeros(len(time_start), dtype = object)
#*******************************
artificial_values=30.01
ix = np.where(det1==artificial_values)  #check float > or ==

print("num of experiments:")
print(len(time_start))

#for i in range(0,len(time_start)):
for i in range(40,60):
    print(i)
    #dtc1[i] = np.absolute(det1[int(ix[0][i*10]+1):int(ix[0][i*10+1])]+(0-det1[1]))
    dtc1[i] = det1[int(ix[0][i*10]+1):int(ix[0][i*10+1])]+(0-det1[1])
    COM1 = ndimage.measurements.center_of_mass(dtc1[i]) #center of mass of signals, to seperate the two droplets
    dtc5[i] = np.absolute(det5[int(ix[0][i*10]+1):int(ix[0][i*10+1])]+(0-det5[1]))
    COM5 = ndimage.measurements.center_of_mass(dtc5[i],labels=None, index=None)
    dtc10[i] = np.absolute(det10[int(ix[0][i*10]+1):int(ix[0][i*10+1])]+(0-det10[1]))
    COM10 = ndimage.measurements.center_of_mass(dtc10[i],labels=None, index=None)

    if np.logical_not(np.isnan(COM1[0])) and np.logical_not(np.isnan(COM5[0])) and np.logical_not(np.isnan(COM10[0])):

        itemindex_str = find_nearest(time1, int(time_start[i]))

        itemindex_stp = find_nearest(time1, int(time_stop[i]))

        tmpr[i] = np.mean(temperature[itemindex_str+5:itemindex_stp-5])  #average temperature for each window (experiment)
        tmpr_dev[i] = temperature[itemindex_str+5]-temperature[itemindex_stp-5]

        win_time[i] = np.mean(time1[itemindex_str+5:itemindex_stp-5]) # win_time is the average real time of each window!

        p[i] = np.mean(pressure[itemindex_str+5:itemindex_stp-5]) #averaged pressure for each window (experiment)
    

        plt.plot(dtc1[i][:int(COM1[0])])
        #plt.plot(dtc5[i][:int(COM5[0])])
        #plt.plot(dtc10[i][:int(COM10[0])])
        plt.title('drop1')
        plt.show()

        plt.plot(dtc1[i][int(COM1[0]):])
        #plt.plot(dtc5[i][int(COM5[0]):])
        #plt.plot(dtc10[i][int(COM10[0]):])
        plt.title('drop2')
        plt.show()

        choice[i] = input('y/n?')
        print(choice[i])

        #===============================================
        #Droplet 1:
        #dtc1&10
        cc = correlate(dtc10[i][:int(COM10[0])],dtc1[i][:int(COM1[0])], mode='full')
        n=len(cc)
        cc = 2*cc/n
        dt1=1/frequency  #frequency: 20,000
        dur=n*dt1/2;
        d=linspace( -dur, dur, n )
        idx = argmax(cc)
        drop1_psg_1_10[i] = d[idx]

        #dtc1&5
        cc = correlate(dtc5[i][:int(COM5[0])],dtc1[i][:int(COM1[0])], mode='full')
        n=len(cc)
        cc = 2*cc/n
        dt1=1/frequency  #frequency: 20,000
        dur=n*dt1/2;
        d=linspace( -dur, dur, n )
        idx = argmax(cc)
        drop1_psg_1_5[i] = d[idx]
        #===============================================
        #Droplet 2:
        #dtc1&10
        cc = correlate(dtc10[i][int(COM10[0]):],dtc1[i][int(COM1[0]):], mode='full')
        n=len(cc)
        cc = 2*cc/n
        dt1=1/frequency  #frequency: 20,000
        dur=n*dt1/2;
        d=linspace( -dur, dur, n )
        idx = argmax(cc)
        drop2_psg_1_10[i] = d[idx]

        #dtc1&5
        cc = correlate(dtc5[i][int(COM5[0]):],dtc1[i][int(COM1[0]):], mode='full')
        n=len(cc)
        cc = 2*cc/n
        dt1=1/frequency  #frequency: 20,000
        dur=n*dt1/2;
        d=linspace( -dur, dur, n )
        idx = argmax(cc)
        drop2_psg_1_5[i] = d[idx]
    else:
        print('*******************************************')

    #===============================================
#---------------------write data to a csv file------------------------------------
df = pd.DataFrame({'pressure':p, 'drop1_psg_1_10':drop1_psg_1_10,'drop1_psg_1_5':drop1_psg_1_5,'drop2_psg_1_10': drop2_psg_1_10,'drop2_psg_1_5':drop2_psg_1_5, 'temperature':tmpr, 'temp_fluc': tmpr_dev, 'win_time': win_time, 'choice': choice}) #**********
df.to_csv('T(p)_%s.csv'%(filenameS))
#-------------------------------------------------------------------------
