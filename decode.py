import serial
import pickle
from colorama import init
init()

import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
data = []
try:

    with serial.Serial('COM70', 9600, timeout=1) as ser:
        prev = None
        while True:
            tm = time.time()
            x = ser.read(41)
            data.append([tm,x])
            
            if len(x)== 41:
                if prev == None:
                    prev=x
                print("(%s) ["%(len(x)),end = '')
                for idx in range(len(x)):
                    if prev[idx] != x[idx]:
                        print(bcolors.FAIL,end = '')
                    print("%0.2x "%(x[idx]),end = '')
                    if prev[idx] != x[idx]:
                        print(bcolors.ENDC,end = '')
                print("] %s"%(tm))
                prev=x
            elif len(x) != 0:
                print("(ss) [",end='')
                for idx in range(len(x)):
                    print("%0.2x "%(x[idx]),end = '')
                print("] %s"%(tm))
except KeyboardInterrupt:
    with open("data-%s.pickle"%(time.time()), 'wb') as f: 
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        exit()