"""
@file: get_circle_point.py
@author: Tatsumi0000
@brief: ブロックサークルと交点サークルを囲むだけで各サークルの座標を取得．
"""

import cv2
import numpy as np


class GetCirclePoint:

    def __init__(self, window_name=None):
        """コンストラクタ
        """
        self.CROSS_CIRCLE_POINTS = 16  # 交点サークルの個数
        self.BLOCK_CIRCLE_POINTS = 8   # ブロックサークルの個数
        self.POINTS_NUMBER = 2         # 座標の個数
        self.cc_points = np.empty((self.CROSS_CIRCLE_POINTS, self.POINTS_NUMBER), dtype=int)  # 交点サークル
        self.bc_points = np.empty((self.BLOCK_CIRCLE_POINTS, self.POINTS_NUMBER), dtype=int)  # ブロックサークル
        self.ix = self.iy = 0  # 起点となる座標
        # サークルを選択するモード．0だと．交点サークルを囲むモード．1だとブロックサークルを囲むモード．2以上だと終了モード
        self.circle_mode = 0
        self.mode = False  # Trueだと青い囲む枠が出てくる
        # 各サークルの座標がX，Y座標が入っている辞書型（BlockPointListの丸パクリ）
        self.named_points = {
            "c00": None, "c10": None, "c20": None, "c30": None,
            "b1": None, "b2": None, "b3": None,
            "c01": None, "c11": None, "c21": None, "c31": None,
            "b4": None, "b5": None,
            "c02": None, "c12": None, "c22": None, "c32": None,
            "b6": None, "b7": None, "b8": None,
            "c03": None, "c13": None, "c23": None, "c33": None,
        }
        self.window_name = window_name

    def add(self):
        """
        交点サークル，ブロックサークルの座標を辞書型に代入する．
        きちんとソートされていないとめちゃくちゃになるので，取り扱い注意．
        :return:
        """
        # ブロックサークルの座標を代入．
        for i in range(self.BLOCK_CIRCLE_POINTS):
            key = 'b{0}'.format(i + 1)
            self.named_points[key] = [int(p) for p in self.bc_points[i]]

        # 交点サークルの座標を代入．
        cross_circle_count = 0
        for i in range(4):
            for j in range(4):
                key = 'c{0}{1}'.format(j, i)
                self.named_points[key] = [int(p) for p in self.cc_points[cross_circle_count]]
                cross_circle_count += 1

    @staticmethod
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

    def drawAllPoints(self, img, points, win_name=None):
        if win_name is None:
            win_name = self.window_name
        for i in range(points.shape[0]):
            # print("({0}, {1})" .format(cc_points[i, 0], cc_points[i, 1]))
            self.drawPoints(img, points[i, 0], points[i, 1])
            # print("{},{}".format(calc_cc_points[i, 0], calc_cc_points[i, 1]))
            img = cv2.circle(img, (points[i, 0], points[i, 1]), 5, (255, 255, 0), -1)
            cv2.imshow(win_name, img)

    @staticmethod
    def calcPoints(points, column) -> np.ndarray:
        """
        分割するときは切り捨てにしている
        columnが8ならブロックサークルの分割，16なら交点サークルの分割をする．それ以外だとすべて0の座標を返す．
        :param points:
        :param column:
        :return:
        """

        circle_points = np.zeros((column, 2), dtype=int)
        x_distance = points[1, 0] - points[0, 0]  # xの距離
        y_distance = points[2, 1] - points[0, 1]  # yの距離
        # print('前{0}'.format(circle_points))
        if column == 8:  # ブロックサークルのとき
            # 交点サークルは，1/3に分割
            # x座標
            circle_points[0, 0] = circle_points[3, 0] = circle_points[5, 0] = points[0, 0]
            circle_points[1, 0] = circle_points[6, 0] = x_distance * 1 // 2 + points[0, 0]
            circle_points[2, 0] = circle_points[4, 0] = circle_points[7, 0] = points[1, 0]
            # y座標
            circle_points[0:4, 1] = points[0, 1]
            circle_points[3:5, 1] = y_distance * 1 // 2 + points[0, 1]
            circle_points[5:, 1] = points[3, 1]
        elif column == 16:  # 交点サークルのとき
            # ブロックサークルは，半分に分割
            # x座標
            circle_points[0:13:4, 0] = points[0, 0]
            circle_points[1:14:4, 0] = x_distance * 1 // 3 + points[0, 0]
            circle_points[2:15:4, 0] = x_distance * 2 // 3 + points[0, 0]
            circle_points[3:16:4, 0] = points[3, 0]
            # y座標
            circle_points[0:4, 1] = points[0, 1]
            circle_points[4:8, 1] = y_distance * 1 // 3 + points[0, 1]
            circle_points[8:12, 1] = y_distance * 2 // 3 + points[0, 1]
            circle_points[12:, 1] = points[3, 1]
        else:
            return circle_points

        # print("座標計算結果：{}".format(circle_points))
        return circle_points

    @staticmethod
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
        window_name, img, get_circle_point = param
        h = img.shape[0]  # 画像の高さを取る
        w = img.shape[1]  # 画像の幅を取る
        if event == cv2.EVENT_MOUSEMOVE and get_circle_point.circle_mode <= 1:  # マウスが動いたときかつ囲むモードのとき
            img_copy = np.copy(img)
            h = img_copy.shape[0]  # 画像の高さを取る
            w = img_copy.shape[1]  # 画像の幅を取る
            # cv2.line(画像, (x1, y1), (x2, y2), (r, g, b))
            cv2.line(img_copy, (x, 0), (x, h), (0, 0, 255))  # 縦の線
            cv2.line(img_copy, (0, y), (w, y), (0, 0, 255))  # 横の線
            if get_circle_point.mode:  # ドラッグ・アンド・ドロップで範囲指定モードがTrueなら
                # cv2.rectangle(画像, 起点の(x, y), 終点の(x, y), 線の色(r, g, b), 線の太さ)
                cv2.rectangle(img_copy, (get_circle_point.ix, get_circle_point.iy), (x, y), (255, 0, 0), thickness=2)
            cv2.imshow(window_name, img_copy)

        if event == cv2.EVENT_LBUTTONDOWN and get_circle_point.circle_mode <= 1:  # 左ボタンを押下したとき
            get_circle_point.ix, get_circle_point.iy = x, y
            print('起点の座標：({0}, {1})'.format(get_circle_point.ix, get_circle_point.iy))
            get_circle_point.mode = True  # ドラッグ・アンド・ドロップで範囲指定モードをON

        if event == cv2.EVENT_LBUTTONUP and get_circle_point.circle_mode <= 1:  # マウスの左ボタンを上げたとき
            cv2.rectangle(img, (get_circle_point.ix, get_circle_point.iy), (x, y), (255, 0, 0), thickness=2)  # 四角形を描画
            get_circle_point.drawPoints(img, get_circle_point.ix, get_circle_point.iy)  # 始点の頂点
            get_circle_point.drawPoints(img, x, get_circle_point.iy)  # 始点の横の頂点
            get_circle_point.drawPoints(img, get_circle_point.ix, y)  # 終点の横の頂点
            get_circle_point.drawPoints(img, x, y)  # 終点の頂点
            square_points = np.empty((4, 2))  # 0行目左上．1行目右上．2行目左下．3行目右下
            ix, iy = get_circle_point.ix, get_circle_point.iy
            if w / 2 <= ix and h / 2 >= iy:  # 起点の座標が第一象限のとき
                square_points = np.array([[x, iy], [ix, iy], [x, y], [ix, y]])
            elif w / 2 >= ix and h / 2 >= iy:  # 起点の座標が第二象限のとき
                # print('{}'.format('第二象限'))
                square_points = np.array([[ix, iy], [x, iy], [ix, y], [x, y]])
            elif w / 2 >= ix and h / 2 <= iy:  # 起点の座標が第三象限のとき
                square_points = np.array([[ix, y], [x, y], [ix, iy], [x, iy]])
            else:  # それ以外（起点の座標が第四象限のとき）
                square_points = np.array([[x, y], [ix, y], [x, iy], [ix, iy]])

            if get_circle_point.circle_mode == 0:  # 交点サークルを囲むモード
                get_circle_point.cc_points = get_circle_point.calcPoints(points=square_points, column=16)
                get_circle_point.drawAllPoints(img, get_circle_point.cc_points)
            elif get_circle_point.circle_mode == 1:  # ブロックサークルを囲むモード
                get_circle_point.bc_points = get_circle_point.calcPoints(points=square_points, column=8)
                get_circle_point.drawAllPoints(img, get_circle_point.bc_points)
                # print('代入前：{0}'.format(get_circle_point.named_points))
                get_circle_point.add()
                # print('代入後：{0}'.format(get_circle_point.named_points))
            else:
                print('m9( ´,_ゝ｀)ﾌﾟｯ')
            get_circle_point.circle_mode += 1
            get_circle_point.mode = False  # ドラッグ・アンド・ドロップで範囲指定モードをOFF


# 自分をmain関数だと思っている精神異常者
def main():
    img = './../img/clip_field.png'
    window_name = 'WindowDAYO'
    img = cv2.imread(img)
    get_circle_point = GetCirclePoint()
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, get_circle_point.dragAndDropSquare,
                         [window_name, img, get_circle_point])
    cv2.imshow(window_name, img)
    cv2.moveWindow(window_name, 100, 100)  # 左上にウィンドウを出す
    cv2.waitKey()
    print(get_circle_point.named_points)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
