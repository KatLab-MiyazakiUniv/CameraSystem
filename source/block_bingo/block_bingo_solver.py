"""
    @file   block_bingo_solver.py
    @author T.Miyaji
    @brief  ブロックビンゴを攻略するための経路を計算するクラス
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

class Path():
    """
    運搬経路を提供するクラス。運搬経路は、辞書型で表現する。
        dict[終点] = 始点
    の形で格納し、経路が求まったあとでdictを終点から逆順に辿ることで「始点=>終点」の経路が得られる。
    """
    def __init__(self):
        self.path = {} # 運搬経路を格納する辞書
    

    def set_path(self, src, dst):
        """
        運搬経路を格納する。

        Parameters
        ----------
        src : tuple
            始点の座標
        dst : tuple
            終点の座標
        """
        self.path[dst] = src
    

    def get(self, dst):
        """
        指定した終点につながる始点を取得する。

        Parameters
        ----------
        dst : tuple
            終点の座標
        """
        return self.path.get(dst)
    

    def search_path(self, start, goal):
        """
        始点から終点に至るまでの運搬経路をすべてを取得する。
        終点からつながる経路を、始点が見つかるまで、取得して返却する。
        
        Parameters
        ----------
        start : tuple
            始点の座標
        goal : tuple
            終点の座標
        """
        path = [goal]
        node = self.get(goal)

        while node is not None:
            path.append(node)
            node = self.get(node)
        
        if path[-1] != start:
            raise ArithmeticError('could not find the path from start node!')
 
        return path[::-1]


class BlockBingoSolver():
    def __init__(self, block_circles, cross_circles, block_circles_path):
        """
        ブロックビンゴを成立させるための経路を計算するクラス。

        Parameters
        ----------
            block_circles : BlockCirclesCoordinate
                ブロックサークルの座標
            cross_circles : CrossCirclesCoordinate
                交点サークルの座標
            block_circles_path : list
                ブロックサークル間移動の運搬経路
        """
        # ブロックサークルの座標クラス
        self.block_circles = block_circles
        # 交点サークルの座標クラス
        self.cross_circles = cross_circles

        # ブロックサークル間移動したあとの走行体の向きを取得する
        self.direction = self.get_robot_direction_after_block_circle(block_circles_path)
        # ブロックサークル間移動したあとに最も近くにあるブロックが置かれた交点サークルまで移動する
        self.position = self.move_initial_position(block_circles_path)
        # 現在地の交点サークルにあるブロックは取得済みなので削除する
        self.cross_circles.move_block(self.position)
    

    def get_robot_direction_after_block_circle(self, block_circles_path):
        """
        ブロックサークル間移動したあとの走行体の向きを計算する。

        Parameters
        ----------
            block_circles_path
                ブロックサークル間移動の運搬経路
        """
        # ボーナスサークルへ進入したときの走行体の向きが知りたいので
        # ブロックサークル間の運搬経路の末尾とその1つ前の座標を取得する
        last = block_circles_path[-1]
        prev = block_circles_path[-2]

        return self.get_robot_direction(prev, last)


    def move_initial_position(self, block_circles_path):
        """
        ブロックサークル間を移動したあとに走行体が向かうブロックが置かれた交点サークルを算出する。
        [方針]
            1. ブロックサークル間移動後の黒線の中点の座標を計算する 例: (1,0.5)なら1番と4番サークルの間
            2. 黒線の中点座標から最も近いブロックが置かれた交点サークルの座標を計算する
        
        Parameters
        ----------
            block_circles_path
                ブロックサークル間移動の運搬経路
        """
        # ボーナスサークルへ進入したあとの走行体の位置が知りたいので
        # ブロックサークル間の運搬経路の末尾とその1つ前の座標を取得する
        last = block_circles_path[-1]
        prev = block_circles_path[-2]

        # (末尾)と(末尾の1つ前)で座標が大きい方を取得する
        block_circle_point = max([last, prev])
        # ブロックサークル間移動後の走行体の向きが北向きor南向きならcolumn += 0.5
        if self.direction == 0 or self.direction == 4:
            src = (block_circle_point[0], block_circle_point[1] + 0.5)
        else:
            src = (block_circle_point[0] + 0.5, block_circle_point[1])

        # 中点座標pointからブロックが置かれた交点サークルの座標との距離を計算する
        distances = list(map(lambda x: abs(src[0]-x[0]) + abs(src[1]-x[1]), self.cross_circles.open))

        # 走行体に最も近いブロックが置かれた交点サークルの座標を取得する
        dst = self.cross_circles.open[distances.index(min(distances))]

        # 走行体が現在向いている方向から移動先の交点サークルがどの向きにあるかを求める
        direction_after_moving = self.get_robot_direction(src, dst)

        # 走行体の向いている方向を更新
        self.direction = direction_after_moving
        
        return dst
    

    def get_robot_direction(self, src, dst):
        """
        始点から終点までの移動したときの走行体の向きを取得する。

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


    def Manhattan_distance(self, src, dst):
        """
        2点間のマンハッタン距離を計算して返す。

        Parameters
        ----------
        src : tuple
            始点の座標
        dst : tuple
            終点の座標
        """
        return abs(dst[0]-src[0]) + abs(dst[1]-src[1])
    

    def current_direction(self, current, path):
        """
        走行体の現在地から走行体の向きを返す。

        Parameters
        ---------
        current : tuple
            走行体の現在地
        """
        last = path.get(current)

        # 走行体の初期位置から移動していない場合は、初期の走行体の向きを返す
        if last is None:
            return self.direction
        return self.get_robot_direction(last, current)