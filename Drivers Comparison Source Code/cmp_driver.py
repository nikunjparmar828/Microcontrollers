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
from plotly.subplots import make_subplots

def plots(f_path_1, f_path_2,f_path_3, acc, vel, d):

    encoder_11 = []
    encoder_21 = []
    encoder_31 = []
    vel_enc_11 = []
    vel_enc_21 = []
    vel_enc_31 = []


    encoder_12 = []
    encoder_22 = []
    encoder_32 = []
    vel_enc_12 = []
    vel_enc_22 = []
    vel_enc_32 = []

    encoder_13 = []
    encoder_23 = []
    encoder_33 = []
    vel_enc_13 = []
    vel_enc_23 = []
    vel_enc_33 = []

    time_axis_1 = []
    time_axis_2 = []
    time_axis_3 = []

    encoder_PPR_res = 4096
    encoder_CPR_res = 4 * encoder_PPR_res
    z_axis = False
    XY_axis = True
    lever_reduction = 42
    XY_lead_screw_pitch = 14
    Z_lead_screw_pitch = 8
    XY_axis_mm_per_count = XY_lead_screw_pitch / encoder_CPR_res
    z_axis_mm_per_count = Z_lead_screw_pitch / (encoder_CPR_res * lever_reduction)

    time_t1 = 0
    time_t2 = 0
    time_t3 = 0



    sampling_period = 0.0002  # sampling_period of 200 microseconds

    ##-----------------------------------`----------------------------------------------------------------------------------------



    FILENAME_1 = f_path_1
    FILENAME_2 = f_path_2
    FILENAME_3 = f_path_3

    FILENAME_NEW_1 = r'/home/morphle/Desktop/NEW1.log'
    FILENAME_NEW_2 = r'/home/morphle/Desktop/NEW2.log'
    FILENAME_NEW_3 = r'/home/morphle/Desktop/NEW3.log'

    ##1st driver-----------------------------------------------------------------
    ##Data cleaning
    # To remove the blank lines from the file and write the data to a .log file

    with open(FILENAME_1) as infile, open(FILENAME_NEW_1, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output

    f = open(FILENAME_NEW_1, mode='r')
    # Write the data to separate array
    for row in f:
        row = row.split('\t')
        time_axis_1.append(time_t1)
        if z_axis:
            encoder_31.append(float(int(row[2]) * z_axis_mm_per_count))
        else:
            encoder_31.append(0)
        encoder_11.append(float(int(row[0]) * XY_axis_mm_per_count))
        encoder_21.append(float(int(row[1]) * XY_axis_mm_per_count))

        time_t1 += sampling_period


    #remove initial zeros

    while True:
        for i in range(len(encoder_11)):
            if(encoder_11[0]==0):
                encoder_11.pop(0)
            else:
                break
        for i in range(len(encoder_21)):
            if(encoder_21[0]==0):
                encoder_21.pop(0)
            else:
                break
        break

    if z_axis:
        data_range_1 = len(encoder_31)
    else:
        data_range_1 = len(encoder_21)

        ##2nd driver-----------------------------------------------------------------
        ##Data cleaning
        # To remove the blank lines from the file and write the data to a .log file

    with open(FILENAME_2) as infile, open(FILENAME_NEW_2, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output

    f = open(FILENAME_NEW_2, mode='r')
    # Write the data to separate array
    for row in f:
        row = row.split('\t')
        time_axis_2.append(time_t2)
        if z_axis:
            encoder_32.append(float(int(row[2]) * z_axis_mm_per_count))
        else:
            encoder_32.append(0)
        encoder_12.append(float(int(row[0]) * XY_axis_mm_per_count))
        encoder_22.append(float(int(row[1]) * XY_axis_mm_per_count))

        time_t2 += sampling_period

    # remove initial zeros

    while True:
        for i in range(len(encoder_12)):
            if (encoder_12[0] == 0):
                encoder_12.pop(0)
            else:
                break
        for i in range(len(encoder_22)):
            if (encoder_22[0] == 0):
                encoder_22.pop(0)
            else:
                break
        break

    if z_axis:
        data_range_2 = len(encoder_32)
    else:
        data_range_2 = len(encoder_22)

        ##3rd driver-----------------------------------------------------------------
        ##Data cleaning
        # To remove the blank lines from the file and write the data to a .log file

    with open(FILENAME_3) as infile, open(FILENAME_NEW_3, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output

    f = open(FILENAME_NEW_3, mode='r')
    # Write the data to separate array
    for row in f:
        row = row.split('\t')
        time_axis_3.append(time_t3)
        if z_axis:
            encoder_33.append(float(int(row[2]) * z_axis_mm_per_count))
        else:
            encoder_33.append(0)
        encoder_13.append(float(int(row[0]) * XY_axis_mm_per_count))
        encoder_23.append(float(int(row[1]) * XY_axis_mm_per_count))

        time_t3 += sampling_period

    # remove initial zeros

    while True:
        for i in range(len(encoder_13)):
            if (encoder_13[0] == 0):
                encoder_13.pop(0)
            else:
                break
        for i in range(len(encoder_23)):
            if (encoder_23[0] == 0):
                encoder_23.pop(0)
            else:
                break
        break

    if z_axis:
        data_range_3 = len(encoder_33)
    else:
        data_range_3 = len(encoder_23)

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
#x_axis_v13, y_axis_t13,x_axis_p13, y_axis_tp13,x_axis_v23, y_axis_t23,,x_axis_p23, y_axis_tp23, cv3

    def compare(x_axis_v11, y_axis_t11, x_axis_v12, y_axis_t12, x_axis_p11, y_axis_tp11,x_axis_p12, y_axis_tp12,x_axis_v21, y_axis_t21, x_axis_v22, y_axis_t22, x_axis_p21, y_axis_tp21,x_axis_p22, y_axis_tp22, x_axis_v13, y_axis_t13,x_axis_p13, y_axis_tp13,x_axis_v23, y_axis_t23,x_axis_p23, y_axis_tp23, cv3,cv1, cv2):


        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(
            go.Scatter(x=y_axis_t11, y=x_axis_v11,  name="MST16"),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=y_axis_t12, y=x_axis_v12, name="MST32"),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=y_axis_t13, y=x_axis_v13, name="MST64"),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tp11, y=x_axis_p11[0:len(y_axis_tp11)], name="MST16"),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tp12,y=x_axis_p12[0:len(y_axis_tp12)], name="MST32"),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tp13,y=x_axis_p13[0:len(y_axis_tp13)], name="MST64"),
            row=1, col=2
        )
    ###
        fig.add_trace(
            go.Scatter(x=y_axis_t21, y=x_axis_v21,  name="MST16"),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=y_axis_t22, y=x_axis_v22, name="MST32"),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(x=y_axis_t23, y=x_axis_v23, name="MST64"),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tp21, y=x_axis_p21[0:len(y_axis_tp21)], name="MST16"),
            row=2, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tp22,y=x_axis_p22[0:len(y_axis_tp22)], name="MST32"),
            row=2, col=2
        )

        fig.add_trace(
            go.Scatter(x=y_axis_tp23,y=x_axis_p23[0:len(y_axis_tp23)], name="MST64"),
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
        fig.update_layout(height=1800, width=1800, title_text=" TMC2209 | Acceleration: %s Velocity: %s stroke: %s cv(MST16): %s cv(MST32): %s cv(MST64): %s"%(acc, vel, d, cv1, cv2, cv3))
        fig.write_html("/home/morphle/Encoder_Data/plots/Acc(%s)Vel(%s)pos(%s).html"%(acc, vel, d))
        # fig.show()


    ##---------------------------------------------------------------------------------------------------------------------------


    for i in range(len(encoder_11)):

        if i < len(encoder_11) - 1:
            vel_enc_11.append((encoder_11[i + 1] - encoder_11[i]) / sampling_period)


    for i in range(len(encoder_21)):

        if i < len(encoder_21) - 1:
            vel_enc_21.append((encoder_21[i + 1] - encoder_21[i]) / sampling_period)

    ##---------------------------------------------------------------------------------------------------------------------------


    for i in range(len(encoder_12)):

        if i < len(encoder_12) - 1:
            vel_enc_12.append((encoder_12[i + 1] - encoder_12[i]) / sampling_period)


    for i in range(len(encoder_22)):

        if i < len(encoder_22) - 1:
            vel_enc_22.append((encoder_22[i + 1] - encoder_22[i]) / sampling_period)

    ##---------------------------------------------------------------------------------------------------------------------------


    for i in range(len(encoder_13)):

        if i < len(encoder_13) - 1:
            vel_enc_13.append((encoder_13[i + 1] - encoder_13[i]) / sampling_period)


    for i in range(len(encoder_23)):

        if i < len(encoder_23) - 1:
            vel_enc_23.append((encoder_23[i + 1] - encoder_23[i]) / sampling_period)



    ##---------------------------------------------------------------------------------------------------------------------------
    #Data striping

    time_interval = 0.01 #10ms
    group = 50

    #position enc11
    new_encoder_11 = []
    time_encoder_11 = []

    itr_num = int(math.floor(len(encoder_11)/group))

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_encoder_11.append(statistics.mean(encoder_11[i:end_val]))
        time_encoder_11.append(statistics.mean(time_axis_1[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_11)):
        new_encoder_11.append(encoder_11[j])
        time_encoder_11.append(time_axis_1[j])

    #position enc21
    new_encoder_21 = []
    time_encoder_21 = []

    itr_num = math.floor(len(encoder_21)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i+group
        new_encoder_21.append(statistics.mean(encoder_21[i:end_val]))
        time_encoder_21.append(statistics.mean(time_axis_1[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_21)):
        new_encoder_21.append(encoder_21[j])
        time_encoder_21.append(time_axis_1[j])


    #Velocity  enc11
    new_vel_enc_11 = []
    time_vel_enc_11 = []

    itr_num = math.floor(len(vel_enc_11)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_11.append(statistics.mean(vel_enc_11[i:end_val]))
        time_vel_enc_11.append(statistics.mean(time_axis_1[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_11)):
        new_vel_enc_11.append(vel_enc_11[j])
        time_vel_enc_11.append(time_axis_1[j])

    #Velocity enc21
    new_vel_enc_21 = []
    time_vel_enc_21 = []

    itr_num = math.floor(len(vel_enc_21)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_21.append(statistics.mean(vel_enc_21[i:end_val]))
        time_vel_enc_21.append(statistics.mean(time_axis_1[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_21)):
        new_vel_enc_21.append(vel_enc_21[j])
        time_vel_enc_21.append(time_axis_1[j])

##------------

    #position enc12
    new_encoder_12 = []
    time_encoder_12 = []

    itr_num = int(math.floor(len(encoder_12)/group))

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_encoder_12.append(statistics.mean(encoder_12[i:end_val]))
        time_encoder_12.append(statistics.mean(time_axis_2[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_12)):
        new_encoder_12.append(encoder_12[j])
        time_encoder_12.append(time_axis_2[j])

    #position enc22
    new_encoder_22 = []
    time_encoder_22 = []

    itr_num = math.floor(len(encoder_22)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i+group
        new_encoder_22.append(statistics.mean(encoder_22[i:end_val]))
        time_encoder_22.append(statistics.mean(time_axis_2[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_22)):
        new_encoder_22.append(encoder_22[j])
        time_encoder_22.append(time_axis_2[j])


    #Velocity  enc12
    new_vel_enc_12 = []
    time_vel_enc_12 = []

    itr_num = math.floor(len(vel_enc_12)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_12.append(statistics.mean(vel_enc_12[i:end_val]))
        time_vel_enc_12.append(statistics.mean(time_axis_2[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_12)):
        new_vel_enc_12.append(vel_enc_12[j])
        time_vel_enc_12.append(time_axis_2[j])

    #Velocity enc22
    new_vel_enc_22 = []
    time_vel_enc_22 = []

    itr_num = math.floor(len(vel_enc_22)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_22.append(statistics.mean(vel_enc_22[i:end_val]))
        time_vel_enc_22.append(statistics.mean(time_axis_2[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_22)):
        new_vel_enc_22.append(vel_enc_22[j])
        time_vel_enc_22.append(time_axis_2[j])
##---------

    #position enc13
    new_encoder_13 = []
    time_encoder_13 = []

    itr_num = int(math.floor(len(encoder_13)/group))

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_encoder_13.append(statistics.mean(encoder_13[i:end_val]))
        time_encoder_13.append(statistics.mean(time_axis_3[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_13)):
        new_encoder_13.append(encoder_13[j])
        time_encoder_13.append(time_axis_3[j])

    #position enc23
    new_encoder_23 = []
    time_encoder_23 = []

    itr_num = math.floor(len(encoder_23)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i+group
        new_encoder_23.append(statistics.mean(encoder_23[i:end_val]))
        time_encoder_23.append(statistics.mean(time_axis_3[i:end_val]))

    for j in range((itr_num*group)+1, len(encoder_23)):
        new_encoder_23.append(encoder_23[j])
        time_encoder_23.append(time_axis_3[j])


    #Velocity  enc13
    new_vel_enc_13 = []
    time_vel_enc_13 = []

    itr_num = math.floor(len(vel_enc_13)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_13.append(statistics.mean(vel_enc_13[i:end_val]))
        time_vel_enc_13.append(statistics.mean(time_axis_3[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_13)):
        new_vel_enc_13.append(vel_enc_13[j])
        time_vel_enc_13.append(time_axis_3[j])

    #Velocity enc23
    new_vel_enc_23 = []
    time_vel_enc_23 = []

    itr_num = math.floor(len(vel_enc_23)/group)
    itr_num = int(itr_num)

    for i in range(0,itr_num*group,group):
        end_val = i + group
        new_vel_enc_23.append(statistics.mean(vel_enc_23[i:end_val]))
        time_vel_enc_23.append(statistics.mean(time_axis_3[i:end_val]))

    for j in range((itr_num*group)+1, len(vel_enc_23)):
        new_vel_enc_23.append(vel_enc_23[j])
        time_vel_enc_23.append(time_axis_3[j])

    ##-----------------------------------`----------------------------------------------------------------------------------------
    # taking snippet of constant velo curve
    t1x = 0
    t1y = 0

    t2x = 0
    t2y = 0

    max_vel = int(vel)  # mm/sec #end-effector's max valocity
    a = int(acc)  # mm/sec^2
    t = sampling_period  # sec
    d = int(d)

    theta = 53

    if (d > 0):
        dx = (math.cos(math.radians(theta))) * d
        dy = (math.sin(math.radians(theta))) * d

    jx = 0  # max jerk in mm/sec
    jy = 0  # max jerk in mm/sec

    if (dx != 0 and dy != 0):

        max_vx = (math.cos(math.radians(theta))) * max_vel
        max_vy = (math.sin(math.radians(theta))) * max_vel
    else:
        max_vy = max_vel
        max_vx = max_vel

    ##---------------------------------------------------------------------------------------------------------------------------

    # Ideal Value calculation - X axis


    t1 = (max_vx - jx) / a  # Assumption: starting velocity = max jerk value
    d1 = jx * t1 + (0.5) * a * (t1 ** 2)

    v2 = max_vx
    v3 = v2 - jx

    t32 = v3 / a  # t32 = t3-t2

    d3 = v3 * t32 - (0.5) * a * (t32 ** 2)
    d2 = dx - (d1 + d3)

    t2 = d2 / v2 + t1

    t_total = t2 + t32


    if(dx<(d1+d3)):  ## Triangular curve for dx<2*d1

        # qaudratic equation parameters
        aa = a
        bb = jx
        cc = -dx

        t11 = (-bb + ((bb ** 2) - (4 * aa * cc)) ** 0.5) / (2 * aa)
        t12 = (-bb - ((bb ** 2) - (4 * aa * cc)) ** 0.5) / (2 * aa)

        if t11 > 0:
            t1 = t11
        else:
            t1 = t12

        if t11 > 0 and t12 > 0:
            print("Error in time calculation")
            exit()

        t_total = 2 * t1

        CV_1 = '-'
        CV_2 = '-'
        CV_3 = '-'
        ##    d1 = (d/2) + (5*t1)
        ##    d2 = d - d1
    else:
        t1x = t1
        t1y = t2

        start_1 = int(t1x / sampling_period)
        end_1 = int(t1y / sampling_period)

        CV_1 = round((np.std(vel_enc_11[start_1:end_1]) / (statistics.mean(vel_enc_11[start_1:end_1]))) * 100, 3)
        CV_2 = round((np.std(vel_enc_12[start_1:end_1]) / (statistics.mean(vel_enc_12[start_1:end_1]))) * 100, 3)
        CV_3 = round((np.std(vel_enc_13[start_1:end_1]) / (statistics.mean(vel_enc_13[start_1:end_1]))) * 100, 3)



            ##---------------------------------------------------------------------------------------------------------------------------

    # Ideal Value calculation - Y axis
    t = sampling_period

    t1 = (max_vy - jy) / a  # Assumption: starting velocity = max jerk value
    d1 = jy * t1 + (0.5) * a * (t1 ** 2)

    v2 = max_vy
    v3 = v2 - jy

    t32 = v3 / a  # t32 = t3-t2

    d3 = v3 * t32 - (0.5) * a * (t32 ** 2)
    d2 = dy - (d1 + d3)

    t2 = d2 / v2 + t1

    t_total = t2 + t32
    t2x = t1
    t2y = t2

    start_2 = int(t2x/sampling_period)
    end_2 = int(t2y/sampling_period)

    if dy<(d1+d3):  ## Triangular curve for d<2*d1

        # qaudratic equation parameters
        aa = a
        bb = jy
        cc = -dy

        t11 = (-bb + ((bb ** 2) - (4 * aa * cc)) ** 0.5) / (2 * aa)
        t12 = (-bb - ((bb ** 2) - (4 * aa * cc)) ** 0.5) / (2 * aa)

        if t11 > 0:
            t1 = t11
        else:
            t1 = t12

        if t11 > 0 and t12 > 0:
            print("Error in time calculation")
            exit()

        t_total = 2 * t1
        ##    d1 = (d/2) + (5*t1)
        ##    d2 = d - d1



            ##---------------------------------------------------------------------------------------------------------------------------
    #print curves

#new_vel_enc_13, time_vel_enc_13[0:len(new_vel_enc_13)], new_encoder_13, time_encoder_13[0:len(new_encoder_13)],new_vel_enc_23, time_vel_enc_23[0:len(new_vel_enc_23)],new_encoder_23, time_encoder_23[0:len(new_encoder_23)],CV_3
    compare(new_vel_enc_11, time_vel_enc_11[0:len(new_vel_enc_11)], new_vel_enc_12, time_vel_enc_12[0:len(new_vel_enc_12)],  new_encoder_11, time_encoder_11[0:len(new_encoder_11)],new_encoder_12, time_encoder_12[0:len(new_encoder_12)], new_vel_enc_21, time_vel_enc_21[0:len(new_vel_enc_21)], new_vel_enc_22, time_vel_enc_22[0:len(new_vel_enc_22)], new_encoder_21, time_encoder_21[0:len(new_encoder_21)],new_encoder_22, time_encoder_22[0:len(new_encoder_22)], new_vel_enc_13, time_vel_enc_13[0:len(new_vel_enc_13)], new_encoder_13, time_encoder_13[0:len(new_encoder_13)],new_vel_enc_23, time_vel_enc_23[0:len(new_vel_enc_23)],new_encoder_23, time_encoder_23[0:len(new_encoder_23)],CV_3 ,CV_1, CV_2)
