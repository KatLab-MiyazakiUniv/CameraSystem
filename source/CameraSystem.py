from detection_number.DetectionNumber import DetectionNumber
from Camera import Camera
from bluetooth.Bluetooth import Bluetooth
from detection_block.BlockRecognizer import BlockRecognizer
from block_bingo.BlackBlockCommands import BlackBlockCommands
from block_bingo.commands import Instructions
from block_bingo.BlockBingoSolver import BlockBingoSolver
import time
import threading
import pprint


class CameraSystem:
    def __init__(self, url="http://raspberrypi.local/?action=stream"):
        self.camera = Camera(url)

        # NOTE: 以前に座標ポチポチしたデータを読み込む（ファイルが存在場合は何もしない）
        #       座標ポチポチをやり直したい場合は、camera.load_settings()を呼び出さなければOK
        self.camera.load_settings()

        self.bt = Bluetooth()
        self.port = "COM4"
        self.is_debug = False

    def start(self):
        """
        カメラシステムクラスのメイン関数
        :return:
        """

        # スレッドを立てて、BT接続を始める。
        connect_thread = threading.Thread(target=self._connect_to_ev3)
        connect_thread.start()
        time.sleep(3)

        while True:
            print("SYS: 本番ですか？")
            print("     y: 本番モード")
            print("     d: デバッグモードで実行")
            is_start = input(">> ")
            if is_start is 'y':
                break
            elif is_start is 'd':
                self.is_debug = True
                break

        is_left = None
        while is_left is None:
            print("SYS: Lコースですか？")
            print("     y: Lコース")
            print("     n: Rコース")
            answer = input(">> ")
            if answer is 'y':
                is_left = True
                break
            elif answer is 'n':
                is_left = False
                break

        # 座標ギメ
        print("\nSYS: 数字カードを切り取ってください")
        self._detection_number_decision_points()

        print("\nSYS: 格子状のエリアを切り取ってください")
        self._detection_block_decide_points()

        print('\nSYS: 開始しています...')
        if not self.is_debug:
            connect_thread.join()
            while True:
                if self.bt.read() == 2:
                    break

        print("\nSYS: 数字カードを認識しています...")
        card_number = self._detection_number()
        print(f"SYS: ボーナスサークルは、{card_number}番サークル")

        print("\nSYS: ブロック運搬経路を計算しています...")
        commands = self._path_planning(card_number, is_left)

        instructions = Instructions()
        print("運搬経路コマンド")
        pprint.pprint([instructions.translate(command)
                       for command in commands])

        print("\nSYS: コマンド送信しています...")
        if not self.is_debug:
            self._send_command(commands)
        else:
            print(commands)

    def _connect_to_ev3(self):
        """
        EV3とBT接続
        """
        print("\nSYS: Connect EV3")
        self.bt.connect(self.port)
        while True:
            write_data = 0
            self.bt.write(write_data, is_print=self.is_debug)
            if self.bt.read() == 1:
                print("SYS: Success! Connected ev3")
                return

            time.sleep(1)  # sec

    def _detection_number_decision_points(self):
        """
        数字カードの切り取りと数字の識別
        :return: 数字カードの数字
        """
        self.camera.capture(padding=100)
        self.camera.get_number_img(is_debug=self.is_debug)
        return

    def _detection_number(self):
        """
        数字カードの切り取りと数字の識別
        :return: 数字カードの数字
        """
        self.camera.capture(padding=100)
        number_card = self.camera.get_number_img(is_debug=self.is_debug)
        detection_number = DetectionNumber(
            img=number_card, model_path="./detection_number/my_model.npz")
        return detection_number.get_detect_number()

    def _path_planning(self, card_number, is_left):
        # ブロックの認識
        (block_circles, cross_circles) = self._detection_block(card_number, is_left)

        # ブロックサークル内の黒ブロック運搬経路を計算する
        (commands, path) = self._black_circles_path(block_circles)
        # ブロックビンゴを成立させるための運搬経路を計算する
        commands += self._block_bingo_path(block_circles, cross_circles, path)

        return commands

    def _detection_block_decide_points(self):
        # 領域、座標指定

        while True:
            try:
                self.camera.get_block_bingo_img(is_debug=self.is_debug)  # 領域指定して画像取得
                self.camera.get_circle_coordinates_with_range()  # 座標ポチポチ
                break
            except TypeError:
                continue
        self.camera.save_settings()  # 座標ポチポチした結果を保存
        return

    def _detection_block(self, card_number, is_left):
        """
        ブロックサークルおよび交点サークルに置かれたブロックを認識する。

        Parameters
        ----------
        card_number : int
            ボーナスサークル番号
        is_left : bool
            Lコースかどうか
        """
        while True:
            # 領域、座標指定
            block_bingo_img = self.camera.get_block_bingo_img(
                is_debug=self.is_debug)     # 領域指定して画像取得
            circles_coordinates = self.camera.get_circle_coordinates_with_range()  # 座標ポチポチ
            self.camera.save_settings()  # 座標ポチポチした結果を保存
            # ブロックの認識器の生成
            recognizer = BlockRecognizer(card_number, is_left)
            # ブロックの認識(戻り値は、BlockCirclesCoordinateとCrossCirclesCoordinateのインスタンス)
            (block_circle, cross_circle) = recognizer.recognize(
                block_bingo_img, circles_coordinates)
            print(f"黒ブロック配置サークルは{block_circle.black_circle}番")
            print(f"カラーブロック配置サークルは{block_circle.color_circle}番")

            if block_circle is not None and cross_circle is not None:
                break
            else:
                self.camera.capture(padding=100)
        return (block_circle, cross_circle)

    def _black_circles_path(self, block_circles):
        """
        ブロックサークル内の黒ブロックを運搬する経路を計算する。

        Parameters
        ----------
        block_circles : BlockCirclesCoordinate
            ブロックサークルの座標
        """
        solver = BlackBlockCommands(
            block_circles.bonus_circle, block_circles.black_circle, block_circles.color_circle)
        commands = list(solver.gen_commands())

        return (commands, solver.reverse_route)

    def _block_bingo_path(self, block_circles, cross_circles, path):
        """
        ブロックビンゴ成立のための運搬経路を計算する。

        Parameters
        ----------
        block_circles : BlockCirclesCoordinate
            ブロックサークルの座標
        cross_circles : CrossCirclesCoordinate
            交点サークルの座標
        path : list
            黒ブロックを運搬するためのブロックサークル間移動の運搬経路
        """
        solver = BlockBingoSolver(block_circles, cross_circles, path)
        return solver.solve()

    def _send_command(self, commands):
        """
        EV3にコマンドを送る

        :param commands: コマンドのリスト
        """
        for c in commands:
            self.bt.write(ord(c))
            time.sleep(0.5)  # sec

        # 終了コードを送信
        self.bt.write(ord('#'))
        print("SYS: command send complete")


if __name__ == '__main__':
    # 本番時はurlを消してね。
    cs = CameraSystem()
    cs.start()
