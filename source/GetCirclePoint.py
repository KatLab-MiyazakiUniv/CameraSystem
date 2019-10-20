"""
@file: GetCirclePoint.py
@author: Tatsumi0000
@brief: 左上の（数字の1）の黄色い交点サークル4箇所とブロックサークル1をクリックするとすべてのサークルの座標を取得する
"""

import cv2
import numpy as np


class GetCirclePoint:

    def __init__(self):
        """コンストラクタ
        """
        self.mouse_point = np.zeros((5, 2))
        # print(self.mouse_point)

    def captureCamera(self) -> None:
        """
        動画をキャプチャして画像として切り出して保存する．
        :return:
        """
        pass

    def decision5LocationPoint(self, img_path="./img/") -> None:
        """
        交点サークル4箇所とブロックサークル1箇所をクリックして座標を指定する．
        ただし，「1」のところをクリックしないとだめ
        :param img_path: str
            画像のパス（デフォルト引数は，XXXX）
        :return:
        """
        pass


def onMouse(event, x, y, flags, param) -> None:
    """
    マウスの処理を行う
    参考：http://opencv.jp/opencv-2svn/py/highgui_user_interface.html?highlight=setmousecallback#SetMouseCallback
    :param event: CV_EVENT_* の内の1つ
    :param x: 画像座標系におけるマウスポインタのX座標
    :param y: 画像座標系におけるマウスポインタのY座標
    :param flags: CV_EVENT_FLAG_* の論理和
    :param param: コールバック関数に渡される，ユーザ定義パラメータ
    """

    window_name, img = param
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが動いたとき
        img_copy = np.copy(img)
        h = img_copy.shape[0]  # 画像の高さを取る
        w = img_copy.shape[1]  # 画像の幅を取る
        # cv2.line(画像, (x1, y1), (x2, y2), (r, g, b))
        cv2.line(img_copy, (x, 0), (x, h), (0, 0, 255))  # 縦の線
        cv2.line(img_copy, (0, y), (w, y), (0, 0, 255))  # 横の線
        cv2.imshow(window_name, img_copy)

    if event == cv2.EVENT_LBUTTONDOWN:  # 左ボタンをクリックしたとき
        pass


if __name__ == '__main__':
    img = cv2.imread("./img/clip_field.png")
    window_name = "WindowDAYO"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, onMouse, [window_name, img])
    cv2.imshow(window_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()
