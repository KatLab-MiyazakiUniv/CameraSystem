# https://qiita.com/otakoma/items/04e525ac74b7191dffe6 より参照

import sys

import numpy as np
import cv2


class PointList:
    def __init__(self, npoints=4):
        self.npoints = npoints
        self.ptlist = np.empty((npoints, 2), dtype=int)
        self.pos = 0
        self.named_points = {"l_top": None, "l_btm": None, "r_top": None, "r_btm": None}

    def add(self, x, y):
        if self.pos < self.npoints:
            self.ptlist[self.pos, :] = [x, y]
            self.pos += 1
            return True
        return False

    def trans(self):
        sum_list = np.sum(self.ptlist, axis=1)
        x_list = self.ptlist[:, 0]
        y_list = self.ptlist[:, 1]
        self.named_points["r_btm"] = self.ptlist[np.argmax(x_list)]
        self.named_points["l_top"] = self.ptlist[np.argmin(x_list)]
        self.named_points["r_top"] = self.ptlist[np.argmin(y_list)]
        self.named_points["l_btm"] = self.ptlist[np.argmax(y_list)]
        print(self.named_points)

    def add_point(self, img, wname="MouseEvent"):
        cv2.setMouseCallback(wname, self._add_point, [wname, img, self])
        cv2.imshow(wname, img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    @staticmethod
    def _add_point(event, x, y, flag, params):
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
            if ptlist.pos == ptlist.npoints:
                print(ptlist.ptlist)
                cv2.line(img, (ptlist.ptlist[0][0], ptlist.ptlist[0][1]),
                         (ptlist.ptlist[1][0], ptlist.ptlist[1][1]), (0, 255, 0), 3)
                cv2.line(img, (ptlist.ptlist[1][0], ptlist.ptlist[1][1]),
                         (ptlist.ptlist[2][0], ptlist.ptlist[2][1]), (0, 255, 0), 3)
                cv2.line(img, (ptlist.ptlist[2][0], ptlist.ptlist[2][1]),
                         (ptlist.ptlist[3][0], ptlist.ptlist[3][1]), (0, 255, 0), 3)
                cv2.line(img, (ptlist.ptlist[3][0], ptlist.ptlist[3][1]),
                         (ptlist.ptlist[0][0], ptlist.ptlist[0][1]), (0, 255, 0), 3)


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
    ptlist = PointList()
    ptlist.add_point()
    ptlist.trans()


if __name__ == '__main__':
    main()
