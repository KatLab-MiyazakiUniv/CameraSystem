"""
@file: move_get_circle_point.py
@author: Tatsumi0000
@brief: 取得した座標をtkinterで描画し，マウスで動かせるようにし座標の微調整をする．
"""

import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from source.decision_points import get_circle_point as gcp


class Points:
    def __init__(self):
        self.ix = self.iy = 0  # 押したxy座標
        self.item_id = []  # オブジェクトのID


class MoveGetCirclePoint:
    def __init__(self, title='Show Image', img='./../img/clip_field.png'):
        """コンストラクタ
        """
        self.points = Points()
        self.title = title
        self.img = img
        self.get_circle_point = gcp.GetCirclePoint()
        self.root = root
        self.image_rgb = self.convertBGRtoRGB()
        self.image_tk = self.convertImg()
        self.root.title(title)
        self.canvas = tk.Canvas(self.root, width=self.image_rgb.shape[0], height=self.image_rgb.shape[1])  # Canvas作成
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.image_tk, anchor='nw')  # ImageTk 画像配置
        self.canvas.pack()

    def convertImg(self):
        """
        RGBをPILに変換
        :return:
        """
        image_pil = Image.fromarray(self.image_rgb)  # RGBからPILフォーマットへ変換
        image_tk = ImageTk.PhotoImage(image_pil)  # ImageTkフォーマットへ変換
        return image_tk

    def convertBGRtoRGB(self):
        """
        imgreadで読み込んだの（BGR）をRGBに変換
        :return:
        """
        image_bgr = cv2.imread(self.img)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)  # imgreadはBGRなのでRGBに変換
        return image_rgb

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
                                        tags='b{}'.format(i))  # tags=オブジェクト固有の番号
                self.canvas.tag_bind('b{0}'.format(i), "<ButtonPress-1>", self.mousePressed)
                self.canvas.tag_bind('b{0}'.format(i), "<B1-Motion>", self.mouseDragged)
                self.canvas.tag_bind('b{0}'.format(i), "<ButtonRelease-1>", self.mouseReleased)

            # 交点サークルの描画
            self.canvas.create_oval(self.get_circle_point.cc_points[i, 0] - 5,  # 左上角のx座標
                                    self.get_circle_point.cc_points[i, 1] - 5,  # 左上角のy座標
                                    self.get_circle_point.cc_points[i, 0] + 5,  # 右下角のx座標
                                    self.get_circle_point.cc_points[i, 1] + 5, fill='green',  # 右下角のx座標, 塗りつぶす色
                                    tags='c{0}'.format(i))  # tags=オブジェクト固有の番号
            self.canvas.tag_bind('c{0}'.format(i), "<ButtonPress-1>", self.mousePressed)
            self.canvas.tag_bind('c{0}'.format(i), "<B1-Motion>", self.mouseDragged)
            self.canvas.tag_bind('c{0}'.format(i), "<ButtonRelease-1>", self.mouseReleased)

    def mousePressed(self, event):
        """
        マウスが押されると呼ばれる
        :param event:
        :return:
        """
        self.points.item_id = self.canvas.find_closest(event.x, event.y)
        tag = self.canvas.gettags(self.points.item_id[0])[0]
        item = self.canvas.type(tag)
        print('押されたのは：{}'.format(tag))
        self.points.pressed_x = event.x
        self.points.pressed_y = event.y

    def mouseDragged(self, event):
        self.points.item_id = self.canvas.find_closest(event.x, event.y)
        tag = self.canvas.gettags(self.points.item_id[0])[0]
        item = self.canvas.type(tag)
        print(item)
        delta_x = event.x - self.points.ix
        delta_y = event.y - self.points.iy
        print('eventの中身：{}' .format(event))
        if item == 'oval':
            x, y = self.canvas.coords(self.points.item_id)
            print('item_id')
            self.canvas.coords(self.points.item_id, delta_x+x, delta_y+y)
        self.points.ix = event.x
        self.points.iy = event.y

    def mouseReleased(self):
        pass

    def sub(self):
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


if __name__ == '__main__':
    # get_circle_point = gcp.GetCirclePoint()
    root = tk.Tk()
    move_get_circle_point = MoveGetCirclePoint()  # 台形補正した画像をを準備して表示
    move_get_circle_point.sub()
    move_get_circle_point.drawGetCirclePoint()
    move_get_circle_point.root.mainloop()
