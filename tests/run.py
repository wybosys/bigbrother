#!/usr/bin/env python3 

import sys, subprocess, signal

#print(sys.argv)

proc = subprocess.Popen(' '.join(sys.argv[1:]), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def doquit(signum=0, frame=0):
    proc.terminate()

signal.signal(signal.SIGINT, doquit)
signal.signal(signal.SIGTERM, doquit)

while True:
    line = proc.stdout.readline()
    line = line.decode("utf-8", "ignore")
    if proc.poll() != None:        
        break
    print(line, end='')

ret = proc.communicate()[1]
if ret:
    exit(ret)
