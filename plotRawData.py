# -*- coding: utf-8 -*-
#!/usr/bin/env python


#################################################################
# Author: Rajashekar Reddy
# Date created: 12th June 2014 
# 
# This code takes the data from a raw data file and plots...
# ...the graphs
#################################################################

import csv
import argparse
import pylab as plt


class PacketFromDevice(object): 
    pass

class SensorDataGlucose(PacketFromDevice):
    
    def __init__(self, row_data): 
        
        self.time_stamp = int(row_data[0])
        self.channel_values = { "CLEAR": int(row_data[1]), "RED":int(row_data[2]), "GREEN":int(row_data[3]), "BLUE":int(row_data[4])}
        self.sequential_number = int(row_data[5])
        self.LED_color = str(row_data[6])
        self.temperature = float(row_data[7])
        self.battery_voltage = float(row_data[8])
        

# Calls extract_raw_dat function and plots the graphs
def plot_the_data(parsedArgs):
    
    x = []
    y_red = []
    y_blue = []
    y_green  = []

    sensor_data_list =  extract_raw_data(parsedArgs)

    for i2 in range(len(sensor_data_list)):
        x.append(sensor_data_list[i2].time_stamp - sensor_data_list[0].time_stamp)
        y_red.append(sensor_data_list[i2].channel_values["RED"])
        y_blue.append(sensor_data_list[i2].channel_values["BLUE"])
        y_green.append(sensor_data_list[i2].channel_values["GREEN"])

    fig = plt.figure()
    fig.suptitle('Sensor Values vs Time')
    plt.subplot(3,1,1)
    plt.plot(x,y_red,'red')
    plt.ylabel('Red Channel')
    plt.subplot(3,1,2)
    plt.plot(x,y_blue,'blue')
    plt.ylabel('Blue Channel')
    plt.subplot(3,1,3)
    plt.plot(x,y_green,'green')
    plt.ylabel('Green Channel')
    plt.xlabel('Time')
    plt.show()
    

# Extracts the data from raw_data_file and stores it as objects of...
# SensorDataGlucose Class
def extract_raw_data(parsedArgs):
    
    with open(parsedArgs['raw_data_file'],'rU') as f:

        raw_data_reader = csv.reader(f)
        raw_data_reader.next() # to skip table titles
        sensor_data_list = list()

        for row in raw_data_reader:
            
            row_data = list()
            for i1 in range(len(row)):
                row_data.append(row[i1])

            sensor_data = SensorDataGlucose(row_data)
            sensor_data_list.append(sensor_data)
            
    return sensor_data_list


# main function, parses the arguments and calls...
# plot_the_data function.

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_data_file')
    
    parsedArgs = vars(parser.parse_args())
    
    plot_the_data(parsedArgs)
