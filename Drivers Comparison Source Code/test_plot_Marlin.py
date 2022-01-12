# Author: Nikunj Parmar, DarkerKnight
# Plotting position, velocity and acceleration graphs for encoder data to analyse the motion profile
# Encoder resolution = 2048 PPR, therefore CPR = 4 x PPR
# mm per count = 1.7 microns

import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np
from numpy import ndarray
import csv
import math

# Data Buffers for Encoder readings, velocity and acceleration calculations
encoder_1 = []
encoder_2 = []
encoder_3 = []
vel_enc_1 = []
vel_enc_2 = []
vel_enc_3 = []
acc_enc_1 = []
acc_enc_2 = []
acc_enc_3 = []
time_axis = []
encoder_PPR_res = 4096
encoder_CPR_res = 4 * encoder_PPR_res
z_axis = False
XY_axis = True
lever_reduction = 42
XY_lead_screw_pitch = 14
Z_lead_screw_pitch = 8
XY_axis_mm_per_count = XY_lead_screw_pitch / encoder_CPR_res
z_axis_mm_per_count = Z_lead_screw_pitch / (encoder_CPR_res * lever_reduction)
time_t = 0
sampling_period = 0.0002  # sampling_period of 200 microseconds

#Required Information
##microstepping = 16
##distance_travelled_mm = 
##ideal_steps_per_rev = 200 * microstepping
#ideal_count = round(distance_travelled_mm / mm_per_count)
# ideal_steps_per_mm = ideal_steps_per_rev / lead_screw_pitch
# set_steps_per_rev = round(ideal_steps_per_mm)
# round_off_error = set_steps_per_rev - ideal_steps_per_mm
# actual_steps_per_rev = set_steps_per_rev * lead_screw_pitch
# correction_factor = actual_steps_per_rev / ideal_steps_per_rev
# expected_distance_travelled = ideal_count * correction_factor * mm_per_count

##-----------------------------------`----------------------------------------------------------------------------------------
#Define X and Y (in mm)

max_vel = 50 #mm/sec #end-effector's max valocity
a = 400 #mm/sec^2
t = sampling_period #sec
d = 40

theta = 53

if (d>0):
    dx = (math.cos(math.radians(theta))) * d
    dy = (math.sin(math.radians(theta))) * d

jx = 0 #max jerk in mm/sec
jy = 0 #max jerk in mm/sec

if (dx !=0 and dy!=0):
    
    theta_rad = math.atan(dx/dy)

    max_vy = (math.cos(theta_rad)) * max_vel
    max_vx = (math.sin(theta_rad)) * max_vel
else:
    max_vy = max_vel
    max_vx = max_vel

##---------------------------------------------------------------------------------------------------------------------------
#Ideal Value calculation - X axis

idl_val_velo_1 = []
idl_val_dis_1 = []
t1 = (max_vx - jx)/a #Assumption: starting velocity = max jerk value
d1 = jx*t1 + (0.5)*a*(t1**2)

v2 = max_vx
v3 = v2 - jx

t32 = v3/a #t32 = t3-t2

d3 = v3*t32 - (0.5)*a*(t32**2)
d2 = dx-(d1+d3)

t2 = d2/v2 + t1

t_total = t2+t32

if dx>(d1+d3): ##Trapezoidal curve
    while t <= t1:
        # +ve acceleration
        v = jx + a * t #velocity cal
        idl_val_velo_1.append(v)
        s = jx*t + (0.5)*a*(t**2) #position cal
        idl_val_dis_1.append(s)
        t = t + 0.0002

    d_x = d1-(max_vx * t)

    while t1 < t and t < t2:
        # zero acceleration
        idl_val_velo_1.append(max_vx)

        s = d_x + (max_vx * t)
        idl_val_dis_1.append(s)
        t = t + 0.0002
    v0 = max_vx - jx
    tt = sampling_period
    s0 = s
    idl_val_velo_1.append(v0)
      
    while t<t_total:
        # -ve acceleration
        v = v0 - (a * tt)
        idl_val_velo_1.append(v)
        
        
        s = (v0 * tt) - ((0.5)*a*(tt**2))
        s = s + s0
        idl_val_dis_1.append(s)
        t = t + 0.0002
        tt = tt + 0.0002

