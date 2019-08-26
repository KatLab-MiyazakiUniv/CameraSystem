"""
@file: clipping_number.py
@author: Takahiro55555
@brief: カメラシステムから取得した画像から、数字カードの部分を切り抜き、台形補正する。
"""

import datetime
import sys

import cv2
import numpy as np

from get_point import get_point, PointList

def captureImage(url="http://raspberrypi.local/?action=stream", padding=0):
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
    # VideoCaptureのインスタンスを作成する。
    cap = cv2.VideoCapture(url) # カメラシステムを使う場合
    #cap = cv2.VideoCapture(DEVICE_ID) # このpythonスクリプトを実行するPCのカメラを使う場合コメントアウトして下さい
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

    # 画像をキャプチャ
    ret, img = cap.read()

    # 余白を設定する
    tmp = img[:, :]
    height, width = img.shape[:2]
    new_img = cv2.resize(np.full((1, 1, 3), fill_value=255, dtype=np.uint8), dsize=(width+padding*2, height+padding*2))
    new_img[padding:height+padding, padding:width+padding] = tmp

    # キャプチャ終了
    cap.release()

    # ファイル名を返す
    return new_img

def clipNumber(src_img, output_size=[420, 297],
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
     https\://note.nkmk.me/python-opencv-warp-affine-perspective/
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
    url = "http://raspberrypi.local/?action=stream"
    img = captureImage(url=url, padding=100)

    wname = "MouseEvent"
    cv2.namedWindow(wname)
    npoints = 4
    ptlist = PointList(npoints)
    cv2.setMouseCallback(wname, get_point, [wname, img, ptlist])
    cv2.imshow(wname, img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    ptlist.trans()

    # 画像を切り取り、保存する
    result_img = clipNumber(img, l_top=ptlist.named_points["l_top"], l_btm=ptlist.named_points["l_btm"], 
               r_btm=ptlist.named_points["r_btm"], r_top=ptlist.named_points["r_top"])

    # 台形補正の結果を表示（何かキーを押すと終了）
    cv2.imshow("color", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
