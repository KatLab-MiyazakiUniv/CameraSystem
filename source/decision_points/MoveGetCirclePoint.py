"""
@file: move_get_circle_point.py
@author: Tatsumi0000
@brief: 取得した座標をtkinterで描画し，マウスで動かせるようにし座標の微調整をする．
"""

import cv2.cv2 as cv2
import tkinter as tk
from PIL import Image, ImageTk
from source.decision_points import GetCirclePoint as gcp


class Points:
    def __init__(self):
        """マウスで図形を動かす時に座標を管理するために使うクラス
        """
        self.ix = self.iy = 0  # 押したxy座標
        self.item_id = ()  # オブジェクトのID


class MoveGetCirclePoint(tk.Frame):
    def __init__(self, master, title='Show Image', img='./../img/clip_field.png'):
        """コンストラクタ
        """
        super().__init__(master)
        self.RADIUS = 5  # 描画する円の半径
        self.master.bind("<KeyPress>", self.key_event)  # キーボードを入力を受け付ける
        self.img = Image.open(img)
        self.image_tk = ImageTk.PhotoImage(self.img)
        width, height = self.img.size  # 画像のサイズ
        self.points = Points()
        self.get_circle_point = gcp.GetCirclePoint()
        self.master.title(title)
        self.canvas = tk.Canvas(self.master, width=width, height=height)  # Canvas作成
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)  # ImageTk画像配置
        self.canvas.pack()

    def set_get_circle_point(self, get_circle_point):
        """
        get_circle_pointのセッター
        :param get_circle_point:
        :type get_circle_point: GetCirclePoint
        :return:
        """
        self.get_circle_point = get_circle_point

    def draw_get_circle_point(self):
        """
        座標を描画する．
        :return:
        """
        for key, value in self.get_circle_point.named_points.items():
            if 'b' in key:  # ブロックサークルの描画
                self.canvas.create_oval(self.get_circle_point.named_points[key][0] - self.RADIUS,  # 左上角のx座標
                                        self.get_circle_point.named_points[key][1] - self.RADIUS,  # 左上角のy座標
                                        self.get_circle_point.named_points[key][0] + self.RADIUS,  # 右下角のx座標
                                        self.get_circle_point.named_points[key][1] + self.RADIUS, fill='red',
                                        # 右下角のx座標, 塗りつぶす色
                                        tags='{0}'.format(key))  # tags=オブジェクト固有の番号
            elif 'c' in key:  # 交点サークルの描画
                self.canvas.create_oval(self.get_circle_point.named_points[key][0] - self.RADIUS,  # 左上角のx座標
                                        self.get_circle_point.named_points[key][1] - self.RADIUS,  # 左上角のy座標
                                        self.get_circle_point.named_points[key][0] + self.RADIUS,  # 右下角のx座標
                                        self.get_circle_point.named_points[key][1] + self.RADIUS, fill='yellow',
                                        # 右下角のx座標, 塗りつぶす色
                                        tags='{0}'.format(key))  # tags=オブジェクト固有の番号
            self.canvas.tag_bind('{0}'.format(key), "<ButtonPress-1>", self.mouse_pressed)  # 右クリックの処理
            self.canvas.tag_bind('{0}'.format(key), "<B1-Motion>", self.mouse_dragged)  # マウスの動き

    def mouse_pressed(self, event):
        """
        マウスが押されると呼ばれる
        :param event:
        :return:
        """
        self.points.item_id = self.canvas.find_closest(event.x, event.y)  # クリックされた座標を渡して何がクリックされたかidを探す
        # print(self.canvas.find_closest(event.x, event.y))
        # tag = self.canvas.gettags(self.points.item_id[0])[0]  # idを渡してtagを探す
        # item = self.canvas.type(tag)
        # print('押されたのは：{}'.format(item))
        self.points.ix = event.x
        self.points.iy = event.y

    def mouse_dragged(self, event):
        """
        マウスがドラッグした時に呼ばれる
        :param event:
        :return:
        """
        try:
            self.points.item_id = self.canvas.find_closest(event.x, event.y)
            tag = self.canvas.gettags(self.points.item_id[0])[0]  # idを渡してtagを探す
            item = self.canvas.type(tag)  # タグを元に図形の形（？）を取得
            delta_x = event.x - self.points.ix
            delta_y = event.y - self.points.iy
            if item == 'oval':  # 円のとき
                x0, y0, x1, y1 = self.canvas.coords(self.points.item_id)  # 左上のxy座標と右下のxy座標を取得
                self.canvas.coords(self.points.item_id, x0 + delta_x, y0 + delta_y, x1 + delta_x, y1 + delta_y)
                self.points.ix = event.x
                self.points.iy = event.y
        except IndexError:
            print('マウスの動きが早すぎます．')

    def key_event(self, event):
        if event.char == 'q':  # キーボードのqが押されたら
            self.fix_point()
            self.master.quit()  # tkinterを終了
        if event.char == 'd':  # デバッグ用のd
            self.fix_point()
        print('押されたキーボード：{}'.format(event.char))

    def fix_point(self):
        """
        画面上のすべての座標を取得しnamed_pointsに代入する．
        本当は，マウスイベントが起こった時に対応する辞書型に代入したほうが圧倒的に効率的
        :return:
        """
        print('修正前： {0}'.format(self.get_circle_point.named_points))
        for object_id in self.canvas.find_all():
            tag = self.canvas.itemcget(object_id, 'tags')  # タグ名取得
            tag = tag.split()  # クリックされたタグは後ろにcurrentという文字列がつくので分割
            if tag:  # リストが空でないとき
                if self.canvas.type(tag[0]) == 'oval':  # oval（円）なら
                    x0, y0, x1, y1 = self.canvas.coords(tag[0])  # 座標の問い合わせ
                    x = int(x0 + self.RADIUS)  # 半径分中心に
                    y = int(y0 + self.RADIUS)  # 半径分中心に
                    self.get_circle_point.named_points[tag[0]] = [x, y]
        print('修正後： {0}'.format(self.get_circle_point.named_points))

    def run_get_circle_point(self):
        img = './../img/clip_field.png'
        window_name = 'WindowDAYO'
        img = cv2.imread(img)
        self.set_get_circle_point(gcp.GetCirclePoint(window_name=window_name))
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.get_circle_point.drag_and_drop_square,
                             [window_name, img, self.get_circle_point])
        cv2.imshow(window_name, img)
        cv2.moveWindow(window_name, 100, 100)  # 左上にウィンドウを出す
        cv2.waitKey()
        print(self.get_circle_point.named_points)

    def run(self):
        print('プログラムが起動しました．ウィンドウが出ない場合は，後ろにウィンドウがでてるかもしれません．')
        self.run_get_circle_point()
        self.draw_get_circle_point()
        self.mainloop()
        # self.fix_point()
        # self.debug()


if __name__ == '__main__':
    root = tk.Tk()
    move_get_circle_point = MoveGetCirclePoint(master=root)  # 台形補正した画像をを準備して表示
    move_get_circle_point.run()
