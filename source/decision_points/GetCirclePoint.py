"""
@file: GetCirclePoint.py
@author: Tatsumi0000
@brief: ブロックサークルと交点サークルを囲むだけで各サークルの座標を取得．
"""

from source.decision_points.module import onMouse as om
import cv2
import numpy as np


class GetCirclePoint:

    def __init__(self):
        """コンストラクタ
        """
        self.cc_points = np.zeros((16, 2), dtype=int)  # 交点サークル
        self.bc_points = np.zeros((8, 2), dtype=int)  # ブロックサークル
        self.toriaezu_points = np.zeros((4, 2), dtype=int)  # デバッグ用のとりあえず

    def startGetCirclePoint(self, img='./../img/clip_field.png', window_name='WindowDAYO'):
        """

        :return:
        """
        img = cv2.imread(img)
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, om.dragAndDropSquare,
                             [window_name, img, self.cc_points, self.bc_points])
        cv2.imshow(window_name, img)
        cv2.moveWindow(window_name, 100, 100)  # 左上にウィンドウを出す
        cv2.waitKey()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    getCirclePoint = GetCirclePoint()
    getCirclePoint.startGetCirclePoint()
    # img = cv2.imread("./../img/clip_field.png")
    # window_name = "WindowDAYO"
    # mouse_count = 5
    # cv2.namedWindow(window_name)
    # cv2.setMouseCallback(window_name, om.dragAndDropSquare,
    #                      [window_name, img, getCirclePoint.cc_points, getCirclePoint.bc_points])
    # cv2.imshow(window_name, img)
    # cv2.moveWindow(window_name, 100, 100)  # 左上にウィンドウを出す
    # cv2.waitKey()
    # cv2.destroyAllWindows()
