"""
@file: Camera.py
@author: Takahiro55555, korosuke613
@brief: カメラシステムから取得した画像から、数字カードの部分を切り抜き、台形補正する。
"""

import sys
import os
import json

import cv2
import numpy as np

from decision_points.PointList import PointList
from decision_points.BlockBingoPointList import BlockBingoPointList
from decision_points.MoveGetCirclePoint import MoveGetCirclePoint


class Camera:
    def __init__(self, url="http://raspberrypi.local/?action=stream"):
        self.camera_url = url
        # NOTE: 座標を指定すると画像に点や線が入ってしまうため処理用と座標指定用を分けた
        self.original_img = None  # キャプチャしてきた元画像（処理用）
        self.original_img_dummy = None  # キャプチャしてきた元画像（座標指定用）
        self.block_bingo_img = None  # 切り取ったブロックビンゴエリアの画像（処理用）
        self.block_bingo_img_dummy = None  # 切り取ったブロックビンゴエリアの画像（座標指定用）
        self.loaded_settings_file = False
        self.modified_settings = False
        self.move_get_circle_point = MoveGetCirclePoint()

        # 以下ファイルへ保存するデータ
        self.number_img_range = None  # 数字カードを切り取るための座標情報
        self.block_bingo_img_range = None  # ブロックビンゴエリアを切り取るための座標情報
        self.block_bingo_circle_coordinates = None  # ブロックビンゴエリアの各種サークルの座標情報

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
        if img_dummy is None:
            img_dummy = img

        # 余白を設定する
        def create_padding(im):
            tmp = im[:, :]
            height, width = img.shape[:2]
            new_img = cv2.resize(np.full((1, 1, 3), fill_value=255, dtype=np.uint8),
                                 dsize=(width + padding * 2, height + padding * 2))
            new_img[padding:height + padding, padding:width + padding] = tmp
            return new_img

        # 画像をメンバ変数に格納
        self.original_img = create_padding(img)
        self.original_img_dummy = create_padding(img_dummy)

        # キャプチャ終了
        cap.release()

    def get_img(self, npoints, wname):
        ptlist = PointList(npoints)
        cv2.namedWindow(wname)
        cv2.setMouseCallback(wname, ptlist.add_point, [wname, self.original_img_dummy, ptlist])
        cv2.imshow(wname, self.original_img_dummy)
        cv2.moveWindow(wname, 0, 0)  # ウィンドウを左上に動かす
        cv2.waitKey()
        cv2.destroyAllWindows()
        ptlist.trans()
        # 切り取りのための座標情報をメンバ変数に格納
        return ptlist.named_points

    def get_number_img(self, wname="CameraSystem", npoints=4, output_size=(420, 297), is_debug=True):
        # ファイルから座標データを読み込んでいない場合は、切り取るための領域を選択する

        if self.number_img_range is None:
            # 切り取りのための座標情報をメンバ変数に格納
            self.number_img_range = self.get_img(npoints, wname)
            self.modified_settings = True

        # 画像を切り取る
        result_img = self.clip(self.original_img, output_size=output_size,
                               l_top=self.number_img_range["l_top"], l_btm=self.number_img_range["l_btm"],
                               r_btm=self.number_img_range["r_btm"], r_top=self.number_img_range["r_top"])
        # 台形補正の結果を表示（何かキーを押すと終了）
        if is_debug:
            cv2.imshow("color", result_img)
            cv2.moveWindow("color", 100, 100)  # ウィンドウを左上に動かす
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return result_img

    def get_block_bingo_img(self, wname="Clip 'Block Bingo' area", npoints=4, output_size=(640, 640), is_debug=True):
        # ファイルから座標データを読み込んでいない場合は、切り取るための領域を選択する
        if self.block_bingo_img_range is None:
            # 切り取りのための座標情報をメンバ変数に格納
            self.block_bingo_img_range = self.get_img(npoints, wname)
            self.modified_settings = True

        # 画像を切り取り、保存する
        result_img = self.clip(self.original_img, output_size=output_size,
                               l_top=self.block_bingo_img_range["l_top"], l_btm=self.block_bingo_img_range["l_btm"],
                               r_btm=self.block_bingo_img_range["r_btm"], r_top=self.block_bingo_img_range["r_top"])
        result_img_dummy = self.clip(self.original_img_dummy, output_size=output_size,
                                     l_top=self.block_bingo_img_range["l_top"],
                                     l_btm=self.block_bingo_img_range["l_btm"],
                                     r_btm=self.block_bingo_img_range["r_btm"],
                                     r_top=self.block_bingo_img_range["r_top"])
        # 台形補正の結果を表示（何かキーを押すと終了）
        if is_debug:
            cv2.imshow("color", result_img)
            cv2.moveWindow("color", 100, 100)  # ウィンドウを左上に動かす
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        self.block_bingo_img = result_img
        self.block_bingo_img_dummy = result_img_dummy
        return result_img

    def get_circle_coordinates_with_range(self, window_name="Choose circles"):
        if self.block_bingo_circle_coordinates is None:
            img = './img/block_bingo_img_dummy.png'
            cv2.imwrite(img, self.block_bingo_img_dummy)  # 画像保存
            self.move_get_circle_point.window_name = window_name
            self.move_get_circle_point.convert_img(img)
            self.move_get_circle_point.run()
            self.block_bingo_circle_coordinates = self.move_get_circle_point.get_circle_point.named_points
            self.modified_settings = True
        return self.block_bingo_circle_coordinates

    def get_circle_coordinates(self, wname="Choose circles", npoints=24):
        """
        切り取ったブロックビンゴエリアの画像から各種サークルの座標を指定
        """
        # ファイルから座標データを読み込んでいない場合は、各種サークルの座標を設定する
        if self.block_bingo_circle_coordinates is None:
            circle_ptlist = BlockBingoPointList(npoints)
            cv2.namedWindow(wname)
            cv2.setMouseCallback(wname, circle_ptlist.add_point, [wname, self.block_bingo_img_dummy, circle_ptlist])
            cv2.imshow(wname, self.block_bingo_img_dummy)
            cv2.moveWindow(wname, 100, 100)  # ウィンドウを左上に動かす
            cv2.waitKey()
            cv2.destroyAllWindows()
            circle_ptlist.trans()
            self.block_bingo_circle_coordinates = circle_ptlist.named_points
            self.modified_settings = True
        # FIX: ここでは座標を返さずに、座標の指定のみを行うべきかもしれない
        return self.block_bingo_circle_coordinates

    def load_settings(self, file_name="camera_settings.json"):
        """
        切り取るための座標情報や、各種サークルの座標情報をファイルから読み込む
        ファイルを読み込んだ後、以下の関数を呼び出しても領域選択画面は出てこない
            get_circle_coordinates
            get_block_bingo_img
            get_number_img
        """
        # ファイルが存在するかを確かめる
        if not os.path.exists(file_name):
            print("ファイル（{}）が存在しません".format(file_name))
            return

        # ファイル読み込み
        with open(file_name, mode='r') as fp:
            try:
                tmp = json.load(fp)
            except json.decoder.JSONDecodeError:
                print("ファイル（{}）は不正な形式です".format(file_name))
                return

        # ファイルのデータが不十分な場合
        if "number_img_range" not in tmp:
            raise ValueError("データが不十分です（数字カード切り取り用）")
        if "block_bingo_img_range" not in tmp:
            raise ValueError("データが不十分です（ブロックビンゴエリア切り取り用）")
        if "block_bingo_circle_coordinates" not in tmp:
            raise ValueError("データが不十分です（各種サークルの座標）")

        self.number_img_range = tmp["number_img_range"]
        self.block_bingo_img_range = tmp["block_bingo_img_range"]
        self.block_bingo_circle_coordinates = tmp["block_bingo_circle_coordinates"]
        self.loaded_settings_file = True

    def save_settings(self, file_name="camera_settings.json"):
        """
        切り取るための座標情報や、各種サークルの座標情報をファイルへ保存する
        """
        if not self.modified_settings:
            print("[{}.{}] 設定の変更がないため保存は行いません".format(self.__class__.__name__, sys._getframe().f_code.co_name))
            return
        settings = {"number_img_range": self.array_to_list(self.number_img_range),
                    "block_bingo_img_range": self.array_to_list(self.block_bingo_img_range),
                    "block_bingo_circle_coordinates": self.block_bingo_circle_coordinates}
        with open(file_name, mode="w") as fp:
            print(settings)
            json.dump(settings, fp, indent=4)
        print("[{}.{}]設定を保存しました".format(self.__class__.__name__, sys._getframe().f_code.co_name))

    @staticmethod
    def array_to_list(src_dict):
        """
        ptlist.named_listの座標(array)をリストに変換する
        """
        target_dict = {}
        for key in src_dict:
            if type(src_dict[key]) != type(np.array([])):
                continue
            target_dict[key] = src_dict[key].tolist()
        return target_dict

    @staticmethod
    def clip(img, output_size=(420, 297),
             l_top=(-30, 460), l_btm=(190, 620),
             r_top=(400, 450), r_btm=(200, 360)):
        """
        画像から指定された座標の部分を切り抜き、台形補正し保存する。

        Parameters
        ----------
        img: numpy.ndarray
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
    edit_settings = False  # 設定ファイルの内容を上書きするかどうか（設定ファイルが存在しない場合は関係ない）
    if len(sys.argv) != 1:
        if sys.argv[1] == "-e":
            edit_settings = True

    # ラズパイから映像を受信し、保存する
    camera = Camera(
        "https://raw.githubusercontent.com/KatLab-MiyazakiUniv/CameraSystem/master/source/detection_number/imgs/sample.jpg")
    if not edit_settings:
        camera.load_settings()
    # 余白を設定
    camera.capture(padding=100)
    num_img = camera.get_number_img()  # 数字カードの画像
    cv2.imwrite("aaa.png", num_img)

    bingo_img = camera.get_block_bingo_img()  # ブロックビンゴエリアの画像
    cv2.imwrite("bbb.png", bingo_img)

    circle_coordinates = camera.get_circle_coordinates()  # 上記の画像における各種サークルの座標
    camera.save_settings()
