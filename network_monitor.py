import psutil
import os
from datetime import datetime
import time




def collect_data(interface):

    tmp_bytes = {"bytes_recv":0,"bytes_sent":0}


    tmp_bytes = {}
    n = 0.25
    time.sleep(n)
    os.system("clear")
    raw_vals = str(psutil.net_io_counters(True)[interface])
    raw_vals = raw_vals[7:len(raw_vals) - 1]
    tmp_lst = raw_vals.split(', ')
    val_dict = {}

    for val in tmp_lst:
        tmp = val.split("=")
        val_dict[tmp[0]] = tmp[1]

    tmp_bytes["bytes_sent"] = float(val_dict["bytes_sent"])/(1000*n)
    tmp_bytes["bytes_recv"] = float(val_dict["bytes_recv"])/(1000*n)



    if check_file_exists("stats.csv"):
        bytes_wite = open("stats.csv",'a')
        bytes_wite.write(str((tmp_bytes["bytes_recv"]))+","+str((tmp_bytes["bytes_sent"]))+","+str(datetime.now())+"\n")


    return_values = str((tmp_bytes["bytes_recv"])) + ":" + str((tmp_bytes["bytes_sent"]))
      
    return return_values
       

def check_file_exists(file):
    try:
        f = open(file,'r')
    except:
        f = open(file,'w')
        f.close()
        return False
    else:
        return True
        f.close()