else: ## Triangular curve for dx<2*d1

    #qaudratic equation parameters
    aa = a
    bb = jx
    cc = -dx
    
    t11 = (-bb + ((bb**2)-(4*aa*cc))**0.5)/(2 * aa)
    t12 = (-bb - ((bb**2)-(4*aa*cc))**0.5)/(2 * aa)
    
    if t11>0:
        t1 = t11
    else:
        t1 = t12

    if t11>0 and t12>0:
        print("Error in time calculation")
        exit()

    t_total = 2*t1
  
    while t<t1:
        v = jx + a * t #velocity cal
        idl_val_velo_1.append(v)

        s = jx*t + (0.5)*a*(t**2) #position cal
        idl_val_dis_1.append(s)
        t = t + 0.0002        

    v2 = v
    v3 = v2-jx
    tt = sampling_period
    s0 = s
    ##change here
    idl_val_velo_1.append(v3)
    
    while t<t_total:
        # -ve acceleration
        v = v3 - (a * tt)
        idl_val_velo_1.append(v)

        s = (v3 * tt) - ((0.5)*a*(tt**2))
        s = s + s0
        idl_val_dis_1.append(s)
        t = t + 0.0002
        tt = tt + 0.0002        
#---------------------------------------------------------------------------------------------------------------------------

#Ideal Value calculation - Y axis
t = sampling_period
idl_val_velo_2 = []
idl_val_dis_2 = []
t1 = (max_vy - jy)/a #Assumption: starting velocity = max jerk value
d1 = jy*t1 + (0.5)*a*(t1**2)

v2 = max_vy
v3 = v2 - jy

t32 = v3/a #t32 = t3-t2

d3 = v3*t32 - (0.5)*a*(t32**2)
d2 = dy-(d1+d3)

t2 = d2/v2 + t1

t_total = t2+t32

if dy>(d1+d3): ##Trapezoidal curve

    while t <= t1:
        # +ve acceleration
        v = jy + a * t #velocity cal
        idl_val_velo_2.append(v)

        s = jy*t + (0.5)*a*(t**2) #position cal
        idl_val_dis_2.append(s)
        t = t + 0.0002

    d_x = d1-(max_vy * t)

    while t1 < t and t < t2:
        # zero acceleration
        idl_val_velo_2.append(max_vy)

        s = d_x + (max_vy * t)
        idl_val_dis_2.append(s)
        t = t + 0.0002

    v0 = max_vy - jy
    tt = sampling_period
    s0 = s
    idl_val_velo_2.append(v0)
   
    while t<t_total:
        # -ve acceleration
        v = v0 - (a * tt)
        idl_val_velo_2.append(v)      
        s = (v0 * tt) - ((0.5)*a*(tt**2))
        s = s + s0
        idl_val_dis_2.append(s)
        t = t + 0.0002
        tt = tt + 0.0002

else: ## Triangular curve for d<2*d1

    #qaudratic equation parameters
    aa = a
    bb = jy
    cc = -dy
    
    t11 = (-bb + ((bb**2)-(4*aa*cc))**0.5)/(2 * aa)
    t12 = (-bb - ((bb**2)-(4*aa*cc))**0.5)/(2 * aa)
    
    if t11>0:
        t1 = t11
    else:
        t1 = t12

    if t11>0 and t12>0:
        print("Error in time calculation")
        exit()

    t_total = 2*t1

    while t<t1:
        v = jy + a * t #velocity cal
        idl_val_velo_2.append(v)

        s = jy*t + (0.5)*a*(t**2) #position cal
        idl_val_dis_2.append(s)
        t = t + 0.0002        

    v2 = v
    v3 = v2-jy
    tt = sampling_period
    s0 = s
