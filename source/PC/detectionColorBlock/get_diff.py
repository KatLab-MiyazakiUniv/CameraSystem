# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../numberDetection')

from clipping_number import clipNumber, captureImage

data_directory = "data/original"


def show_match(file_a, file_b):
    # 画像の読み込み
    imgA = cv2.imread(file_a)
    imgB = cv2.imread(file_b)

    # グレー変換
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # 画像サイズの取得
    height, width = grayA.shape
    # 部分画像を作って、マッチングさせる
    result_window = np.zeros((height, width), dtype=imgA.dtype)
    for start_y in range(0, height - 100, 50):
        for start_x in range(0, width - 100, 50):
            window = grayA[start_y:start_y + 100, start_x:start_x + 100]
            match = cv2.matchTemplate(grayB, window, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(match)
            matched_window = grayB[max_loc[1]:max_loc[1] + 100, max_loc[0]:max_loc[0] + 100]
            result = cv2.absdiff(window, matched_window)
            result_window[start_y:start_y + 100, start_x:start_x + 100] = result

    plt.imshow(result_window)


def match(file_a, file_b):
    # 画像の読み込み
    imgA = cv2.imread(file_a)
    imgB = cv2.imread(file_b)

    # グレー変換
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # 画像サイズの取得
    height, width = grayA.shape
    # 部分画像を作って、マッチングさせる
    result_window = np.zeros((height, width), dtype=imgA.dtype)
    for start_y in range(0, height - 100, 50):
        for start_x in range(0, width - 100, 50):
            window = grayA[start_y:start_y + 100, start_x:start_x + 100]
            match = cv2.matchTemplate(grayB, window, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(match)
            matched_window = grayB[max_loc[1]:max_loc[1] + 100, max_loc[0]:max_loc[0] + 100]
            result = cv2.absdiff(window, matched_window)
            result_window[start_y:start_y + 100, start_x:start_x + 100] = result

    # マッチングした結果できた差分画像の輪郭を抽出し、四角で囲む
    _, result_window_bin = cv2.threshold(result_window, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(result_window_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imgC = imgA.copy()
    for contour in contours:
        print(contour)
        min = np.nanmin(contour, 0)
        max = np.nanmax(contour, 0)
        loc1 = (min[0][0], min[0][1])
        loc2 = (max[0][0], max[0][1])
        cv2.rectangle(imgC, loc1, loc2, 255, 2)

    # 画像表示する
    plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)), plt.title('A'), plt.xticks([]), plt.yticks(
        [])
    plt.subplot(1, 3, 2), plt.imshow(cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB)), plt.title('B'), plt.xticks([]), plt.yticks(
        [])
    plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)), plt.title('Answer'), plt.xticks(
        []), plt.yticks([])
    plt.show()


def test(file_a, file_b):
    # 画像の読み込み
    img_src1 = cv2.imread(file_a, 1)
    img_src2 = cv2.imread(file_b, 1)

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(img_src1)
    fgmask = fgbg.apply(img_src2)

    # 表示
    cv2.imshow('frame', fgmask)

    # 検出画像
    bg_diff_path = './diff.jpg'
    cv2.imwrite(bg_diff_path, fgmask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cripping_field(file):
    clipNumber(file, "clip_field.png", output_size=[640, 640],
               l_top=[194, 279], l_btm=[1145, 625],
               r_top=[1278, 149], r_btm=[675, 65])


if __name__ == '__main__':
    #data_directory = "./"
    src_name = captureImage(target_dir="./", url="http://raspberrypi.local/?action=stream")
    cripping_field(src_name)
    none_fig = os.path.join(data_directory, "clip_field_none_block.png")
    fix_fig = os.path.join(data_directory, "clip_field_has_block.png")
    test(none_fig, fix_fig)
    #cripping_field(fix_fig)