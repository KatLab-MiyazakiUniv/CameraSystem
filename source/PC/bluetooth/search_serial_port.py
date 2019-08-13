import serial
import serial.tools.list_ports


def search_serial_port():
    """
    シリアルポートを探す（デバッグ用）
    """
    coms = serial.tools.list_ports.comports()
    for com in coms:
        print('{0}'.format(com))

if __name__ == '__main__':
    search_serial_port()
