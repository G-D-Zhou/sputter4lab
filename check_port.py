# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 22:42:39 2024

@author: 20230313C
"""
import serial
from classes import *


def check_port():
    
    # 初始化电磁继电器串口
    try:
        serRelay = serial.Serial("COM3", 38400, timeout=0.1)
    except:
        serRelay = False
    
    if serRelay != False:
        if serRelay.name == "COM3":
            if serRelay.port == "COM3":
                print("你打开了继电器的串口，COM3！")
            else:
                print("继电器串口连接失败，请检查01！")
        else:
            print("继电器串口连接失败，请检查02！")
            
    else:
        print("继电器串口连接失败，请检查03！")
                

    # 初始化电磁继电器串口
    try:
        serH700 = serial.Serial("COM4", 9600, timeout=0.1)
    except:
        serH700 = False
    
    if serH700 != False:
        if serH700.name == "COM4":
            if serH700.port == "COM4":
                print("你打开了数据采集系统的串口，COM4！")
            else:
                print("数据采集系统串口连接失败，请检查01！")
        else:
            print("数据采集系统串口连接失败，请检查02！")
            
    else:
        print("数据采集系统串口连接失败，请检查03！")    

        
   
    return serRelay, serH700


