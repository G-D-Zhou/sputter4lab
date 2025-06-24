# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 13:49:03 2024

@author: 20230313C
"""

import sys  
import os
import crcmod
import struct
from binascii import b2a_hex, unhexlify
import time



# 输入完整命令，发送给串口，并return返回值
def sentAndReturn(command,ser,check_len=False):
    Command = command
    Command_str = bytes.fromhex(Command)
    ser.write(Command_str)
    received_data = b''
    if check_len != False:
        while len(received_data) < check_len:
            chunk = ser.read(check_len - len(received_data))

        
            received_data += chunk
    
    
        mcu = str(b2a_hex(received_data))
    
    else:
        mcu = str(b2a_hex(ser.read(size=16)))
    
    return mcu

def hex2float(valueHex):
    # 输入的字符串排序是不对的首先需要交换位置
    valueHexSwapped = valueHex[4:] + valueHex[:4]
    
    # print(MFCvalueHexSwapped)
    
    # 将十六进制字符串转换为字节对象
    bytes_object = bytes.fromhex(valueHexSwapped)
    
    if len(bytes_object) != 4:
        raise ValueError(f"Converted bytes length must be 4, got {len(bytes_object)}: {bytes_object}")
    
    # 解码字节对象为浮点数（双精度）
    # '!f'表示大端序单精度浮点数
    double_value = struct.unpack('!f', bytes_object)[0]
    
    return f"{double_value:.4f}"

def parse_hex_string(s):
    #print(s)
    # 移除字符串开头的"b'"和结尾的"'"
    inner = s[2:-1]
    # 移除开头的"010470"（6个字符）和末尾的"D6F5"（4个字符）
    inner = inner[6:-4]
    # 按8字符一组拆分
    groups = [inner[i:i+8] for i in range(0, len(inner), 8)]
    # 生成字典（键从C1开始）
    return {f'C{i+1}': group for i, group in enumerate(groups)}


class Relay():
    # 打开某个电磁器
    def openRelay(Y, ser):
        try:
            if Y == "Y1":
                returnValue = sentAndReturn('010600000001480A', ser)
                #print(returnValue)   # 01 06 00 00 00 01 48 0A
                
            if Y == "Y11":
                returnValue = sentAndReturn('0106000A00016808', ser)
               # print(returnValue)   # 01 06 00 0A 00 01 68 08
               
            
            if Y == "Y30":
                returnValue = sentAndReturn('0106001D0001D80C', ser)
                
            if Y == "Y31":
                returnValue = sentAndReturn('0106001E0001280C', ser)
               
            if Y == "Y32":
                returnValue = sentAndReturn('0106001F000179CC', ser)
                
                
        except:
            print("请检查输入！")
            print("请检查串口连接！")
            print("请检查继电器供电以及是否损坏！")


# 14:12:51.583→发 01 06 00 1D 00 00 19 CC 
# 14:12:51.603←收 01 06 00 1D 00 00 19 CC 
# 14:12:52.915→发 01 06 00 1D 00 01 D8 0C 
# 14:12:52.931←收 01 06 00 1D 00 01 D8 0C           
        
        
    
    def closeRelay(Y, ser):
        if Y == "Y1":
            returnValue = sentAndReturn('01060000000089CA', ser)
            #print(returnValue)   # 01 06 00 00 00 00 89 CA
        
        
        if Y == "Y11":
            returnValue = sentAndReturn('0106000A0000A9C8', ser)
            #print(returnValue)   # 01 06 00 0A 00 00 A9 C8
        
        
        if Y == "Y30":
            returnValue = sentAndReturn('0106001D000019CC', ser)
            
        if Y == "Y31":
            returnValue = sentAndReturn('0106001E0000E9CC', ser)
        
        if Y == "Y32":
            returnValue = sentAndReturn('0106001F0000B80C', ser)
        
        
    def checkAllState(ser):
        # 接收所有继电器的状态
        state_All = sentAndReturn('0103000000204412', ser,check_len=69)
        state_All = state_All[2:-1]
        #将所有状态依次转化为布尔值
        # 将字节串转换为字符串并去掉开头的 '010340'
        data_str = state_All.replace('010340', '')[:-4]

        # 每四个字符为一组进行分割
        groups = [data_str[i:i+4] for i in range(0, len(data_str), 4)]

        # 3. 遍历列表，替换 "0000" 为 False，"0001" 为 True
        result = []
        for item in groups:
            if item == "0000":
                result.append(False)
            elif item == "0001":
                result.append(True)
            else:
                result.append(item)  # 如果不是 "0000" 或 "0001"，保留原值


        # 4. 存入字典，键为 "Y01" 到 "Y32"
        output_dict = {}
        for i in range(len(result)):
            key = f"Y{i+1:02d}"  # 格式化为 Y01, Y02, ..., Y32
            output_dict[key] = result[i]
        
        # print(output_dict)
        
        # # 检查Y11继电器状态----前级阀门
        # state_Y11 = sentAndReturn('0103000A0001A408', ser)
        # if state_Y11 == "b'0103020000b844'":
        #     sate_Y11_bool = False
        # elif state_Y11 == "b'01030200017984'":
        #     sate_Y11_bool = True
        
        
        
        # # 检查Y30继电器状态----干泵远程
        # state_Y30 = sentAndReturn('0103001D0001140C', ser)
        # if state_Y30 == "b'0103020000b844'":
        #     sate_Y30_bool = False
        # elif state_Y30 == "b'01030200017984'":
        #     sate_Y30_bool = True
    
        # # 检查Y31继电器状态----干泵远程
        # state_Y31 = sentAndReturn('0103001E0001E40C', ser)
        # if state_Y31 == "b'0103020000b844'":
        #     sate_Y31_bool = False
        # elif state_Y31 == "b'01030200017984'":
        #     sate_Y31_bool = True            
    
    
        # # 检查Y32继电器状态----干泵启动
        # state_Y32 = sentAndReturn('0103001F0001B5CC', ser)
        # if state_Y32 == "b'0103020000b844'":
        #     sate_Y32_bool = False
        # elif state_Y32 == "b'01030200017984'":
        #     sate_Y32_bool = True
            

        
        # # 继电器状态字典
        # relay_status = {
        #     "Y11": sate_Y11_bool,  # 第 11 个继电器
            
        #     "Y30": sate_Y30_bool, # 第 30 个继电器
            
        #     "Y31": sate_Y31_bool, # 第 31 个继电器
            
        #     "Y32": sate_Y32_bool,  # 第 32 个继电器
        #     # "Y12": True,   # 第 12 个继电器开启
        #     # "Y13": False
        # }
        
        return output_dict
    
    
        
        
def H700(ser):
    # 从数据系统中依次读取当前值，并完成数据转化
    returnValue = sentAndReturn('010400000038F1D8', ser, check_len=117)
    hex_groups = parse_hex_string(returnValue)
    
    float_dict = {}
    for i, hex_str in enumerate(hex_groups):
    #    if hex_str != "00000000":  # 跳过全零分组
            float_value = hex2float(hex_groups[hex_str])
            float_dict[f"C{i+1}"] = float_value


    return float_dict
        
    
    
    
    
    
        
#      18:36:14.643→发 01 06 00 0A 00 01 68 08 
# 18:36:14.666←收 01 06 00 0A 00 01 68 08 
# 18:36:15.309→发 01 06 00 0A 00 00 A9 C8 
# 18:36:15.321←收 01 06 00 0A 00 00 A9 C8    
        
        
        
        
# 真空计模拟信号转化
class VacuumGauge():
    def WideRangeGauge_Edwards(voltage, units="Pa"):
        if units == "Pa":
            return 10**(1.5*voltage-10)
    
        elif units == "mbar":
            return 10**(1.5*voltage-12)

        elif units == "torr":
            return 10**(1.5*voltage-12.125)
        
    # def CapacitanceDiaphragmGauge_inficon(voltage, p_max,units='Pa'):
    #     if units == "Pa":
    #         return (voltage/10)*
        
        
        
        
        
        
        
        
        
        
        