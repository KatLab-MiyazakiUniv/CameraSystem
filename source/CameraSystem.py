from DetectionNumber import DetectionNumber
from Camera import Camera
from bluetooth.Bluetooth import Bluetooth
from block_bingo.black_block_commands import BlackBlockCommands
import time


class CameraSystem:
    def __init__(self):
        self.camera = Camera()
        
        # NOTE: 以前に座標ポチポチしたデータを読み込む（ファイルが存在場合は何もしない）
        #       座標ポチポチをやり直したい場合は、camera.load_settings()を呼び出さなければOK
        self.camera.load_settings()

        self.bt = Bluetooth()
        self.port = "/dev/cu.MindstormsEV3-SerialPor"
        self.card_number = None

    def _connect_to_ev3(self):
        """
        EV3とBT接続
        """
        self.bt.connect(self.port)
        while True:
            write_data = 0
            self.bt.write(write_data)
            if self.bt.read() == 1:
                return

            time.sleep(1)  # sec

    def _detection_number(self):
        """
        数字カードの切り取りと数字の識別
        :return: 数字カードの数字
        """
        self.camera.capture()
        number_card = self.camera.get_number_img()
        detection_number = DetectionNumber(img=number_card, model_path="./DetectionNumber/my_model.npz")
        return detection_number.get_detect_number()

    def _send_command(self, commands):
        """
        EV3にコマンドを送る

        :param commands: コマンドのリスト
        """
        for c in commands:
            self.bt.write(ord(c))
            time.sleep(1)  # sec

        # 終了コードを送信
        self.bt.write(ord('z'))

    def start(self):
        """
        カメラシステムクラスのメイン関数
        :return:
        """
        print("\nConnect EV3")
        self._connect_to_ev3()
        print("Success! Connected ev3")

        print("\nDetection Number")
        self.card_number = self._detection_number()
        print(f"number is {self.card_number}")

        print("\nDetection Block")
        # 領域、座標指定
        block_bingo_img = self.camera.get_block_bingo_img()     # 領域指定して画像取得
        circles_coordinates = self.camera.get_circle_coordinates()  # 座標ポチポチ
        self.camera.save_settings() # 座標ポチポチした結果を保存
        # TODO ブロックの識別が来る
        bonus = 1 # ボーナスサークル（int）
        black = 2 # 黒ブロックが置かれているブロックサークル（int）
        color = 3 # カラーブロックが置かれているブロックサークル（int）
        balck_block_commands = BlackBlockCommands(bonus, black, color)
        commands_tmp = balck_block_commands.gen_commands()

        # TODO 経路から命令に変換
        commands = list(commands_tmp)

        print("\nSend Command")
        self._send_command(commands)
        # TODO これから


if __name__ == '__main__':
    cs = CameraSystem()
    cs.start()
