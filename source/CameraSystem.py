import pprint

from DetectionNumber import DetectionNumber
from Camera import Camera


class CameraSystem:
    def __init__(self):
        self.camera = Camera()

    def start(self):
        self.camera.capture()
        number_card = self.camera.get_number_img()
        block_bingo_img = self.camera.get_block_bingo_img()
        circles_coordinates = self.camera.get_circle_coordinates()
        pprint.pprint(circles_coordinates)
        detection_number = DetectionNumber(img=number_card, model_path="./DetectionNumber/my_model.npz")
        number = detection_number.get_detect_number()
        print(number)


if __name__ == '__main__':
    cs = CameraSystem()
    cs.start()
