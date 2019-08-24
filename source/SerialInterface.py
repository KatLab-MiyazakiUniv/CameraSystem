#!/usr/bin/env python
# coding: utf-8
import serial
import struct
import time

class SerialInterface(object):
    def __init__(self):
        self.ser = serial.Serial()

    def __del__(self):
        self.close()

    # シリアル通信の開通
    def open(self, port, baud=115200, timeout=1):
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.timeout = timeout
        
        if self.ser.is_open:
            self.ser.close()

        while (not self.ser.is_open):
            try:
                self.ser.open()
            except serial.SerialException:
                print("SerialInterface> wait for connect from client..")
                time.sleep(5) # 5秒後に接続リトライ
                continue
            except:
                raise Exception("failed to open")

        print("SerialInterface> connected")

    # Type-Length-Value形式でメッセージ送信
    def write(self, type, value):
        if not self.ser.is_open:
            raise Exception("serial port is not opened")
        if value == None:
            raise Exception("value is none")
        msg = type.to_bytes(1,'big')
        msg += len(value).to_bytes(1,'big')
        msg += value
        self.ser.write(struct.pack('B'*len(msg), *msg))

    # Type-Length-Value形式のメッセージ受信
    def read(self):
        if not self.ser.is_open:
            raise Exception("serial port is not opened")
        type = struct.unpack('B', self.ser.read(1))[0]
        length  = struct.unpack('B', self.ser.read(1))[0]
        value = self.ser.read(length)
        return (type, value)

    # シリアル通信の閉鎖
    def close(self):
        if self.ser.is_open:
            self.ser.close()
            print("SerialInterface> disconnected")
