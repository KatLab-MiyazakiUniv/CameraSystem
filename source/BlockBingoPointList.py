"""
    PointList.py より参照（ほぼコピペ）

    @file: BlockBingoPointList.py
    @author: UEDA Takahiro
    @brief: ブロックビンゴエリア画像の交点サークル、ブロックサークルの中心座標をマウスで設定する
"""

import sys

import numpy as np
import cv2


class BlockBingoPointList:
    def __init__(self, npoints=24):
        self.npoints = npoints
        self.ptlist = []
        self.pos = 0
        self.named_points = {
            "c00": None, "c10": None, "c20": None, "c30": None,
            "b1": None, "b2": None, "b3": None,
            "c01": None, "c11": None, "c21": None, "c31": None,
            "b4": None, "b5": None,
            "c02": None, "c12": None, "c22": None, "c32": None,
            "b6": None, "b7": None, "b8": None,
            "c03": None, "c13": None, "c23": None, "c33": None,
            }

    def add(self, x, y):
        if self.pos < self.npoints:
            self.ptlist.append((x, y))
            self.pos += 1
            print("[各種サークルの座標設定] 指定された座標の数: {}/{}[個]".format(self.pos, self.npoints))
            return True
        return False

    def trans(self):
        # 点の数をチェック
        if self.pos != self.npoints:
            print("[各種サークルの座標設定] 指定した座標の数（{}/{}[個]）が足りません。".format(self.pos, self.npoints))
            return
        
        # y座標を基準にソート
        self.ptlist = sorted(self.ptlist, key=lambda x: x[1])

        # 各行ごとに分割しx座標を基準にソート（keyは指定しなくても良い）
        ptlist_cc = []
        ptlist_bc = []
        ptlist_cc.append(sorted(self.ptlist[0:4], key=lambda x: x[0]))
        ptlist_bc.extend(sorted(self.ptlist[4:7], key=lambda x: x[0]))
        ptlist_cc.append(sorted(self.ptlist[7:11], key=lambda x: x[0]))
        ptlist_bc.extend(sorted(self.ptlist[11:13], key=lambda x: x[0]))
        ptlist_cc.append(sorted(self.ptlist[13:17], key=lambda x: x[0]))
        ptlist_bc.extend(sorted(self.ptlist[17:20], key=lambda x: x[0]))
        ptlist_cc.append(sorted(self.ptlist[20:24], key=lambda x: x[0]))

        # ブロックサークルの座標を辞書に格納
        for i in range(8):
            key = "b{}".format(i + 1)
            self.named_points[key] = ptlist_bc[i]
        
        # 交点サークルの座標を辞書に格納
        for y in range(4):
            for x in range(4):
                key = "c{}{}".format(x, y)
                self.named_points[key] = ptlist_cc[y][x]

        print(self.named_points)

    @staticmethod
    def add_point(event, x, y, flag, params):
        wname, img, ptlist = params
        if event == cv2.EVENT_MOUSEMOVE:  # マウスが移動したときにx線とy線を更新する
            img2 = np.copy(img)
            h, w = img2.shape[0], img2.shape[1]
            cv2.line(img2, (x, 0), (x, h - 1), (255, 0, 0))
            cv2.line(img2, (0, y), (w - 1, y), (255, 0, 0))
            cv2.imshow(wname, img2)

        if event == cv2.EVENT_LBUTTONDOWN:  # レフトボタンをクリックしたとき、ptlist配列にx,y座標を格納する
            if ptlist.add(x, y):
                print('[%d] ( %d, %d )' % (ptlist.pos - 1, x, y))
                cv2.circle(img, (x, y), 3, (0, 0, 255), 3)
                cv2.imshow(wname, img)
            else:
                print('All points have selected.  Press ESC-key.')


def main():
    url = "http://raspberrypi.local/?action=stream"
    # VideoCaptureのインスタンスを作成する。
    cap = cv2.VideoCapture(url)  # カメラシステムを使う場合
    if not cap.isOpened():
        print("画像のキャプチャに失敗しました")
        sys.exit()

    # 画像をキャプチャ
    ret, img = cap.read()
    wname = "MouseEvent"
    cv2.namedWindow(wname)
    ptlist = BlockBingoPointList()
    ptlist.add_point()
    ptlist.trans()


if __name__ == '__main__':
    main()
