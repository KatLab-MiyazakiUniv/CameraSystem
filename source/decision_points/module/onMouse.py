"""
@file: onMouse.py
@author: Tatsumi0000
@brief:
"""

from source.decision_points import GetCirclePoint as gcp
from source.decision_points.module import calcPoints as cp
import cv2
import numpy as np


def onMouse(event, x, y, flags, param) -> None:
    """
    マウスでポチポチするやつ．仕様変更によりいらない子になった．
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

    if event == cv2.EVENT_LBUTTONDOWN:  # 左ボタンをクリックしたとき
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


ix = iy = h = w = 0
mode = False


def dragAndDropSquare(event, x, y, flags, param) -> None:
    """
    画像上でドラッグアンドドロップした範囲に対して四角形を描画する
    :param event: CV_EVENT_* の内の1つ
    :param x: 画像座標系におけるマウスポインタのX座標
    :param y: 画像座標系におけるマウスポインタのY座標
    :param flags: CV_EVENT_FLAG_* の論理和
    :param param: コールバック関数に渡される，ユーザ定義パラメータ
    :return: None
    """
    window_name, img, cc_points, bc_points = param
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが動いたとき
        global ix, iy, h, w, mode
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
    if event == cv2.EVENT_LBUTTONUP:  # マウスの左ボタンを上げたとき
        cv2.rectangle(img, (ix, iy), (x, y), (255, 0, 0), thickness=2)  # 四角形を描画
        drawPoints(img, ix, iy)  # 始点の頂点
        drawPoints(img, x, iy)  # 始点の横の頂点
        drawPoints(img, ix, y)  # 終点の横の頂点
        drawPoints(img, x, y)  # 終点の頂点
        square_points = np.empty((4, 2))  # 0行目左上．1行目左下．2行目右上．3行目右下
        if w/2 <= ix and h/2 >= iy:  # 起点の座標が第一象限のとき
            print('{}'. format('第一象限'))
            square_points = np.array([[x, iy], [x, y], [ix, iy], [ix, y]])
        elif w/2 >= ix and h/2 >= iy:  # 起点の座標が第二象限のとき
            print('{}'.format('第二象限'))
            square_points = np.array([[ix, iy], [ix, y], [x, iy], [x, y]])
        elif w/2 >= ix and h/2 <= iy:  # 起点の座標が第三象限のとき
            print('{}'.format('第三象限'))
            square_points = np.array([[ix, y], [ix, iy], [x, y], [x, iy]])
        else:  # それ以外（起点の座標が第四象限のとき）
            print('{}'.format('第四象限'))
            square_points = np.array([[x, y], [x, iy], [ix, y], [ix, iy]])
        print('終点の座標：({0}, {1})'.format(x, y))
        print('各頂点の座標：({0})'.format(square_points))
        print("")
        calc_cc_points = cp.calcPoints(square_points, cc_points)
        for i in range(calc_cc_points.shape[0]):
            # print("({0}, {1})" .format(cc_points[i, 0], cc_points[i, 1]))
            drawPoints(img, cc_points[i, 0], cc_points[i, 1])
            img = cv2.circle(img, (cc_points[i, 0], cc_points[i, 1]), 5, (255, 255, 0), -1)
            cv2.imshow(window_name, img)
        # print("{0}" .format(cp.calcPoints(square_points, cc_points)))

        mode = False  # ドラッグ・アンド・ドロップで範囲指定モードをOFF


def drawPoints(img, x, y):
    """
    座標を描画する
    :param img: 画像
    :type img: ndarray
    :param x: x座標
    :type x: int
    :param y: y座標
    :param y: int
    :return None:
    """
    cv2.putText(img, '({0}, {1})'.format(x, y), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))


if __name__ == '__main__':
    pass
