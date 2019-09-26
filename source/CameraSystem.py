from DetectionNumber import DetectionNumber
from Camera import Camera
from bluetooth.Bluetooth import Bluetooth
from detection_block.BlockRecognizer import BlockRecognizer
from block_bingo.black_block_commands import BlackBlockCommands
import time
import threading


class CameraSystem:
    def __init__(self):
        self.camera = Camera()
        
        # NOTE: 以前に座標ポチポチしたデータを読み込む（ファイルが存在場合は何もしない）
        #       座標ポチポチをやり直したい場合は、camera.load_settings()を呼び出さなければOK
        self.camera.load_settings()

        self.bt = Bluetooth()
        self.port = "/dev/cu.MindstormsEV3-SerialPor"
        self.card_number = None
        self.is_debug = False

    def _connect_to_ev3(self):
        """
        EV3とBT接続
        """
        print("\nSYS: Connect EV3")
        self.bt.connect(self.port)
        while True:
            write_data = 0
            self.bt.write(write_data, is_print=False)
            if self.bt.read() == 1:
                print("SYS: Success! Connected ev3")
                return

            time.sleep(1)  # sec

    def _detection_number(self):
        """
        数字カードの切り取りと数字の識別
        :return: 数字カードの数字
        """
        self.camera.capture(padding=100)
        number_card = self.camera.get_number_img(is_debug=self.is_debug)
        detection_number = DetectionNumber(img=number_card, model_path="./detection_number/my_model.npz")
        return detection_number.get_detect_number()

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

    def _detection_block(self):
        while True:
            # 領域、座標指定
            block_bingo_img = self.camera.get_block_bingo_img(is_debug=self.is_debug)     # 領域指定して画像取得
            circles_coordinates = self.camera.get_circle_coordinates()  # 座標ポチポチ
            self.camera.save_settings()  # 座標ポチポチした結果を保存
            # ブロックの識別が来る
            recognizer = BlockRecognizer()
            black_block_place, color_block_place = recognizer.recognize_block_circle(block_bingo_img, circles_coordinates)
            print(black_block_place, color_block_place)

            if black_block_place is not None and color_block_place is not None:
                break
            else:
                self.camera.capture()

        # ボーナスサークル（int）
        # 黒ブロックが置かれているブロックサークル（int）
        # カラーブロックが置かれているブロックサークル（int）
        black_block_commands = BlackBlockCommands(self.card_number, black_block_place, color_block_place)
        commands_tmp = black_block_commands.gen_commands()
        print(black_block_commands.route)
        print(commands_tmp)
        # 経路から命令に変換
        return list(commands_tmp)

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

        if not self.is_debug:
            print('\nSYS: Wait start...')
            connect_thread.join()
            while True:
                if self.bt.read() == 2:
                    break

        print("\nSYS: Detection Number")
        self.card_number = self._detection_number()
        print(f"SYS: number is {self.card_number}")

        print("\nSYS: Detection Block")
        commands = self._detection_block()

        if self.is_debug:
            connect_thread.join()

        print("\nSYS: Send Command")
        self._send_command(commands)
        # TODO これから


if __name__ == '__main__':
    cs = CameraSystem()
    cs.start()
