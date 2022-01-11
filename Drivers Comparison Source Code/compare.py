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
import plotly
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.offline import init_notebook_mode
import glob
import statistics

def plots(f_path_g, f_path_m, acc, vel, d):
    # Data Buffers for Encoder readings, velocity and acceleration calculations
    #g - grbl
    #m - marlin

    encoder_1g = []
    encoder_2g = []
    encoder_3g = []
    vel_enc_1g = []
    vel_enc_2g = []
    vel_enc_3g = []
    acc_enc_1g = []
    acc_enc_2g = []
    acc_enc_3g = []

    encoder_1m = []
    encoder_2m = []
    encoder_3m = []
    vel_enc_1m = []
    vel_enc_2m = []
    vel_enc_3m = []
    acc_enc_1m = []
    acc_enc_2m = []
    acc_enc_3m = []

    time_axis_g = []
    time_axis_m = []

    encoder_PPR_res = 4096
    encoder_CPR_res = 4 * encoder_PPR_res
    z_axis = False
    XY_axis = True
    lever_reduction = 42
    XY_lead_screw_pitch = 14
    Z_lead_screw_pitch = 8
    XY_axis_mm_per_count = XY_lead_screw_pitch / encoder_CPR_res
    z_axis_mm_per_count = Z_lead_screw_pitch / (encoder_CPR_res * lever_reduction)

    time_tg = 0
    time_tm = 0
    sampling_period = 0.0002  # sampling_period of 200 microseconds

    ##-----------------------------------`----------------------------------------------------------------------------------------
    FILENAME_g = f_path_g
    FILENAME_m = f_path_m

    FILENAME_NEW_g = r'/home/morphle/Desktop/GXNEW.log'
    FILENAME_NEW_m = r'/home/morphle/Desktop/MXNEW.log'

    ##grbl-----------------------------------------------------------------
    ##GRBL Data cleaning
    # To remove the blank lines from the file and write the data to a .log file

    with open(FILENAME_g) as infile, open(FILENAME_NEW_g, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output

    f = open(FILENAME_NEW_g, mode='r')
    # Write the data to separate array
    for row in f:
        row = row.split('\t')
        time_axis_g.append(time_tg)
        if z_axis:
            encoder_3g.append(float(int(row[2]) * z_axis_mm_per_count))
        else:
            encoder_3g.append(0)
        encoder_1g.append(float(int(row[0]) * XY_axis_mm_per_count))
        encoder_2g.append(float(int(row[1]) * XY_axis_mm_per_count))

        time_tg += sampling_period

    #remove initial zeros
    while True:
        for i in range(len(encoder_1g)):
            if(encoder_1g[0]==0):
                encoder_1g.pop(0)
            else:
                break
        for i in range(len(encoder_2g)):
            if(encoder_2g[0]==0):
                encoder_2g.pop(0)
            else:
                break
        break

    if z_axis:
        data_range_g = len(encoder_3g)
    else:
        data_range_g = len(encoder_2g)

    ##MARLIN-------------------------------------------------------------
    ##MARLIN Data cleaning
    # To remove the blank lines from the file and write the data to a .log file

    with open(FILENAME_m) as infile, open(FILENAME_NEW_m, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output

    f = open(FILENAME_NEW_m, mode='r')
    # Write the data to separate array
    for row in f:
        row = row.split('\t')
        time_axis_m.append(time_tm)
        if z_axis:
            encoder_3m.append(float(int(row[2]) * z_axis_mm_per_count))
        else:
            encoder_3m.append(0)
        encoder_1m.append(float(int(row[0]) * XY_axis_mm_per_count))
        encoder_2m.append(float(int(row[1]) * XY_axis_mm_per_count))

        time_tm += sampling_period
        
    #remove initial zeros

    while True:
        for i in range(len(encoder_1m)):
            if(encoder_1m[0]==0):
                encoder_1m.pop(0)
            else:
                break
        for i in range(len(encoder_2m)):
            if(encoder_2m[0]==0):
                encoder_2m.pop(0)
            else:
                break
        break

    if z_axis:
        data_range_m = len(encoder_3m)
    else:
        data_range_m = len(encoder_2m)

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
        # plt.plot(x_axis_idl, y_axis_idl, 'tab:red')
        ##    plt.plot([0,0.008333], [0, 83.33], 'tab:red')
        ##    plt.plot([0.008333,0.32733], [83.33,83.33], 'tab:red')
        ##    plt.plot([0.32733, 0.336], [83.33, 0], 'tab:red')
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
    # Plots Position and Velocity profiles for marlin and grbl

    def compare(x_axis_vg1, y_axis_tg1, x_axis_vm1, y_axis_tm1, x_axis_pg1, y_axis_tpg1,x_axis_pm1, y_axis_tpm1,x_axis_vg2, y_axis_tg2, x_axis_vm2, y_axis_tm2, x_axis_pg2,y_axis_tpg2 ,x_axis_pm2, y_axis_tpm2):
        # plt.subplot(1,2,1)
        # plt.title("Velocity(mm/sec) vs time(sec)")
        # plt.ylabel("v (mm/s)")
        # plt.xlabel("t (sec)")
        # plt.plot(y_axis_tg,x_axis_vg, 'tab:orange', label="grbl")
        # plt.plot( y_axis_tm,x_axis_vm, 'tab:red', label="marlin")
        # plt.grid(color='black', linestyle='--', linewidth=1)
        # plt.legend()
        #
        # plt.subplot(1,2,2)
        # plt.title("Position(mm) vs time(sec)")
        # plt.ylabel("Position (mm)")
        # plt.xlabel("time (sec)")
        # plt.plot(y_axis_tg,x_axis_pg[0:len(y_axis_tg)], 'tab:orange', label="grbl")
        # plt.plot( y_axis_tm,x_axis_pm[0:len(y_axis_tm)], 'tab:red', label="marlin")
        # plt.grid(color='black', linestyle='--', linewidth=1)
        # plt.legend()
        #
        # plt.suptitle("Acceleration: %s Velocity: %s stroke: %s"%(acc, vel, d))
        # # plt.show()
        # plt.savefig("Acceleration_%s_Velocity_%s_stroke_%s.png"%(acc, vel, d))


        from plotly.subplots import make_subplots

        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(
            go.Scatter(x=y_axis_tg1, y=x_axis_vg1,  name="GRBL"),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=y_axis_tm1, y=x_axis_vm1, name="MARLIN"),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tpg1, y=x_axis_pg1[0:len(y_axis_tpg1)], name="GRBL"),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tpm1,y=x_axis_pm1[0:len(y_axis_tpm1)], name="MARLIN"),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tg2, y=x_axis_vg2, name="GRBL"),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=y_axis_tm2, y=x_axis_vm2, name="MARLIN"),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tpg2, y=x_axis_pg2[0:len(y_axis_tpg2)], name="GRBL"),
            row=2, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tpm2, y=x_axis_pm2[0:len(y_axis_tpm2)], name="MARLIN"),
            row=2, col=2
        )

        fig['layout']['xaxis']['title'] = 'Time (sec)'
        fig['layout']['xaxis2']['title'] = 'Time (sec)'
        fig['layout']['yaxis']['title'] = 'Velocity (mm/sec) - enc1'
        fig['layout']['yaxis2']['title'] = 'Position (mm) - enc1'
        fig['layout']['xaxis3']['title'] = 'Time (sec)'
        fig['layout']['xaxis4']['title'] = 'Time (sec)'
        fig['layout']['yaxis3']['title'] = 'Velocity (mm/sec) - enc2'
        fig['layout']['yaxis4']['title'] = 'Position (mm) - enc2'
        fig.update_layout(height=1800, width=1800, title_text="Acceleration: %s Velocity: %s stroke: %s"%(acc, vel, d))
        # fig.write_html("/home/morphle/Encoder_Data/plots/%s%s%s.html"%(acc, vel, d))
        fig.show()


    ##---------------------------------------------------------------------------------------------------------------------------

    # Velocity calculation GRBL
    for i in range(len(encoder_1g)):

        if i < len(encoder_1g) - 1:
            vel_enc_1g.append((encoder_1g[i + 1] - encoder_1g[i]) / sampling_period)


    for i in range(len(encoder_2g)):

        if i < len(encoder_2g) - 1:
            vel_enc_2g.append((encoder_2g[i + 1] - encoder_2g[i]) / sampling_period)

   ##---------------------------------------------------------------------------------------------------------------------------
    # Velocity calculation MARLIN

    for i in range(len(encoder_1m)):

        if i < len(encoder_1m) - 1:
            vel_enc_1m.append((encoder_1m[i + 1] - encoder_1m[i]) / sampling_period)


    for i in range(len(encoder_2m)):

        if i < len(encoder_2m) - 1:
            vel_enc_2m.append((encoder_2m[i + 1] - encoder_2m[i]) / sampling_period)

    ##---------------------------------------------------------------------------------------------------------------------------
    #Data striping

    time_interval = 0.01 #10ms
    group = 50

    #position GRBL enc1
    new_encoder_1g = []
    time_encoder_1g = []

    itr_num = int(math.floor(len(encoder_1g)/group))

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_encoder_1g.append(statistics.mean(encoder_1g[i:end_val]))
        time_encoder_1g.append(statistics.mean(time_axis_g[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_1g)):
        new_encoder_1g.append(encoder_1g[j])
        time_encoder_1g.append(time_axis_g[j])

    #position GRBL enc2
    new_encoder_2g = []
    time_encoder_2g = []

    itr_num = math.floor(len(encoder_2g)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i+group
        new_encoder_2g.append(statistics.mean(encoder_2g[i:end_val]))
        time_encoder_2g.append(statistics.mean(time_axis_g[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_2g)):
        new_encoder_2g.append(encoder_2g[j])
        time_encoder_2g.append(time_axis_g[j])

    #position MARLIN enc1
    new_encoder_1m = []
    time_encoder_1m = []

    itr_num = math.floor(len(encoder_1m)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_encoder_1m.append(statistics.mean(encoder_1m[i:end_val]))
        time_encoder_1m.append(statistics.mean(time_axis_m[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_1m)):
        new_encoder_1m.append(encoder_1m[j])
        time_encoder_1m.append(time_axis_m[j])

    #position MARLIN enc2
    new_encoder_2m = []
    time_encoder_2m = []

    itr_num = math.floor(len(encoder_2m)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_encoder_2m.append(statistics.mean(encoder_2m[i:end_val]))
        time_encoder_2m.append(statistics.mean(time_axis_m[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_2m)):
        new_encoder_2m.append(encoder_2m[j])
        time_encoder_2m.append(time_axis_m[j])

    #Velocity GRBL enc1
    new_vel_enc_1g = []
    time_vel_enc_1g = []

    itr_num = math.floor(len(vel_enc_1g)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_1g.append(statistics.mean(vel_enc_1g[i:end_val]))
        time_vel_enc_1g.append(statistics.mean(time_axis_g[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_1g)):
        new_vel_enc_1g.append(vel_enc_1g[j])
        time_vel_enc_1g.append(time_axis_g[j])

    #Velocity GRBL enc2
    new_vel_enc_2g = []
    time_vel_enc_2g = []

    itr_num = math.floor(len(vel_enc_2g)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_2g.append(statistics.mean(vel_enc_2g[i:end_val]))
        time_vel_enc_2g.append(statistics.mean(time_axis_g[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_2g)):
        new_vel_enc_2g.append(vel_enc_2g[j])
        time_vel_enc_2g.append(time_axis_g[j])

    #Velocity MARLIN enc1
    new_vel_enc_1m = []
    time_vel_enc_1m = []

    itr_num = math.floor(len(vel_enc_1m)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_1m.append(statistics.mean(vel_enc_1m[i:end_val]))
        time_vel_enc_1m.append(statistics.mean(time_axis_m[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_1m)):
        new_vel_enc_1m.append(vel_enc_1m[j])
        time_vel_enc_1m.append(time_axis_m[j])

    #Velocity MARLIN enc2
    new_vel_enc_2m = []
    time_vel_enc_2m = []

    itr_num = math.floor(len(vel_enc_2m)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_2m.append(statistics.mean(vel_enc_2m[i:end_val]))
        time_vel_enc_2m.append(statistics.mean(time_axis_m[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_2m)):
        new_vel_enc_2m.append(vel_enc_2m[j])
        time_vel_enc_2m.append(time_axis_m[j])

    ##---------------------------------------------------------------------------------------------------------------------------
    #print curves

    ####low pass filter
    ##
    # n = 30  # the larger n is, the smoother curve will be
    # b = [1.0 / n] * n
    # a = 1
    # xxx = lfilter(b,a,vel_enc_1)
    ##yyy = lfilter(b,a,vel_enc_2)

    time_axis = []

    if (time_axis_g > time_axis_m):
        time_axis = time_axis_g
    else:
        time_axis = time_axis_m

    # n = 30  # the larger n is, the smoother curve will be
    # b = [1.0 / n] * n
    # a = 1
    # xxx1 = lfilter(b,a,vel_enc_1g)
    # yyy1 = lfilter(b,a,vel_enc_1m)
    # zzz1 = lfilter(b,a,encoder_1g)
    # fff1 = lfilter(b,a,encoder_1m)
    #
    # xxx2 = lfilter(b,a,vel_enc_2g)
    # yyy2 = lfilter(b,a,vel_enc_2m)
    # zzz2 = lfilter(b,a,encoder_2g)
    # fff2 = lfilter(b,a,encoder_2m)

    # group = 3
    # xxx1 = np.array(vel_enc_1g).reshape(-1, group).mean()
    # yyy1 = np.array(vel_enc_1m).reshape(-1, group).mean(axis=1)
    # zzz1 = np.array(encoder_1g).reshape(-1, group).mean(axis=1)
    # fff1 = np.array(encoder_1m).reshape(-1, group).mean(axis=1)
    #
    # xxx2 = np.array(vel_enc_2g).reshape(-1, group).mean(axis=1)
    # yyy2 = np.array(vel_enc_2m).reshape(-1, group).mean(axis=1)
    # zzz2 = np.array(encoder_2g).reshape(-1, group).mean(axis=1)
    # fff2 = np.array(encoder_2m).reshape(-1, group).mean(axis=1)
    #
    # ttt = np.array(time_axis).reshape(-1, group).mean(axis=1)
    # print(len(vel_enc_1g))
    # print(len(vel_enc_1m))
    # print(len(vel_enc_2g))
    # print(len(vel_enc_2m))
    #
    # print(len(encoder_1g))
    # print(len(encoder_1m))
    # print(len(encoder_2g))
    # print(len(encoder_2m))

    compare(new_vel_enc_1g, time_vel_enc_1g[0:len(new_vel_enc_1g)], new_vel_enc_1m, time_vel_enc_1m[0:len(new_vel_enc_1m)], new_encoder_1g, time_encoder_1g[0:len(new_encoder_1g)],new_encoder_1m, time_encoder_1m[0:len(new_encoder_1m)]
            ,new_vel_enc_2g, time_vel_enc_2g[0:len(new_vel_enc_2g)], new_vel_enc_2m, time_vel_enc_2m[0:len(new_vel_enc_2m)], new_encoder_2g, time_encoder_2g[0:len(new_encoder_2g)],new_encoder_2m, time_encoder_2m[0:len(new_encoder_2m)])
