"""
@file: clipping_number.py
@author: Takahiro55555
@brief: カメラシステムから取得した画像から、数字カードの部分を切り抜き、台形補正する。
"""

import datetime

import cv2
import numpy as np


def captureImage(target_name=None, target_dir="./", url="http://192.168.11.25/?action=stream"):
    """
    URLから流れてくる映像をキャプチャし、静止画として保存する

    Parameters
    ----------
    target_name: str
        キャプチャした静止画のファイル名。デフォルトでは時刻によってファイル名が決まる。

    target_dir: str
        キャプチャした静止画を保存するためのディレクトリ。デフォルトでは実行時のカレントディレクトリ。

    url: str
         映像配信URL

    Returns
    -------
    target_name: str
        キャプチャした静止画のファイル名
    """
    # VideoCaptureのインスタンスを作成する。
    cap = cv2.VideoCapture(url) # カメラシステムを使う場合
    #cap = cv2.VideoCapture(DEVICE_ID) # このpythonスクリプトを実行するPCのカメラを使う場合コメントアウトして下さい

    # カメラFPSを30FPSに設定
    cap.set(cv2.CAP_PROP_FPS, 30)

    # カメラ画像の横幅を1280に設定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    # カメラ画像の縦幅を720に設定
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # ピクセル配列をゼロ初期化
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    if cap.isOpened():
        # 画像をキャプチャ
        ret, img = cap.read()
        
        # 出力ファイル名を設定
        if target_name == None:
            target_name = 'snapshot_{0:%Y%m%d_%H%M%S}.jpg'.format(datetime.datetime.now())

        # 画像をJPEGファイルへ保存
        cv2.imwrite(target_dir + target_name, img)

    # キャプチャ終了
    cap.release()

    # ファイル名を返す
    return target_name


def clipNumber(src_path, target_name, target_dir="./", output_size=[420, 297],
               l_top=[-30, 460], l_btm=[190, 620],
               r_top=[400, 450], r_btm=[200, 360]):
    """
    画像から指定された座標の部分を切り抜き、台形補正し保存する。

    Parameters
    ----------
    src_path: str
        対象のファイル名
    
    target_name: str
        出力するファイル名

    target_dir: str
        出力先のディレクトリ名

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
        None

    Referrenced
    -----------
     https\://note.nkmk.me/python-opencv-warp-affine-perspective/
    """
    # ファイル読込み
    img = cv2.imread(src_path)
    
    # 出力サイズを引数から取得
    h, w = output_size

    src_pts = np.array([[0, 0], [0, h], [w, h], [w, 0]], dtype=np.float32)
    # 座標指定の順序[[左上], [左下], [右上], [右下]]
    dst_pts = np.array([l_top, l_btm, r_top, r_btm], dtype=np.float32)
    mat = cv2.getPerspectiveTransform(dst_pts, src_pts)
    
    # borderValueで色(R, G, B)256段階を指定すると、画像でない部分を指定した色で埋めてくれる
    # ２値化することを考慮し、画像でない部分は白色に設定
    perspective_img = cv2.warpPerspective(img, mat, (w, h), borderValue=(255, 255, 255))

    # 画像の保存
    cv2.imwrite(target_dir + target_name, perspective_img)


if __name__ == '__main__':
    imgs_dir = "imgs/" # 画像を保管するディレクトリ

    # ラズパイから映像を受信し、保存する
    src_name = captureImage(target_dir=imgs_dir)
    target_name = "_result_" + src_name # 切り取った画像の出力ファイル名
    
    # 画像を切り取り、保存する
    clipNumber(src_path=imgs_dir + src_name, target_name=target_name, target_dir=imgs_dir)

    # 確認のために画像を表示しているだけ（何かキーを押すと終了）
    img = cv2.imread(imgs_dir + src_name)
    cv2.imshow("color", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 台形補正の結果を表示（何かキーを押すと終了）
    img = cv2.imread(imgs_dir + target_name)
    cv2.imshow("color", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
