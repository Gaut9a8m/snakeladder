#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
from datetime import datetime

def sendmessage(message, t):
    while 1:
        #print(datetime.now().strftime("%H:%M"))
        if(datetime.now().strftime("%H:%M") == t):
            subprocess.Popen(['notify-send', message])
            break

if __name__ == '__main__':
    sendmessage(input('enter your mssg: '), input('\n enter time: '))
