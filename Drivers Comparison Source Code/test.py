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
