from DetectionNumber import DetectionNumber
from Camera import Camera
from bluetooth.Bluetooth import Bluetooth
import time


class CameraSystem:
    def __init__(self):
        self.camera = Camera()
        self.bt = Bluetooth()
        self.port = "/dev/cu.MindstormsEV3-SerialPor"

    def connect_to_ev3(self):
        self.bt.connect(self.port)
        while True:
            write_data = 0
            self.bt.write(write_data)
            if self.bt.read() == 1:
                return

            time.sleep(1)  # sec

    def start(self):
        self.connect_to_ev3()
        print("Success! Connected ev3")
        while True:
            try:
                self.bt.write(ord(input()))
            except OverflowError:
                print("OverflowError")
            except ValueError:
                print("ValueError")
        print()
        print("Detection Number")
        self.camera.capture()
        number_card = self.camera.get_point()
        detection_number = DetectionNumber(img=number_card, model_path="./DetectionNumber/my_model.npz")
        number = detection_number.get_detect_number()
        print(f"number is {number}")


if __name__ == '__main__':
    cs = CameraSystem()
    cs.start()
