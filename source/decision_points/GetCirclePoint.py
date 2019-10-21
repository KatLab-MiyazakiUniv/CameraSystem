"""
@file: GetCirclePoint.py
@author: Tatsumi0000
@brief: 左上の（数字の1）の黄色い交点サークル4箇所とブロックサークル1をクリックするとすべてのサークルの座標を取得する
"""

from source.decision_points.module import onMouse as om
import cv2
import numpy as np


class GetCirclePoint:

    def __init__(self):
        """コンストラクタ
        """
        self.cc_points = np.empty((16, 2))  # 交点サークル
        self.bc_points = np.empty((8, 2))  # ブロックサークル


if __name__ == '__main__':
    getCirclePoint = GetCirclePoint()
    img = cv2.imread("./../img/clip_field.png")
    window_name = "WindowDAYO"
    mouse_count = 5
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, om.dragAndDropSquare,
                         [window_name, img, getCirclePoint.cc_points, getCirclePoint.bc_points])
    cv2.imshow(window_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()
