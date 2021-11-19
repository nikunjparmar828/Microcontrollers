from cmp_driver import plots
import glob

strk = ['10','40']
velo = ['10', '50','200']
acce = ['400', '1000','3000' ]
drvr = ['TMC2209_V2']
stps = ['MST16', 'MST32', 'MST64']

f_path_1 = ''
f_path_2 = ''
f_path_3 = ''

# f_path_lst_1 = glob.glob('/home/morphle/Encoder_Data/Marlin_Driver_testing_data/%s/%s/Acc_%s/%s_mm_sec/%smm/*.log' % (
# drvr[0], stps[0], acce[0], velo[0], strk[1]))
# FILENAME_1 = f_path_lst_1[0]
#
# f_path_lst_2 = glob.glob('/home/morphle/Encoder_Data/Marlin_Driver_testing_data/%s/%s/Acc_%s/%s_mm_sec/%smm/*.log' % (
# drvr[0], stps[1], acce[0], velo[0], strk[1]))
# FILENAME_2 = f_path_lst_2[0]
#
# f_path_lst_3 = glob.glob('/home/morphle/Encoder_Data/Marlin_Driver_testing_data/%s/%s/Acc_%s/%s_mm_sec/%smm/*.log' % (
# drvr[0], stps[2], acce[0], velo[0], strk[1]))
# FILENAME_3 = f_path_lst_3[0]
#
# plots(FILENAME_1, FILENAME_2, FILENAME_3, acce[0], velo[0], strk[1])


for i in range(len(acce)):

    for j in range(len(velo)):

        for k in range(len(strk)):
            f_path_lst_1 = glob.glob('/home/morphle/Encoder_Data/Marlin_Driver_testing_data/%s/%s/Acc_%s/%s_mm_sec/%smm/*.log'%(drvr[0], stps[0], acce[i], velo[j], strk[k]))
            FILENAME_1 = f_path_lst_1[0]

            f_path_lst_2 = glob.glob('/home/morphle/Encoder_Data/Marlin_Driver_testing_data/%s/%s/Acc_%s/%s_mm_sec/%smm/*.log'%(drvr[0], stps[1], acce[i], velo[j], strk[k]))
            FILENAME_2 = f_path_lst_2[0]

            f_path_lst_3 = glob.glob('/home/morphle/Encoder_Data/Marlin_Driver_testing_data/%s/%s/Acc_%s/%s_mm_sec/%smm/*.log'%(drvr[0], stps[2], acce[i], velo[j], strk[k]))
            FILENAME_3 = f_path_lst_3[0]

            plots(FILENAME_1, FILENAME_2,FILENAME_3, acce[i], velo[j], strk[k])



##-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# time_interval = 0.01 #10ms
#     group = int(time_interval / sampling_period)
#
#     #position GRBL enc1
#     new_encoder_1g = []
#     time_encoder_1g = []
#
#     itr_num = int(math.floor(len(encoder_1g)/group))
#
#     for i in range(0,itr_num*group,group):
#         new_encoder_1g.append(encoder_1g[i:end_val].mean())
#         time_encoder_1g.append(time_axis_g[i])
#
#     for j in range((itr_num*group)+1, len(encoder_1g)):
#         new_encoder_1g.append(encoder_1g[j])
#         time_encoder_1g.append(time_axis_g[j])
#
#     #position GRBL enc2
#     new_encoder_2g = []
#     time_encoder_2g = []
#
#     itr_num = math.floor(len(encoder_2g)/group)
#     itr_num = int(itr_num)
#     for i in range(0,itr_num*group,group):
#         new_encoder_2g.append(encoder_2g[i])
#         time_encoder_2g.append(time_axis_g[i])
#
#     for j in range((itr_num*group)+1, len(encoder_2g)):
#         new_encoder_2g.append(encoder_2g[j])
#         time_encoder_2g.append(time_axis_g[j])
#
#     #position MARLIN enc1
#     new_encoder_1m = []
#     time_encoder_1m = []
#
#     itr_num = math.floor(len(encoder_1m)/group)
#     itr_num = int(itr_num)
#
#     for i in range(0,itr_num*group,group):
#         new_encoder_1m.append(encoder_1m[i])
#         time_encoder_1m.append(time_axis_m[i])
#
#     for j in range((itr_num*group)+1, len(encoder_1m)):
#         new_encoder_1m.append(encoder_1m[j])
#         time_encoder_1m.append(time_axis_m[j])
#
#     #position MARLIN enc2
#     new_encoder_2m = []
#     time_encoder_2m = []
#
#     itr_num = math.floor(len(encoder_2m)/group)
#     itr_num = int(itr_num)
#
#     for i in range(0,itr_num*group,group):
#         new_encoder_2m.append(encoder_2m[i])
#         time_encoder_2m.append(time_axis_m[i])
#
#     for j in range((itr_num*group)+1, len(encoder_2m)):
#         new_encoder_2m.append(encoder_2m[j])
#         time_encoder_2m.append(time_axis_m[j])
#
#     #Velocity GRBL enc1
#     new_vel_enc_1g = []
#     time_vel_enc_1g = []
#
#     itr_num = math.floor(len(vel_enc_1g)/group)
#     itr_num = int(itr_num)
#
#     for i in range(0,itr_num*group,group):
#         new_vel_enc_1g.append(vel_enc_1g[i])
#         time_vel_enc_1g.append(time_axis_g[i])
#
#     for j in range((itr_num*group)+1, len(vel_enc_1g)):
#         new_vel_enc_1g.append(vel_enc_1g[j])
#         time_vel_enc_1g.append(time_axis_g[j])
#
#     #Velocity GRBL enc2
#     new_vel_enc_2g = []
#     time_vel_enc_2g = []
#
#     itr_num = math.floor(len(vel_enc_2g)/group)
#     itr_num = int(itr_num)
#
#     for i in range(0,itr_num*group,group):
#         new_vel_enc_2g.append(vel_enc_2g[i])
#         time_vel_enc_2g.append(time_axis_g[i])
#
#     for j in range((itr_num*group)+1, len(vel_enc_2g)):
#         new_vel_enc_2g.append(vel_enc_2g[j])
#         time_vel_enc_2g.append(time_axis_g[j])
#
#     #Velocity MARLIN enc1
#     new_vel_enc_1m = []
#     time_vel_enc_1m = []
#
#     itr_num = math.floor(len(vel_enc_1m)/group)
#     itr_num = int(itr_num)
#
#     for i in range(0,itr_num*group,group):
#         new_vel_enc_1m.append(vel_enc_1m[i])
#         time_vel_enc_1m.append(time_axis_m[i])
#
#     for j in range((itr_num*group)+1, len(vel_enc_1m)):
#         new_vel_enc_1m.append(vel_enc_1m[j])
#         time_vel_enc_1m.append(time_axis_m[j])
#
#     #Velocity MARLIN enc2
#     new_vel_enc_2m = []
#     time_vel_enc_2m = []
#
#     itr_num = math.floor(len(vel_enc_2m)/group)
#     itr_num = int(itr_num)
#
#     for i in range(0,itr_num*group,group):
#         new_vel_enc_2m.append(vel_enc_2m[i])
#         time_vel_enc_2m.append(time_axis_m[i])
#
#     for j in range((itr_num*group)+1, len(vel_enc_2m)):
#         new_vel_enc_2m.append(vel_enc_2m[j])
#         time_vel_enc_2m.append(time_axis_m[j])
