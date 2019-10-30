"""
@file: move_get_circle_point.py
@author: Tatsumi0000
@brief: 取得した座標をtkinterで描画し，マウスで動かせるようにし座標の微調整をする．
"""

import cv2.cv2 as cv2
import tkinter as tk
from PIL import Image, ImageTk
from source.decision_points import get_circle_point as gcp


class Points:
    def __init__(self):
        self.ix = self.iy = 0  # 押したxy座標
        self.item_id = ()  # オブジェクトのID


class MoveGetCirclePoint(tk.Frame):
    def __init__(self, master, title='Show Image', img='./../img/clip_field.png'):
        """コンストラクタ
        """
        super().__init__(master)
        self.img = Image.open(img)
        self.image_tk = ImageTk.PhotoImage(self.img)
        width, height = self.img.size
        self.points = Points()
        self.title = title
        self.get_circle_point = gcp.GetCirclePoint()
        master.title(title)
        self.canvas = tk.Canvas(master, width=width, height=height)  # Canvas作成
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)  # ImageTk画像配置
        self.canvas.pack()

    def setGetCirclePoint(self, get_circle_point):
        """
        get_circle_pointのセッター
        :param get_circle_point:
        :type get_circle_point: GetCirclePoint
        :return:
        """
        self.get_circle_point = get_circle_point

    def drawGetCirclePoint(self):
        for i in range(self.get_circle_point.CROSS_CIRCLE_POINTS):
            if i < self.get_circle_point.BLOCK_CIRCLE_POINTS:  # ブロックサークル
                self.canvas.create_oval(self.get_circle_point.bc_points[i, 0] - 5,  # 左上角のx座標
                                        self.get_circle_point.bc_points[i, 1] - 5,  # 左上角のy座標
                                        self.get_circle_point.bc_points[i, 0] + 5,  # 右下角のx座標
                                        self.get_circle_point.bc_points[i, 1] + 5, fill='red',  # 右下角のx座標, 塗りつぶす色
                                        tags='b{0}'.format(i))  # tags=オブジェクト固有の番号
                self.canvas.tag_bind('b{0}'.format(i), "<ButtonPress-1>", self.mousePressed)
                self.canvas.tag_bind('b{0}'.format(i), "<B1-Motion>", self.mouseDragged)
                # self.canvas.create_text(self.get_circle_point.bc_points[i, 0] + 25,  # x座標
                #                         self.get_circle_point.bc_points[i, 1] - 15,  # y座標
                #                         text='({}, {})'.format(self.get_circle_point.bc_points[i, 0],
                #                                                self.get_circle_point.bc_points[i, 1]),
                #                         fill='blue',  # 文字色
                #                         tags='b{0}'.format(i))

            # 交点サークルの描画
            self.canvas.create_oval(self.get_circle_point.cc_points[i, 0] - 5,  # 左上角のx座標
                                    self.get_circle_point.cc_points[i, 1] - 5,  # 左上角のy座標
                                    self.get_circle_point.cc_points[i, 0] + 5,  # 右下角のx座標
                                    self.get_circle_point.cc_points[i, 1] + 5, fill='green',  # 右下角のx座標, 塗りつぶす色
                                    tags='c{0}'.format(i))  # tags=オブジェクト固有の番号
            # self.canvas.create_text(self.get_circle_point.cc_points[i, 0] + 25,  # x座標
            #                         self.get_circle_point.cc_points[i, 1] - 15,  # y座標
            #                         text='({}, {})'.format(self.get_circle_point.cc_points[i, 0],
            #                                                self.get_circle_point.cc_points[i, 1]),
            #                         fill='blue',  # 文字色
            #                         tags='c{0}'.format(i))
            self.canvas.tag_bind('c{0}'.format(i), "<ButtonPress-1>", self.mousePressed)
            self.canvas.tag_bind('c{0}'.format(i), "<B1-Motion>", self.mouseDragged)

    def mousePressed(self, event):
        """
        マウスが押されると呼ばれる
        :param event:
        :return:
        """
        self.points.item_id = self.canvas.find_closest(event.x, event.y)
        print(self.canvas.find_closest(event.x, event.y))
        tag = self.canvas.gettags(self.points.item_id[0])[0]
        item = self.canvas.type(tag)
        # print('押されたのは：{}'.format(tag))
        self.points.ix = event.x
        self.points.iy = event.y

    def mouseDragged(self, event):
        """
        マウスがドラッグした時に呼ばれる
        :param event:
        :return:
        """
        try:
            self.points.item_id = self.canvas.find_closest(event.x, event.y)
            tag = self.canvas.gettags(self.points.item_id[0])[0]
            item = self.canvas.type(tag)
            delta_x = event.x - self.points.ix
            delta_y = event.y - self.points.iy
            if item == 'oval':  # 円のとき
                x0, y0, x1, y1 = self.canvas.coords(self.points.item_id)  # 左上のxy座標と右下のxy座標を取得
                self.canvas.coords(self.points.item_id, x0 + delta_x, y0 + delta_y, x1 + delta_x, y1 + delta_y)
                self.points.ix = event.x
                self.points.iy = event.y
        except IndexError:
            print('マウスの動きが早すぎます．')

    def runGetCirclePoint(self):
        img = './../img/clip_field.png'
        window_name = 'WindowDAYO'
        img = cv2.imread(img)
        self.get_circle_point = gcp.GetCirclePoint(window_name=window_name)
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.get_circle_point.dragAndDropSquare,
                             [window_name, img, self.get_circle_point])
        cv2.imshow(window_name, img)
        cv2.moveWindow(window_name, 100, 100)  # 左上にウィンドウを出す
        cv2.waitKey()
        print(self.get_circle_point.named_points)

    def run(self):
        print('プログラムが起動しました．ウィンドウが出ない場合は，後ろにウィンドウがでてるかもしれません．')
        self.runGetCirclePoint()
        self.drawGetCirclePoint()
        self.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    move_get_circle_point = MoveGetCirclePoint(master=root)  # 台形補正した画像をを準備して表示
    move_get_circle_point.run()
