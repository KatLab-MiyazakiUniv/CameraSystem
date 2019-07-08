"""
@file: create_data.py
@author: korosuke613
@brief: 画像を大量に生成する
"""

import cv2
import numpy as np


def load_original():
    # 画像の読込(numpy.ndarrayで読み込まれる)
    image = cv2.imread('original/1.jpg')
    return image


def change_brightness(image):
    # 乱数生成
    rand_num = np.random.rand() / 2
    print(rand_num)
    # γ値の定義(1より小さいと暗く、1より大きいと明るくなる)
    gamma = 1 - rand_num

    # ルックアップテーブルの生成
    look_up_table = np.zeros((256, 1), dtype=np.uint8)
    for i in range(256):
        look_up_table[i][0] = 255 * (float(i)/255) ** (1.0 / gamma)

    # γ変換後の画像取得
    image_gamma = cv2.LUT(image, look_up_table)
    return image_gamma


def save_image(image, name):
    cv2.imwrite(name + ".jpg", image)


def print_image(image):
    # 画像を表示
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    for i in range(100):
        image = load_original()
        created_image = change_brightness(image)
        name = "1_" + str(i)
        save_image(created_image, name)