##    change here
    idl_val_velo_2.append(v3)
    
    while t<t_total:
        # -ve acceleration
        v = v3 - (a * tt)
        idl_val_velo_2.append(v)

        s = (v3 * tt) - ((0.5)*a*(tt**2))
        s = s + s0
        idl_val_dis_2.append(s)
        t = t + 0.0002
        tt = tt + 0.0002        
    
##---------------------------------------------------------------------------------------------------------------------------

FILENAME = r'/home/morphle/Encoder_Data/Marlin_Driver_testing_data/TMC2209_V2/MST16/Acc_400/50_mm_sec/40mm/2021-04-16 14_24_26.993555.log'
FILENAME_NEW = r'/home/morphle/Desktop/GX40.log'
# To remove the blank lines from the file and write the data to a .txt file
with open(FILENAME) as infile, open(
        FILENAME_NEW, 'w') as outfile:
    for line in infile:
        if not line.strip():
            continue  # skip the empty line
        outfile.write(line)  # non-empty line. Write it to output

f = open(FILENAME_NEW, mode='r')
# Write the data to separate array
for row in f:
    row = row.split('\t')
    time_axis.append(time_t)
    if z_axis:
        encoder_3.append(float(int(row[2]) * z_axis_mm_per_count))
    else:
        encoder_3.append(0)
    encoder_1.append(float(int(row[0]) * XY_axis_mm_per_count))
    encoder_2.append(float(int(row[1]) * XY_axis_mm_per_count))

    time_t += sampling_period

if z_axis:
    data_range = len(encoder_3)
else:
    data_range = len(encoder_2)

##---------------------------------------------------------------------------------------------------------------------------
# Position Graph

def position_plot(x_axis, y_axis, x_axis_idl, y_axis_idl):
    plt.title('Travel Profile')
    plt.xlabel('Time (second)')
    plt.ylabel('Position(mm)')
    plt.plot(x_axis, y_axis, 'tab:orange')
    plt.plot(x_axis_idl, y_axis_idl, 'tab:red')
    plt.grid(color='black', linestyle='--', linewidth=1)
    plt.show()
##---------------------------------------------------------------------------------------------------------------------------
# Plots Velocity Profile
def velocity_plot(x_axis, y_axis, x_axis_idl, y_axis_idl):
    plt.title('Velocity Profile')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity(mm/s)')
    plt.plot(x_axis, y_axis, 'tab:green')
    plt.plot(x_axis_idl, y_axis_idl, 'tab:red')
    plt.grid(color='black', linestyle='--', linewidth=1)
    plt.show()
##---------------------------------------------------------------------------------------------------------------------------
# Plots Acceleration Profile
def acceleration_plot(x_axis, y_axis):
    plt.title('Acceleration Profile')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Acceleration(mm/s/s)')
    plt.plot(x_axis, y_axis, 'tab:red')
    plt.grid(color='black', linestyle='--', linewidth=1)
    plt.show()

