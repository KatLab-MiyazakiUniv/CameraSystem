"""
    @file   commands.py
    @author T.Miyaji
    @brief  ブロックビンゴ攻略のための運搬経路を走行体動作コマンドに変換する。
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

class Instructions():
    ENTER_BINGO_AREA_L4 = 'a'
    ENTER_BINGO_AREA_L6 = 'b'
    STRAIGHT = 'c'
    SPIN_RIGHT = 'd'
    SPIN_LEFT = 'e'
    SPIN180 = 'f'
    PUT = 'g'
    STRAIGHT_DETOUR_RIGHT = 'h'
    STRAIGHT_DETOUR_LEFT = 'i'
    TURN_RIGHT90_EXIST_BLOCK = 'j'
    TURN_RIGHT90_UNEXIST_BLOCK = 'k'
    TURN_LEFT90_EXIST_BLOCK = 'l'
    TURN_LEFT90_UNEXIST_BLOCK = 'm'
    TURN180 = 'n'

    MOVE_NODE = 'u'
    
    QUICK_PUT_R = 'y'
    QUICK_PUT_L = 'z'


    def translate(self, instruction):
        ja = {  Instructions.ENTER_BINGO_AREA_L4: '4番サークルに進入',
                Instructions.ENTER_BINGO_AREA_L6: '6番サークルに進入',
                Instructions.STRAIGHT: 'ブロックサークル間を直進',
                Instructions.SPIN_RIGHT: '右に90°回頭する',
                Instructions.SPIN_LEFT: '左に90°回頭する',
                Instructions.SPIN180: '180°回頭する',
                Instructions.PUT: 'ブロックを黒線の中点から設置',
                Instructions.STRAIGHT_DETOUR_RIGHT: 'ブロックを右方向に迂回しながら直進',
                Instructions.STRAIGHT_DETOUR_LEFT: 'ブロックを左方向に迂回しながら直進',
                Instructions.TURN_RIGHT90_EXIST_BLOCK: '右方向に旋回（ブロックあり）',
                Instructions.TURN_LEFT90_EXIST_BLOCK: '左方向に旋回（ブロックあり）',
                Instructions.TURN_RIGHT90_UNEXIST_BLOCK: '右方向に旋回（ブロックなし）',
                Instructions.TURN_LEFT90_UNEXIST_BLOCK: '左方向に旋回（ブロックなし）'   ,   
                Instructions.TURN180: '180°回頭して直進（ブロックなし）',
                Instructions.MOVE_NODE: '交点サークルから黒線の中点まで直進',

                Instructions.QUICK_PUT_R: '交点サークルから右方向に旋回してブロック設置',
                Instructions.QUICK_PUT_L: '交点サークルから左方向に旋回してブロック設置'
        }
        return ja[instruction]


class Commands():
    def __init__(self, block_circles, cross_circles):
        """
        ブロックサークルおよび交点サークルの情報を登録する。

        Parameters
        ----------
        block_circles : BlockCirclesCoordinate
            ブロックサークルの座標
        cross_circles : CrossCirclesCoordinate
            交点サークルの座標
        """
        self.block_circles = block_circles
        self.cross_circles = cross_circles

        # コマンドのリスト
        self.commands = []
    
    
    def convert(self, direction, path):
        """
        運搬経路をコマンド変換する。

        Parameters
        ----------
        direction : int
            方角: 上向きを0とし、時計回りに45度=1、90度=2、135度=3・・・315度=7とする
            0
          6   2
            4
        path : list
            運搬経路（移動する座標のリスト）
        """
        # 運搬経路から始点と終点を抽出する
        for (src, dst) in zip(path[:-1], path[1:]):
            # 始点にブロックが置いてあるか調べる。
            has_block = src in self.cross_circles.open
            # srcの前に運搬経路が存在しないことを確認する。
            if src == path[0]:
                direction = self.spin(src, dst, direction, has_block)
            direction = self.straight(src, dst, direction, has_block)
        return direction
    

    def get(self):
        return self.commands


    def get_next_direction(self, src, dst):
        """
        始点から終点までの移動したときの走行体の向きを取得する。
        方角: 上向きを0とし、時計回りに45度=1、90度=2、135度=3・・・315度=7とする
            0
          6   2
            4
        Parameters
        ----------
        src : tuple
            始点の座標
        dst : tuple
            終点の座標
        """
        subtraction = (dst[0]-src[0], dst[1]-src[1])

        if subtraction == (-1, 0) or subtraction == (-0.5, 0):
            return 0    # 北向き
        if subtraction == (0, 1) or subtraction == (0, 0.5):
            return 2    # 東向き
        if subtraction == (1, 0) or subtraction == (0.5, 0):
            return 4    # 南向き
        if subtraction == (0, -1) or subtraction == (0, -0.5):
            return 6    # 西向き
        raise ValueError('could not calculate direction')


    def spin(self, src, dst, direction, has_block):
        """
        回頭コマンドへ変換する。
        """
        next_direction = self.get_next_direction(src, dst)
        
        # 次の方向と現在の方向を引き算する。
        sub = next_direction - direction
        if sub == 0:
            return direction
        if sub == 2 or sub == -6:
            self.commands.append(Instructions.SPIN_RIGHT)
            return next_direction
        if sub == 4 or sub == -4:
            self.commands.append(Instructions.SPIN180)
            return next_direction
        if sub == -2 or sub == 6:
            self.commands.append(Instructions.SPIN_LEFT)
            return next_direction
        
        raise ArithmeticError('cannot convert path to SPIN command!')
    

    def straight(self, src, dst, direction, has_block):
        """
        交点サークル間の直進コマンドへ変換する。
        """
        # srcからdstの向きとdirectionが同じ向きであることを確認する
        if direction != self.get_next_direction(src, dst):
            # 向きが異なる場合、旋回コマンドに変換する
            return self.turn(src, dst, direction, has_block)
        if has_block != False:
            # 始点にブロックがある場合、ブロックありの直進に変換する
            return self.straight_detour(src, dst, direction, has_block)
        self.commands.append(Instructions.MOVE_NODE)
        return direction


    def turn(self, src, dst, direction, has_block):
        """
        旋回コマンドへ変換する。
        """
        # 始点にブロックがないことを確認する
        if has_block != False:
            # 始点にブロックがある場合、ブロックありの旋回に変換する
            return self.turn_detour(src, dst, direction, has_block)
        # srcとdstから走行体が次に向く方向を求める
        next_direction = self.get_next_direction(src, dst)
        sub = next_direction - direction

        if sub == 2 or sub == -6:
            self.commands[-1] = Instructions.TURN_RIGHT90_UNEXIST_BLOCK
            return next_direction
        if sub == 4 or sub == -4:
            # 180°回頭する必要がある場合は、180°回頭コマンドへ変換する
            self.turn180(src, dst, direction, has_block)
        if sub == -2 or sub == 6:
            self.commands[-1] = Instructions.TURN_LEFT90_UNEXIST_BLOCK
            return next_direction
        raise ArithmeticError('cannot convert path to TURN command!')


    def turn180(self, src, dst, direction, has_block):
        """
        180°回頭して直進するコマンドへ変換する。
        """
        # 始点にブロックがないことを確認する
        if has_block != False:
            # 始点にブロックがある場合、ブロックありの180°回頭して直進するコマンドへ変換する
            self.turn180_detour(src, dst, direction, has_block)
        self.commands.append(Instructions.TURN180)

        return self.get_next_direction(src, dst)
    

    def straight_detour(self, src, dst, direction, has_block):
        """
        ブロックありの直進コマンドへ変換する。
        """
        # 始点が格子状エリアの右端または下端にない場合
        if 0 <= src[0] < 3 and 0 <= src[1] < 3:
            # 走行体が上向きまたは右方向に進む場合
            if dst[0] < src[0] or src[1] < dst[1]:
                self.commands[-1] = Instructions.STRAIGHT_DETOUR_RIGHT
            # 走行体が下向きまたは左方向に進む場合
            else:
                self.commands[-1] = Instructions.STRAIGHT_DETOUR_LEFT
            return direction
        
        # 始点が格子状エリアの右端または下端にある場合
        if dst[0] < src[0] or src[1] < dst[1]:
            self.commands[-1] = Instructions.STRAIGHT_DETOUR_LEFT
        else:
            self.commands[-1] = Instructions.STRAIGHT_DETOUR_RIGHT
        
        return direction
    

    def turn_detour(self, src, dst, direction, has_block):
        """
        ブロックありの旋回コマンドへ変換する。
        """
        # srcとdstから走行体が次に向く方向を求める
        next_direction = self.get_next_direction(src, dst)
        sub = next_direction - direction

        if sub == 2 or sub == -6:
            self.commands[-1] = Instructions.TURN_RIGHT90_EXIST_BLOCK
            return next_direction
        if sub == 4 or sub == -4:
            # 180°回頭する必要がある場合は、180°回頭コマンドへ変換する
            self.turn180(src, dst, direction, has_block)
        if sub == -2 or sub == 6:
            self.commands[-1] = Instructions.TURN_LEFT90_EXIST_BLOCK
            return next_direction
        raise ArithmeticError('cannot convert path to TURN command!')


    def turn180_detour(self, src, dst, direction, has_block):
        """
        ブロックありの180°回頭して直進するコマンドへ変換する。
        """
        # コマンドリストの先頭を取り出す
        top = self.commands.pop(-1)
        # 180°回頭するコマンドをコマンドリストへ追加し、directionを更新する
        self.commands.append(Instructions.SPIN180)
        direction = self.get_next_direction(src, dst)
        # 取り出したコマンドリストの先頭をコマンドリストへ追加する
        self.commands.append(top)
        # ブロックありの直進コマンドへ変換する
        return self.straight_detour(src, dst, direction, True)
    

    def put(self, src, dst, direction, has_block=False):
        """
        ブロックをブロックサークルに設置する動作をコマンドへ変換する。
        """
        # 終点にブロックサークルがあることを確認する
        if dst not in self.block_circles.block_circles.values():
            raise ValueError('cannot find block circle corresponding to dst!')
        # 始点が交点サークルにあるとき
        if src[0] in [0, 1, 2, 3] and src[1] in [0, 1, 2, 3]:
            return self.put_block_from_cross_circle(src, dst, direction, has_block)
        # 始点が黒線の中点にあるとき
        return self.put_block_from_midpoint(src, dst, direction, has_block)


    def put_block_from_midpoint(self, src, dst, direction, has_block):
        """
        黒線の中点からブロックを設置する動作をコマンドに変換する。
        """
        # 黒線の中点の座標からブロックサークルの座標を引く
        sub = (src[0] - dst[0], src[1] - dst[1])

        if sub == (0,0.5): # ブロックサークルの上部の中点
            # 走行体が南に向くように回頭コマンドの変換をする
            direction = self.spin(src, (src[0]+1, src[1]), direction, has_block)
        if sub == (0.5,1): # ブロックサークルの左の中点
            # 走行体が西に向くように回頭コマンドの変換をする
            direction = self.spin(src, (src[0], src[1]-1), direction, has_block)
        if sub == (1,0.5): # ブロックサークルの下部の中点
            # 走行体が北に向くように回頭コマンドの変換をする
            direction = self.spin(src, (src[0]-1, src[1]), direction, has_block)
        if sub == (0.5,0): # ブロックサークルの右の中点
            # 走行体が東に向くように回頭コマンドの変換をする
            direction = self.spin(src, (src[0], src[1]+1), direction, has_block)

        # ブロック設置のコマンド変換をする
        self.commands.append(Instructions.PUT)
        return direction  


    def put_block_from_cross_circle(self, src, dst, direction, has_block):
        """
        交点サークルからブロックを設置する動作をコマンドに変換する。
        """
        # 交点サークルの座標からブロックサークルの座標を引く
        sub = (src[0] - dst[0], src[1] - dst[1])

        if sub == (0,0):    # ブロックサークルの左上の交点サークル
            if direction == 0 or direction == 2:    # 向きが北 or 東
                # 走行体が東に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0], src[1]+1), direction, has_block)
                # 右方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_R)
            if direction == 4 or direction == 6:    # 向きが西 or 南
                # 走行体が南に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0]+1, src[1]), direction, has_block)
                # 左方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_L)
        
        if sub == (0,1):    # ブロックサークルの右上の交点サークル
            if direction == 2 or direction == 4:    # 向きが東 or 南
                # 走行体が南に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0]+1, src[1]), direction, has_block)
                # 右方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_R)
            if direction == 0 or direction == 6:    # 向きが北 or 西
                # 走行体が西に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0], src[1]-1), direction, has_block)
                # 左方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_L)
        
        if sub == (1,0):    # ブロックサークルの左下の交点サークル
            if direction == 0 or direction == 6:    # 向きが北 or 西
                # 走行体が北に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0]-1, src[1]), direction, has_block)
                # 右方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_R)
            if direction == 2 or direction == 4:    # 向きが東 or 南
                # 走行体が東に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0], src[1]+1), direction, has_block)
                # 左方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_L)
        
        if sub == (1,1):    # ブロックサークルの右下の交点サークル
            if direction == 0 or direction == 2:    # 向きが北 or 東
                # 走行体が北に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0]-1, src[0]-1), direction, has_block)
                # 左方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_L)
            if direction == 4 or direction == 6:    # 向きが南 or 西
                # 走行体が西に向くように回頭コマンドの変換をする
                direction = self.spin(src, (src[0], src[1]-1), direction, has_block)
                # 右方向にブロックを設置する
                self.commands.append(Instructions.QUICK_PUT_R)
        
        return direction
