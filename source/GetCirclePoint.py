"""
@file: GetCirclePoint.py
@author: Tatsumi0000
@brief: 左上の（数字の1）の黄色い交点サークル4箇所とブロックサークル1をクリックするとすべてのサークルの座標を取得する
"""

import cv2
from source import onMouse as om
# import source.onMouse
import numpy as np


class GetCirclePoint:

    def __init__(self):
        """コンストラクタ
        """
        # self.mouse_point = []
        self.mouse_point = np.empty((5, 2))
        # print(self.mouse_point)

    def captureCamera(self) -> None:
        """
        動画をキャプチャして画像として切り出して保存する．
        :return:
        """
        pass

    def sort5LocationPoint(self, ) -> None:
        """
        取得した座標をソートする．
        :return:
        """
        self.mouse_point = np.array(self.mouse_point)
        mouse_point = np.sum(self.mouse_point, axis=1)
        print('{0}' .format(mouse_point))


if __name__ == '__main__':
    getCirclePoint = GetCirclePoint()
    img = cv2.imread("./img/clip_field.png")
    window_name = "WindowDAYO"
    mouse_count = 5
    cv2.namedWindow(window_name)
    # cv2.setMouseCallback(window_name, om.onMouse, [window_name, img, mouse_count, getCirclePoint.mouse_point])
    cv2.setMouseCallback(window_name, om.dragAndDropSquare, [window_name, img])
    cv2.imshow(window_name, img)
    cv2.waitKey()
    getCirclePoint.sort5LocationPoint()
    cv2.destroyAllWindows()