##---------------------------------------------------------------------------------------------------------------------------
# Plots all Position, Velocity and Acceleration plots for both the encoder
def side_by_side_plot(x_axis, y_axis_00, y_axis_01, y_axis_02, y_axis_10, y_axis_11, y_axis_12, y_axis_20, y_axis_21,
                      y_axis_22):
    fig, axs = plt.subplots(3, 3)
    axs[0, 0].set_title('X Motor(Encoder 1)')
    axs[0, 0].set_xlabel('Time (microseconds)')
    axs[0, 0].set_ylabel('Position (mm)')
    axs[0, 0].plot(x_axis, y_axis_00, 'tab:orange')
    axs[0, 0].grid(color='black', linestyle='--', linewidth=1)

    axs[0, 1].set_title('Y Motor(Encoder 2)')
    axs[0, 1].set_xlabel('Time (microseconds)')
    axs[0, 1].plot(x_axis, y_axis_01, 'tab:orange')
    axs[0, 1].grid(color='black', linestyle='--', linewidth=1)

    axs[0, 2].set_title('Z Motor(Encoder 3)')
    axs[0, 2].set_xlabel('Time (microseconds)')
    axs[0, 2].plot(x_axis, y_axis_02, 'tab:orange')
    axs[0, 2].grid(color='black', linestyle='--', linewidth=1)

    axs[1, 0].set_xlabel('Time (microseconds)')
    axs[1, 0].set_ylabel('Velocity (mm/s)')
    axs[1, 0].plot(x_axis, y_axis_10, 'tab:green')
    axs[1, 0].grid(color='black', linestyle='--', linewidth=1)

    axs[1, 1].set_xlabel('Time (microseconds)')
    axs[1, 1].plot(x_axis, y_axis_11, 'tab:green')
    axs[1, 1].grid(color='black', linestyle='--', linewidth=1)

    axs[1, 2].set_xlabel('Time (microseconds)')
    axs[1, 2].plot(x_axis, y_axis_12, 'tab:green')
    axs[1, 2].grid(color='black', linestyle='--', linewidth=1)

    axs[2, 0].set_xlabel('Time (microseconds)')
    axs[2, 0].set_ylabel('Acceleration (mm/s/s)')
    axs[2, 0].plot(x_axis, y_axis_20, 'tab:red')
    axs[2, 0].grid(color='black', linestyle='--', linewidth=1)

    axs[2, 1].set_xlabel('Time (microseconds)')
    axs[2, 1].plot(x_axis, y_axis_21, 'tab:red')
    axs[2, 1].grid(color='black', linestyle='--', linewidth=1)

    axs[2, 2].set_xlabel('Time (microseconds)')
    axs[2, 2].plot(x_axis, y_axis_22, 'tab:red')
    axs[2, 2].grid(color='black', linestyle='--', linewidth=1)

    plt.show()
##---------------------------------------------------------------------------------------------------------------------------
# Velocity calculation
for i in range(data_range):
    if i < data_range - 1:
        if z_axis:
            vel_enc_3.append((encoder_3[i + 1] - encoder_3[i]) / sampling_period)
        else:
            vel_enc_3.append(0)
        vel_enc_1.append((encoder_1[i + 1] - encoder_1[i]) / sampling_period)
        vel_enc_2.append((encoder_2[i + 1] - encoder_2[i]) / sampling_period)
    else:
        vel_enc_3.append(vel_enc_3[i - 1])
        vel_enc_1.append(vel_enc_2[i - 1])
        vel_enc_2.append(vel_enc_3[i - 1])
##---------------------------------------------------------------------------------------------------------------------------
# Acceleration calculation
for i in range(data_range):
    if i < data_range - 1:
        if z_axis:
            acc_enc_3.append((vel_enc_3[i + 1] - vel_enc_3[i]) / sampling_period)
        else:
            acc_enc_3.append(0)
        acc_enc_1.append((vel_enc_1[i + 1] - vel_enc_1[i]) / sampling_period)
        acc_enc_2.append((vel_enc_2[i + 1] - vel_enc_2[i]) / sampling_period)
    else:

        acc_enc_3.append(acc_enc_3[i - 1])
        acc_enc_1.append(acc_enc_1[i - 1])
        acc_enc_2.append(acc_enc_2[i - 1])

##---------------------------------------------------------------------------------------------------------------------------
#print curves
data_range = len(idl_val_dis_1)
data_range2 = len(idl_val_dis_2)

####low pass filter
##
# n = 30  # the larger n is, the smoother curve will be
# b = [1.0 / n] * n
# a = 1
# xxx = lfilter(b,a,vel_enc_1)
##yyy = lfilter(b,a,vel_enc_2)
velocity_plot(time_axis, vel_enc_1, time_axis[0:data_range+1], idl_val_velo_1)
position_plot(time_axis, encoder_1, time_axis[0:data_range],idl_val_dis_1 )
