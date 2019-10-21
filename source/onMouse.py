"""
@file: onMouse.py
@author: Tatsumi0000
@brief:
"""

import cv2
import numpy as np


def onMouse(event, x, y, flags, param) -> None:
    """
    マウスでポチポチするやつ．
    参考：http://opencv.jp/opencv-2svn/py/highgui_user_interface.html?highlight=setmousecallback#SetMouseCallback
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html
    :param event: CV_EVENT_* の内の1つ
    :param x: 画像座標系におけるマウスポインタのX座標
    :param y: 画像座標系におけるマウスポインタのY座標
    :param flags: CV_EVENT_FLAG_* の論理和
    :param param: コールバック関数に渡される，ユーザ定義パラメータ
    """

    window_name, img, mouse_count, mouse_point = param
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが動いたとき
        img_copy = np.copy(img)
        h = img_copy.shape[0]  # 画像の高さを取る
        w = img_copy.shape[1]  # 画像の幅を取る
        # cv2.line(画像, (x1, y1), (x2, y2), (r, g, b))
        cv2.line(img_copy, (x, 0), (x, h), (0, 0, 255))  # 縦の線
        cv2.line(img_copy, (0, y), (w, y), (0, 0, 255))  # 横の線
        cv2.imshow(window_name, img_copy)

    if event == cv2.EVENT_LBUTTONDOWN:  # 左ボタンをクリックしたとき（5回まで）
        if len(mouse_point) < mouse_count:  # 配列のサイズが5以下の場合
            # cv2.circle(画像, (円の中心), 半径, (r, g, b), 負の場合塗りつぶし)
            img = cv2.circle(img, (x, y), 5, (255, 255, 0), -1)
            # cv2.putText(画像, 文字列, 描画する文字列の左下の座標, フォントのタイプ, フォントの縮尺, 文字色(r, g, b))
            cv2.putText(img, '({0}, {1})'.format(x, y), (x + 5, y - 15), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))
            # mouse_point.append([x, y])
            np.append(mouse_point, [x, y], axis=1)
            cv2.imshow(window_name, img)
            print('{0}回目：{1}'.format(len(mouse_point), mouse_point))
        else:
            print("座標取得の終了")


ix = iy = -1
mode = False
def dragAndDropSquare(event, x, y, flags, param) -> None:
    """
    画像上でドラッグアンドドロップ範囲に対して四角形を描画する
    :param event: CV_EVENT_* の内の1つ
    :param x: 画像座標系におけるマウスポインタのX座標
    :param y: 画像座標系におけるマウスポインタのY座標
    :param flags: CV_EVENT_FLAG_* の論理和
    :param param: コールバック関数に渡される，ユーザ定義パラメータ
    :return: None
    """
    window_name, img,  = param
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが動いたとき
        global ix, iy, mode
        img_copy = np.copy(img)
        h = img_copy.shape[0]  # 画像の高さを取る
        w = img_copy.shape[1]  # 画像の幅を取る
        # cv2.line(画像, (x1, y1), (x2, y2), (r, g, b))
        cv2.line(img_copy, (x, 0), (x, h), (0, 0, 255))  # 縦の線
        cv2.line(img_copy, (0, y), (w, y), (0, 0, 255))  # 横の線
        if mode:  # ドラッグ・アンド・ドロップで範囲指定モードがTrueなら
            # cv2.rectangle(画像, 起点の(x, y), 終点の(x, y), 線の色(r, g, b), 線の太さ)
            cv2.rectangle(img_copy, (ix, iy), (x, y), (255, 0, 0), thickness=2)
        cv2.imshow(window_name, img_copy)

    if event == cv2.EVENT_LBUTTONDOWN:  # 左ボタンを押下したとき
        ix, iy = x, y
        print('起点の座標：({0}, {1})'.format(ix, iy))
        mode = True  # ドラッグ・アンド・ドロップで範囲指定モードをON
    if event == cv2.EVENT_LBUTTONUP:  # 左ボタンを上げたとき
        cv2.rectangle(img, (ix, iy), (x, y), (255, 0, 0), thickness=2)
        print('終点の座標：({0}, {1})'.format(x, y))
        mode = False  # ドラッグ・アンド・ドロップで範囲指定モードをOFF


if __name__ == '__main__':
    pass
