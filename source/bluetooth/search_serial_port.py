"""
@file: search_serial_port.py
@author: Tatsumi0000
@brief: 現在使っているPCの利用可能なシリアルポートの名前を探すデバッグ用の関数（これがなくてもBluetooth.pyは動く）
"""
import serial
import serial.tools.list_ports


def search_com_ports():
    """
    シリアルポートを探す（デバッグ用）
    """
    coms = serial.tools.list_ports.comports()
    for com in coms:
        print('{0}'.format(com))


def search_enabled_com_port():
    # 有効なCOMポートを自動的に探して返す
    coms = serial.tools.list_ports.comports()
    comlist = []
    for com in coms:
        comlist.append(com.device)
    print('Connected COM ports: ' + str(comlist))
    use_port = comlist[0]
    print('Use COM port: ' + use_port)
    return use_port


if __name__ == '__main__':
    search_com_ports()
    search_enabled_com_port()