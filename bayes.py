#!/usr/bin/env python3
# -- coding: utf-8 --

import serial 
import math
import sys

arduino = serial.Serial('/dev/ttyUSB0', 9600)
gridsize = 5
positions = [] 
sensor_data = [] 
grid = [[1, 2, 3,4,5], [6, 7, 8,9,10], [11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
onegridsize=46

try:
    while True:
        command = input("Enter command (F/B/L/R/S/U/q): ").upper()

        if command == 'Q':
            break
        elif command == 'F':
            arduino.write(b'F')
        elif command == 'B':
            arduino.write(b'B')
        elif command == 'L':
            arduino.write(b'L')
        elif command == 'R':
            arduino.write(b'R')
        elif command == 'S':
            arduino.write(b'S')
        elif command == 'U':
            arduino.write(b'S')
            arduino.write(b'U')
            
            measurement = arduino.readline().decode('utf-8').rstrip()
            if measurement=="":
                measurement=400.0
            print(measurement)
            position = int(input("\nEnter position: "))
            orien = input("Enter Pose: , Up/Down/Right/Left: ")
            posecurrent=(position,orien)
            positions.append(posecurrent)
            sensor_data.append(float(measurement))
        elif command == 'D':
            break
        else:
            print("Invalid command. Please enter F, B, L, R, S, U, or Q.")

finally:
    probmatrix = [[0 for i in range(len(sensor_data) + 1)] for j in range(gridsize*gridsize)]

    def dooperations(locationx,locationy,facing,targetx,targety,sensordata):
        diffrow = abs(locationx - targetx)
        diffcol = abs(locationy - targety)

        Probfree = 0.1
        Probocc =  0.8 
        
        if facing == 'Left' or facing == 'Right':
            if sensordata >= diffcol * onegridsize:
                Probabilityone = round(math.log(Probfree / (1 - Probfree)), 3)
            else:
                Probabilityone = round(math.log(Probocc / (1 - Probocc)), 3)
                
        elif facing == 'Up' or facing == 'Down':
            if sensordata >= diffrow * onegridsize:
                Probabilityone = round(math.log(Probfree / (1 - Probfree)), 3)
            else:
                Probabilityone = round(math.log(Probocc / (1 - Probocc)), 3)

        

        return Probabilityone
        

    for t in range(len(positions)):
        time = t+1
        row=0

        while(row < gridsize):
            col=0
            while(col < gridsize):
                #knowing current location according to array using the positions 
                if grid[row][col]==positions[t][0]:
                    locationx= row
                    locationy= col
                    break
                col=col+1
            row=row+1
        
        #checking if our robot is facing up, down, left, right
        if positions[t][1]=="Right":
            targetx= locationx
            targety= locationy+1
            while targety<gridsize and targety>=0:
                diff= abs(targety-locationy)
                target_element= grid[targetx][targety]
                if sensor_data[t] < diff * onegridsize:
                    probmatrix[target_element - 1][time] = probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    break
                elif sensor_data[t] >= diff * onegridsize:
                    probmatrix[target_element - 1][time] =  probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    
                targety=targety+1
        
        if positions[t][1]=="Left":
            targetx= locationx
            targety= locationy-1
            while targety<gridsize and targety>=0:
                diff= abs(targety-locationy)
                target_element= grid[targetx][targety]
                if sensor_data[t] < diff * onegridsize:
                    probmatrix[target_element - 1][time] = probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    break
                elif sensor_data[t] >= diff * onegridsize:
                    probmatrix[target_element - 1][time] =  probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    
                targety=targety-1
        
        if positions[t][1]=="Down":
            targetx= locationx+1
            targety= locationy
            while targetx<gridsize and targetx>=0:
                diff= abs(targetx-locationx)
                target_element= grid[targetx][targety]
                if sensor_data[t] <= diff * onegridsize:
                    probmatrix[target_element - 1][time] = probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    break
                elif sensor_data[t] >= diff * onegridsize:
                    probmatrix[target_element - 1][time] =  probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    
                targetx=targetx+1
        
        if positions[t][1]=="Up":
            pass
            targetx= locationx-1
            targety= locationy
            while targetx<gridsize and targetx>=0:
                diff= abs(targetx-locationx)
                target_element= grid[targetx][targety]
                if sensor_data[t] < diff * onegridsize:
                    probmatrix[target_element - 1][time] = probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    break
                elif sensor_data[t] >= diff * onegridsize:
                    probmatrix[target_element - 1][time] =  probmatrix[target_element-1][time-1] + dooperations(locationx,locationy,positions[t][1],targetx,targety,sensor_data[t]) -0 
                    
                targetx=targetx-1
        
        for var in range(gridsize*gridsize):
            if(probmatrix[var][time] == 0):
                probmatrix[var][time] = probmatrix[var][time - 1]
        
        
    lastcolprob=[]
    finalprob=[]
    for i in range(gridsize*gridsize):
        lastcolprob.append((probmatrix[i][len(sensor_data)]))

    for i in lastcolprob:
        calprob = 1 - 1 / (1 + math.exp(i))
        finalprob.append(round(calprob,3))
    print(probmatrix)
    for i in range(gridsize*gridsize):
        print("Probability of state ", i+1, " being occupied is:", finalprob[i])

        arduino.close()