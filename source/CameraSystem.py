from DetectionNumber import DetectionNumber
from Camera import Camera
from bluetooth.Bluetooth import Bluetooth
import time


class CameraSystem:
    def __init__(self):
        self.camera = Camera()
        self.bt = Bluetooth()
        self.port = "/dev/cu.MindstormsEV3-SerialPor"
        self.card_number = None

    def _connect_to_ev3(self):
        self.bt.connect(self.port)
        while True:
            write_data = 0
            self.bt.write(write_data)
            if self.bt.read() == 1:
                return

            time.sleep(1)  # sec

    def _detection_number(self):
        self.camera.capture()
        number_card = self.camera.get_point()
        detection_number = DetectionNumber(img=number_card, model_path="./DetectionNumber/my_model.npz")
        return detection_number.get_detect_number()

    def start(self):
        print("\nConnect EV3")
        self._connect_to_ev3()
        print("Success! Connected ev3")

        print("\nDetection Number")
        self.card_number = self._detection_number()
        print(f"number is {self.card_number}")

        print("\nDetection Block")
        # TODO これから

        print("\nSend Command")
        # TODO これから


if __name__ == '__main__':
    cs = CameraSystem()
    cs.start()
