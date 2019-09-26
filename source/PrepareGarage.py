from block_bingo.block_circles_path import BlockCirclesCoordinate
from block_bingo.cross_circles_path import CrossCircleSolver
from detection_block.BlockBingo import Color
import unittest


class PrepareGarage():
    def __init__(self, route):
        '''ブロックサークルにある黒ブロックをボーナスサークルに移動した後、ブロックサークル5,8の間に移動する

        Attributes:
            route: (list) ブロックサークル内の黒ブロックをボーナスサークルに運搬する経路
        '''
        self.route = route

        # コマンドの初期化
        # 90度右回転
        self.TURN_RIGHT_90 = 'd'
        # 90度左回転
        self.TURN_LEFT_90 = 'e'
        # 180度回転
        self.TURN_180 = 'f'
        # 右に45度回頭する
        self.TURN_RIGHT_45 = 'q'
        # 左にに45度回頭する
        self.TURN_LEFT_45 = 'r'
        # 右に135度回頭する
        self.TURN_RIGHT_135 = 's'
        # 左に135度回頭する
        self.TURN_LEFT_135 = 't'
        # 黒線上を直進する
        self.MOVE_BLACK = 'u'
        # 黒線上を直進する
        self.MOVE_DIAGONAL = 'v'


    def move_58(self):
        '''ブロックサークルにある黒ブロックをボーナスサークルに移動した後、ブロックサークル5,8の間に移動するためのコマンドを取得する

        Returens:
            (string) ブロックサークル5,8の間に移動するためのコマンド
        '''
        
        commands = ''
        block_circle_coordinate = BlockCirclesCoordinate()

        # 走行体の向きを取得
        robot_direction = self.get_robot_direction()
        # 走行体の現在地からブロックサークル5,8間の中点まで経路を取得する。座標はcross_circles_path.pyを参照
        route_58 = self.get_path()

        # print(robot_direction, route_58)

        # 経路を元にコマンドを作成する
        for i in range(1, len(route_58)):
            # 現在地から見た場合の次の座標の方角
            next_direction = self.get_next_direction(route_58[i-1], route_58[i])
            # 現在の方角から次の座標の方角を向くのに必要な回頭角度を取得
            rotation_angel = self.get_rotation_angle(robot_direction, next_direction)
            
            # 回頭角度に応じたコマンドを追加する
            if rotation_angel != 0:
                commands += self.get_rotation_command(rotation_angel)
            
            if next_direction in [0,2,4,6]:
                # 黒線上を直進するコマンドを追加する
                commands += self.MOVE_BLACK
            else:
                # 斜め移動
                commands += self.MOVE_DIAGONAL

            # 走行体の向きを更新
            robot_direction = next_direction

        # (4,5)についた後、走行体がガレージの方向(2)を向くようにする
        rotation_angel = self.get_rotation_angle(robot_direction, 2)
        if rotation_angel != 0:
            commands += self.get_rotation_command(rotation_angel)

        return commands


    def get_path(self):
        '''現在地からブロックサークル5,8間の中点までの経路を求める
        Returns:
            (list) 座標のリスト。座標はcross_circles_path.pyで定義した座標
        '''
        # 交点サークルにあるブロックの座標と色。ここでは何でも良い。
        block_coordinate = {(0,0): Color.BLUE, (0,4): Color.BLACK, (2,2): Color.GREEN, (2,6): Color.RED, (4,0): Color.RED, (4,4): Color.YELLOW, (6,2): Color.BLUE, (6,6): Color.GREEN}
        robot_direction = self.get_robot_direction()
        cross_circle_solver = CrossCircleSolver(robot_direction, block_coordinate)
        # 最初に走行体がいる場所の座標を求める
        start = self.get_start_coor(self.route[-1], self.route[-2])
        # 最初に走行体がいる座標からブロックサークル5,8間の中点までの経路を計算する
        route_58 = cross_circle_solver.aster(start, (4,5))
        return route_58


    def get_robot_direction(self):
        '''走行体が向いている方角を取得する
        Returns:
            (int) 走行体が向いている方角。上向きを0とし、時計回りに45度=1、90度=2、135度=3・・・315度=7とする
            0
           7 1
          6   2
           5 3
            4
              
        '''
        # 最後に到達したブロックサークルの座標 = ボーナスサークルの座標
        # block_circle_path.pyで定義されている座標
        last = self.route[-1]
        # 最後から2番目に到達したブロックサークルの座標
        # block_circle_path.pyで定義されている座標
        second = self.route[-2]
        if last == (0, 0):
            if second == (0, 1):
                # 1,2
                return 6
            else:
                # 1,4
                return 0
        elif last == (0, 1):
            if second == (0, 0):
                # 2,1
                return 2
            else:
                # 2,3
                return 6
        elif last == (0, 2):
            if second == (0, 1):
                # 3,2
                return 2
            else:
                # 3,5
                return 0
        elif last == (1, 0):
            if second == (0,0):
                # 4,1
                return 4
            else:
                # 4,6
                return 0
        elif last == (1, 2):
            if second == (0, 2):
                # 5,3
                return 4
            else:
                # 5,8
                return 0
        elif last == (2, 0):
            if second == (1, 0):
                # 6,4
                return 4
            else:
                # 6,7
                return 6
        elif last == (2, 1):
            if second == (2, 0):
                # 7,6
                return 2
            else:
                # 7,8
                return 6
        elif last == (2, 2):
            if second == (1, 2):
                # 8,5
                return 4
            else:
                # 8,7
                return 2


    def get_next_direction(self, current, next):
        dx = next[1] - current[1]
        dy = next[0] - current[0]
        if dx == 0 and dy < 0:
            return 0
        elif dx > 0 and dy < 0:
            return 1
        elif dx > 0 and dy == 0:
            return 2
        elif dx > 0 and dy > 0:
            return 3
        elif dx == 0 and dy > 0:
            return 4
        elif dx < 0 and dy > 0:
            return 5
        elif dx < 0 and dy == 0:
            return 6
        elif dx < 0 and dy < 0:
            return 7
        else:
            raise ValueError('Same coordinate.')


    def get_rotation_angle(self, robot_direction, next_direction):
        '''走行体の方角と次の座標がある方角から、回頭する角度を求める
        Args:
            robot_direction: (int) 走行体が向いている方角
            next_direction: (int) 現在の座標から見て次の座標がある方角

        Returns:
            (int) 回頭する角度。0,45,90,135,180,-180,-135,-90,-45のいずれか
        '''
        angle = 0

        # 時計回り、反時計回りで回頭角度が小さくなる方を選ぶように色々している
        if next_direction - robot_direction < -4:
            angle = 8 + (next_direction - robot_direction)
        elif next_direction - robot_direction > 4:
            angle = (next_direction - robot_direction) - 8
        else:
            angle = next_direction - robot_direction

        return angle * 45


    def get_rotation_command(self, rotation_angel):
        if rotation_angel == 45:
            return self.TURN_RIGHT_45
        elif rotation_angel == 90:
            return self.TURN_RIGHT_90
        elif rotation_angel == 135:
            return self.TURN_RIGHT_135
        elif rotation_angel == -45:
            return self.TURN_LEFT_45
        elif rotation_angel == -90:
            return self.TURN_LEFT_90
        elif rotation_angel == -135:
            return self.TURN_LEFT_135
        elif abs(rotation_angel) == 180:
            return self.TURN_180


    def get_start_coor(self, last, second):
        '''走行体が最初にいる場所の座標を求める
        Args:
            last: (tuple) 最後のブロックサークル(ボーナスサークル)の座標。block_circles_path.pyで定義した座標。
            second: (tuple) 最後から2番目のブロックサークルの座標。block_circles_path.pyで定義した座標。
        Returns:
            (tuple) 走行体が最初にいる場所の座標。cross_circles_path.pyで定義した座標。
        '''
        if last == (0, 0) and second == (0, 1) or last == (0, 1) and second == (0, 0):
            # 1,2
            return (1, 2)
        elif last == (0, 1) and second == (0, 2) or last == (0, 2) and second == (0, 1):
            # 2,3
            return (1, 4)
        elif last == (0, 0) and second == (1, 0) or last == (1, 0) and second == (0, 0):
            # 1,4
            return (2,1)
        elif last == (0, 2) and second == (1, 2) or last == (1, 2) and second == (0, 2):
            # 3,4
            return (2,5)
        elif last == (1, 0) and second == (2, 0) or last == (2, 0) and second == (1, 0):
            # 4,6
            return (4, 1)
        elif last == (1, 2) and second == (2, 2) or last == (2, 2) and second == (1, 2):
            # 5,8
            return (4,5)
        elif last == (2, 0) and second == (2, 1) or last == (2, 1) and second == (2, 0):
            # 6,7
            return (5,2)
        elif last == (2, 1) and second == (2, 2) or last == (2, 2) and second == (2, 1):
            # 7,8
            return (5, 4)


class PrepareGarageTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PrepareGarageTest, self).__init__(*args, **kwargs)
        self.route_all = [
            [(0, 0), (0, 1)], [(0, 1), (0, 0)],
            [(0, 1), (0, 2)], [(0, 2), (0, 1)],
            [(0, 0), (1, 0)], [(1, 0), (0, 0)],
            [(0, 2), (1, 2)], [(1, 2), (0, 2)],
            [(1, 0), (2, 0)], [(2, 0), (1, 0)],
            [(1, 2), (2, 2)], [(2, 2), (1, 2)],
            [(2, 0), (2, 1)], [(2, 1), (2, 0)],
            [(2, 1), (2, 2)], [(2, 2), (2, 1)],
        ]



    def test_get_path(self):
        '''
        get_path()のテストコード
        確認事項
            1. 経路の最後が(5,4)である
        '''
        # ブロックサークル内の黒ブロックをボーナスサークルへ運搬する経路。最後の2座標のみ。全パターン。

        for route in self.route_all:
            prepare_garage = PrepareGarage(route)
            route_58 = prepare_garage.get_path()
            self.assertEqual(route_58[-1], (4, 5))
            

    def test_get_robot_direction(self):
        '''
        get_robot_direction()のテストコード
        '''
        expect_direction = [2,6,2,6,4,0,4,0,4,0,4,0,2,6,2,6]
        for i,route in enumerate(self.route_all):
            prepare_garage = PrepareGarage(route)
            robot_direction = prepare_garage.get_robot_direction()
            self.assertEqual(robot_direction, expect_direction[i])


    def test_get_next_direction(self):
        '''
        get_next_direction()のテストコード
        '''
        test_case = [
            {'current': (2, 4), 'next': (1, 4), 'expect': 0},
            {'current': (2, 4), 'next': (2, 5), 'expect': 2},
            {'current': (2, 4), 'next': (3, 4), 'expect': 4},
            {'current': (2, 4), 'next': (2, 3), 'expect': 6},
            {'current': (2, 3), 'next': (1, 4), 'expect': 1},
            {'current': (2, 3), 'next': (3, 4), 'expect': 3},
            {'current': (2, 3), 'next': (3, 2), 'expect': 5},
            {'current': (2, 3), 'next': (1, 2), 'expect': 7},
        ]
        
        prepare_garage = PrepareGarage(self.route_all[0])
        for tc in test_case:
            next_direction = prepare_garage.get_next_direction(tc['current'], tc['next'])
            self.assertEqual(next_direction, tc['expect'])


    def test_get_rotation_angle(self):
        '''
        get_rotation_angle()のテストコード
        '''
        expect = [0,1,2,3,4,-3,-2,-1,-1,0,1,2,3,4,-3,-2,-2,-1,0,1,2,3,4,-3,-3,-2,-1,0,1,2,3,4,-4,-3,-2,-1,0,1,2,3,3,-4,-3,-2,-1,0,1,2,2,3,-4,-3,-2,-1,0,1,1,2,3,-4,-3,-2,-1,0]

        prepare_garage = PrepareGarage(self.route_all[0])
        cnt = 0
        for robot_direction in range(8):
            for next_direction in range(8):
                angle = prepare_garage.get_rotation_angle(robot_direction, next_direction)
                self.assertEqual(angle, expect[cnt] * 45)
                cnt += 1


if __name__ == '__main__':
    route_all = [
        [(0, 0), (0, 1)],
        [(0, 1), (0, 0)],

        [(0, 1), (0, 2)],
        [(0, 2), (0, 1)],

        [(0, 0), (1, 0)],
        [(1, 0), (0, 0)],

        [(0, 2), (1, 2)],
        [(1, 2), (0, 2)],

        [(1, 0), (2, 0)],
        [(2, 0), (1, 0)],

        [(1, 2), (2, 2)],
        [(2, 2), (1, 2)],

        [(2, 0), (2, 1)],
        [(2, 1), (2, 0)],

        [(2, 1), (2, 2)],
        [(2, 2), (2, 1)],
    ]
    for route in route_all:
        prepare_garage = PrepareGarage(route)
        print(route)
        print(prepare_garage.get_path())
        print(f'{prepare_garage.move_58()}\n')






