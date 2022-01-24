import pickle
import sys
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
    
    
if len(sys.argv)==1:
    print("No input file")
    exit(-1)

print("opening '%s' "%(sys.argv[1]))
notes = None

noteh = {}
if len(sys.argv)==3:
    print("Loading Notes")
    nf = open(sys.argv[2], 'r')
    notel = nf.read().split("\n")
    noteh = {}
    for n in notel:
        line = n.split("\t")
        noteh[line[0]]=line[1]
    print(noteh)

with open(sys.argv[1], 'rb') as f:
    data = pickle.load(f)
    prev = None
    for d in data:
        x=d[1]
        t=d[0]
        # Packets SEEM to be 41 bytes and start with 42
        if len(x)== 41:
                if prev == None:
                    prev=x
                print("(%s) ["%(len(x)),end = '')
                for idx in range(len(x)):
                    # Hilight changed bytes in red
                    if prev[idx] != x[idx]:
                        print(bcolors.FAIL,end = '')
                    print("%0.2x "%(x[idx]),end = '')
                    if prev[idx] != x[idx]:
                        print(bcolors.ENDC,end = '')
                print("] %s"%(t),end='')
                if str(t) in noteh:
                    print(" %s"%(noteh[str(t)]),end='')
                print()
                prev=x
        # Sometimes the serial port times out and we get 0 bytes
        # Sometimes we get a "short packet"
        elif len(x) != 0:
                print("(ss) [",end='')
                for idx in range(len(x)):
                    print("%0.2x "%(x[idx]),end = '')
                print("] %s"%(t),end='')
                if str(t) in noteh:
                    print(" %s"%(noteh[str(t)]),end='')
                print()