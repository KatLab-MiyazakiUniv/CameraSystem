from block_bingo.BlockBingoCoordinate import CrossCirclesCoordinate, BlockCirclesCoordinate
from block_bingo.BlockBingoCoordinate import Color
import cv2
import numpy as np
import glob

class BlockRecognizer:
    def __init__(self, bonus, is_left):
        """
        Parameters
        ----------
        bonus: int
            ボーナスサークルの番号
        is_left: bool
            コース情報
        """
        self.extractor = BlockExtractor()
        self.bonus = bonus
        self.is_left = is_left

    def create_color_dict(self, files, value):
        color_dict = {}
        for file in files:
            color_dict[file] = value

        return color_dict

    def open_sample_block_files(self):
        white = self.create_color_dict(glob.glob('img/white/*.png'), Color.WHITE)
        black = self.create_color_dict(glob.glob('img/black/*.png'), Color.BLACK)
        blue = self.create_color_dict(glob.glob('img/blue/*.png'), Color.BLUE)
        green = self.create_color_dict(glob.glob('img/green/*.png'), Color.GREEN)
        red = self.create_color_dict(glob.glob('img/red/*.png'), Color.RED)
        yellow = self.create_color_dict(glob.glob('img/yellow/*.png'), Color.YELLOW)

        files = [white, black, blue, green, red, yellow]
        for file in files:
            if len(file) == 0:
                raise ValueError('Cannot open image for calculating histogram')

        return files

    def calculate_histogram(self, img):
        # HSV色空間に変換する
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 色相(Hue)のヒストグラムを求める
        h = cv2.calcHist([img], [0], None, [256], [0, 256])
        # 彩度(Saturation)のヒストグラムを求める
        s = cv2.calcHist([img], [1], None, [256], [0, 256])
        # 明度(Value)のヒストグラムを求める
        v = cv2.calcHist([img], [2], None, [256], [0, 256])
        return (h, s, v)


    def compare_histogram(self, subject, comparer):
        """
        画像とサンプル画像の類似度を計算する
        :param subject: 入力画像のヒストグラム
        :param comparer: サンプル画像のヒストグラム
        :return: 類似度
        """
        # 入力画像とサンプル画像のヒストグラムに関する次元が異なる場合は、例外を送出する
        if len(subject) != len(comparer):
            raise ArithmeticError('Cannot compare histogram! subject size != comparer size')
        # 類似度を初期化しておく
        similarity = 0
        # ヒストグラム比較をする
        for (h1, h2) in zip(subject, comparer):
            similarity += 1 - cv2.compareHist(h1, h2, cv2.HISTCMP_BHATTACHARYYA)

        return similarity / len(subject)


    def detect_color(self, img):
        # 引数のブロック画像のヒストグラムを求める
        subject = self.calculate_histogram(img)
        # ヒストグラムを比較するサンプル画像ファイルのパスを取得する
        paths = self.open_sample_block_files()
        # 類似度を格納する辞書を用意する
        similarity = {}
        for path in paths:
            # 類似度を初期化しておく
            color = list(path.values())[0]
            similarity[color] = 0
            for file in path.keys():
                # サンプル画像ファイルを開く
                sample = cv2.imread(file)
                # サンプル画像のヒストグラムを求める
                comparer = self.calculate_histogram(sample)
                # ブロック画像とサンプル画像を比較する
                similarity[color] += self.compare_histogram(subject, comparer)
            # 計算した類似度を正規化する
            similarity[color] = similarity[color] / len(path.keys())
        # 類似度が最も高い色を返す
        return max(similarity, key=similarity.get)


    def recognize(self, img, circles_coordinates):
        """
        各ブロック・交点サークル上のブロックを認識する

        Parameters
        ----------
        img: numpy.ndarray
            ブロックサークルの部分を切り取った画像

        circles_coordinates: dict
            ブロック・交点サークルの座標

        Returns
        -------
        block_circle: BlockCirclesCoordinate
            ブロックサークルのブロック情報
        cross_circle: CrossCirclesCoordinate
            交点サークル上のブロック情報
        """
        # ブロックサークルの数字を削除する。画像の周辺のノイズも削除する。
        img = self.extractor.remove_circle_number(img)

        # ブロックサークル上のブロックを識別
        color, black = self.recognize_block_circle(img, circles_coordinates)
        block_circle = BlockCirclesCoordinate(self.is_left, self.bonus, color, black)

        # クロスサークル上のブロックを識別
        cross_circle = self.recognize_cross_circle(img, circles_coordinates)

        return block_circle, cross_circle

    def recognize_cross_circle(self, img, circles_coordinates):
        cross_circles = CrossCirclesCoordinate()
        for col in "0123":
            for row in "0123":
                key = 'c' + row + col
                coordinate = (int(col), int(row))
                point = circles_coordinates[key]  # 交点サークルの座標
                crop = self.extractor.trim(img, point)  # 交点サークルの周辺を切り取る
                color = self.detect_color(self.extractor.closing(crop))  # ブロック識別
                cross_circles.set_block_color(coordinate, color)  # 認識結果を辞書に格納
        return cross_circles

    def recognize_block_circle(self, img, circles_coordinates):
        black = None  # 黒ブロックが置かれているブロックサークル番号
        color = None  # カラーブロックが置かれているブロックサークル番号

        # サークル座標のデータ構造からブロックサークルの座標だけ抽出する
        points = self.extract_block_circles_point(circles_coordinates)

        for (idx, point) in enumerate(points):
            crop = self.extractor.trim(img, point)
            # cv2.imshow("crop", crop)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            if Color.BLACK == self.detect_color(self.extractor.closing(crop)):
                black = idx + 1
            elif Color.WHITE != self.detect_color(self.extractor.closing(crop)):
                color = idx + 1

        return (color, black)

    def extract_block_circles_point(self, circles_coordinates):
        points = []
        for key in ['b' + str(i + 1) for i in range(0, 8)]:
            points.append(circles_coordinates[key])
        return points


class BlockExtractor():
    def trim(self, img, point, margin=5):
        """
        画像を指定の座標周辺で切り取る。
        
        Parameters
        ----------
        img : Mat
            画像
        point : tuple
            座標
        margin : int
            指定座標の周囲(px)
        """
        return img[point[1] - margin:point[1] + margin, point[0] - margin:point[0] + margin]

    def hsv_decomposition(self, img):
        """
        HSV分解する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return cv2.split(hsv)

    def binarization(self, img):
        """
        2値化処理する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        (h, s, v) = self.hsv_decomposition(img)
        s = cv2.GaussianBlur(s, (19, 19), 0)
        _, dst = cv2.threshold(s, 57, 255, cv2.THRESH_BINARY)
        return dst

    def closing(self, img):
        """
        クロージング処理する。
        
        Parameters
        ----------
        img : Mat
            画像
        """
        # 8近傍の定義
        kernel = np.ones((9, 9))
        mask = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return mask

    def opening(self, img):
        """
        オープニング処理する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        # 8近傍の定義
        kernel = np.ones((9, 9))
        mask = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return mask

    def remove_circle_number(self, img):
        """
        ブロックサークルの数字を削除する。画像の周辺のノイズも削除する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        # 2値化処理
        mask = self.binarization(img)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # マスク処理をして画像から不要な情報を削除する
        dst = cv2.bitwise_and(img, mask)
        # 不要な情報が黒色になっているので白色に変換する
        return cv2.addWeighted(dst, 1, cv2.bitwise_not(mask), 1, 0)


if __name__ == '__main__':
    pass