"""
@file: Camera.py
@author: Takahiro55555, korosuke613
@brief: カメラシステムから取得した画像から、数字カードの部分を切り抜き、台形補正する。
"""

import datetime
import sys

import cv2
import numpy as np

from PointList import PointList
from BlockBingoPointList import BlockBingoPointList

class Camera:
    def __init__(self, url="http://raspberrypi.local/?action=stream"):
        self.camera_url = url
        # NOTE: 座標を指定すると点や線が入ってしまうため処理用と座標指定用を分けた
        self.original_img = None # キャプチャしてきた元画像（処理用）
        self.original_img_dummy = None # キャプチャしてきた元画像（座標指定用）        
        self.block_bingo_img = None # 切り取ったブロックビンゴエリアの画像（処理用）
        self.block_bingo_img_dummy = None #  切り取ったブロックビンゴエリアの画像（座標指定用）

    def capture(self, url=None, padding=0):
        """
        URLから流れてくる映像をキャプチャし、静止画として保存する

        Parameters
        ----------
        url: str
            映像配信URL

        padding: int
            キャプチャした画像の余白（単位：px）。

        Returns
        -------
        target_name: numpy.ndarray
            キャプチャした静止画
        """
        if url is None:
            url = self.camera_url
        cap = cv2.VideoCapture(url)  # カメラシステムを使う場合
        if not cap.isOpened():
            # HACK: エラーを返した方がいいかも
            print("On file {}".format(__file__))
            print("画像のキャプチャに失敗しました")
            sys.exit()

        # カメラFPSを30FPSに設定
        cap.set(cv2.CAP_PROP_FPS, 30)

        # カメラ画像の横幅を1280に設定
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        # カメラ画像の縦幅を720に設定
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # ピクセル配列をゼロ初期化
        img = np.zeros((720, 1280, 3), dtype=np.uint8)
        img_img = np.zeros((720, 1280, 3), dtype=np.uint8)

        # 画像をキャプチャ
        ret, img = cap.read()
        ret_dummy, img_dummy = cap.read()

        # 余白を設定する
        tmp = img[:, :]
        height, width = img.shape[:2]
        new_img = cv2.resize(np.full((1, 1, 3), fill_value=255, dtype=np.uint8),
                             dsize=(width + padding * 2, height + padding * 2))
        new_img[padding:height + padding, padding:width + padding] = tmp
        # 余白を設定する
        tmp = img_dummy[:, :]
        height, width = img_dummy.shape[:2]
        new_img_dummy = cv2.resize(np.full((1, 1, 3), fill_value=255, dtype=np.uint8),
                             dsize=(width + padding * 2, height + padding * 2))
        new_img_dummy[padding:height + padding, padding:width + padding] = tmp

        # キャプチャ終了
        cap.release()

        # 画像をメンバ変数に格納
        self.original_img = new_img
        self.original_img_dummy = new_img_dummy

    def get_number_img(self, wname="CameraSystem", npoints=4, output_size=[420, 297]):
        ptlist = PointList(npoints)
        cv2.namedWindow(wname)
        cv2.setMouseCallback(wname, ptlist.add_point, [wname, self.original_img_dummy, ptlist])
        cv2.imshow(wname, self.original_img_dummy)
        cv2.waitKey()
        cv2.destroyAllWindows()
        ptlist.trans()
        # 画像を切り取り、保存する
        result_img = self.clip(self.original_img, output_size=output_size,
                               l_top=ptlist.named_points["l_top"], l_btm=ptlist.named_points["l_btm"],
                               r_btm=ptlist.named_points["r_btm"], r_top=ptlist.named_points["r_top"])

        # 台形補正の結果を表示（何かキーを押すと終了）
        cv2.imshow("color", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return result_img

    def get_block_bingo_img(self, wname="Clip 'Block Bingo' area", npoints=4, output_size = [640, 640]):
        ptlist = PointList(npoints)
        cv2.namedWindow(wname)
        cv2.setMouseCallback(wname, ptlist.add_point, [wname, self.original_img_dummy, ptlist])
        cv2.imshow(wname, self.original_img_dummy)
        cv2.waitKey()
        cv2.destroyAllWindows()
        ptlist.trans()
        # 画像を切り取り、保存する
        result_img = self.clip(self.original_img, output_size=output_size,
                               l_top=ptlist.named_points["l_top"], l_btm=ptlist.named_points["l_btm"],
                               r_btm=ptlist.named_points["r_btm"], r_top=ptlist.named_points["r_top"])
        result_img_dummy = self.clip(self.original_img_dummy, output_size=output_size,
                               l_top=ptlist.named_points["l_top"], l_btm=ptlist.named_points["l_btm"],
                               r_btm=ptlist.named_points["r_btm"], r_top=ptlist.named_points["r_top"])

        # 台形補正の結果を表示（何かキーを押すと終了）
        cv2.imshow("color", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.block_bingo_img = result_img
        self.block_bingo_img_dummy = result_img_dummy
        return result_img

    def get_circle_coordinates(self, wname="Choose circles", npoints=24):
        circle_ptlist = BlockBingoPointList(npoints)
        cv2.namedWindow(wname)
        cv2.setMouseCallback(wname, circle_ptlist.add_point, [wname, self.block_bingo_img_dummy, circle_ptlist])
        cv2.imshow(wname, self.block_bingo_img_dummy)
        cv2.waitKey()
        cv2.destroyAllWindows()
        circle_ptlist.trans()
        return circle_ptlist.named_points

    def clip(self, img, output_size=[420, 297],
             l_top=[-30, 460], l_btm=[190, 620],
             r_top=[400, 450], r_btm=[200, 360]):
        """
        画像から指定された座標の部分を切り抜き、台形補正し保存する。

        Parameters
        ----------
        src_img: numpy.ndarray
            入力画像

        output_size: list
            出力画像のサイズ。[高さ、横幅]の順

        l_top: list
            数字カードの左上の座標。[X, Y]の順

        l_btm: list
            数字カードの左下の座標。[X, Y]の順

        r_top: list
            数字カードの右上の座標。[X, Y]の順

        r_btm: list
            数字カードの右下の座標。[X, Y]の順

        Returns
        -------
        clipped_img: numpy.ndarray
            切り取った結果の画像

        Referrenced
        -----------
         https://note.nkmk.me/python-opencv-warp-affine-perspective/
        """
        # 出力サイズを引数から取得
        h, w = output_size
        # [左上の座標],[右上の座標],[左下の座標],[右下の座標]
        src_pts = np.array([l_top, r_top, l_btm, r_btm], dtype=np.float32)
        dst_pts = np.array([[0, 0], [w, 0], [0, h], [w, h]], dtype=np.float32)
        mat = cv2.getPerspectiveTransform(src_pts, dst_pts)

        clipped_img = cv2.warpPerspective(img, mat, (w, h))

        return clipped_img


if __name__ == '__main__':
    # ラズパイから映像を受信し、保存する
    camera = Camera()
    # 余白を設定
    camera.capture(padding=100)    
    num_img = camera.get_number_img() # 数字カードの画像

    bingo_img = camera.get_block_bingo_img() # ブロックビンゴエリアの画像
    circle_coordinates = camera.get_circle_coordinates() # 上記の画像における各種サークルの座標

    # 切り取った画像を表示
    cv2.imshow("", num_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    cv2.imshow("", bingo_img)
    cv2.waitKey()
    cv2.destroyAllWindows()
