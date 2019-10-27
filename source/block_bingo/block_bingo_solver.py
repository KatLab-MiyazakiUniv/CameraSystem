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
        # ブロックサークル間移動したあとの走行体の位置を取得する
        self.position = self.get_robot_position_after_block_circle(block_circles_path)
    

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


    def get_robot_position_after_block_circle(self, block_circles_path):
        """
        ブロックサークル間移動したあとの走行体の位置を計算する。

        Parameters
        ----------
        block_circles_path : list
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
            return (block_circle_point[0], block_circle_point[1] + 0.5)
        else:
            return (block_circle_point[0] + 0.5, block_circle_point[1])
    

    def get_robot_direction(self, src, dst):
        """
        始点から終点まで移動したときの走行体の向きを取得する。

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
    

    def adjacent_nodes(self, node):
        """
        指定ノードの隣接ノードのリストを返す。      

        Parameters
        ----------
        node : tuple
            指定ノード
        """
        # 上下左右の4要素を作成する
        nodes = [(node[0]-0.5, node[1]), (node[0]+0.5, node[1]), 
                 (node[0], node[1]-0.5), (node[0], node[1]+0.5)]
        # ブロックサークルを表す座標を作成する(隣接ノードと認めないため)
        block_circles = [(0.5,0.5), (0.5,1.5), (0.5,2.5),
                         (1.5,0.5), (1.5,1.5), (1.5,2.5),
                         (2.5,0.5), (2.5,1.5), (2.5,2.5)]

        return [node for node in nodes if 0 <= node[0] <= 3 and 0 <= node[1] <= 3 and node not in block_circles]      


    def a_star(self, src, dst):
        """
        A*アルゴリズムを用いて始点ノード(src)から終点ノード(dst)まで移動する経路を探索する。

        Parameters
        ----------
        src : tuple
            始点ノード
        dst : tuple
            終点ノード
        """
        # openリスト
        open = {self.position: 0 + self.Manhattan_distance(self.position, dst)}   # openリスト(辞書型; key: 交点サークルの座標, value: 移動コスト+予測コスト)
        # closeリスト
        close = {}
        # 運搬経路
        path = Path()
        while 1:
            # openリストが空であるとき、例外を送出する(探索失敗)
            if len(open) == 0:
                raise ArithmeticError('open set is empty!')

            # openリストのうち、最もコストの小さい要素を取得する
            elem = min(open.items(), key=lambda x: x[1])[0]

            # 取得した要素が終点ノードなら探索を終了する
            if elem == dst:
                return path.search_path(src, dst)
            
            # 取得した要素をopenリストからcloseリストへ移す
            close[elem] = open.pop(elem)
            # 取得した要素の隣接ノードすべてに対して以下の操作を実行する
            for node in self.adjacent_nodes(elem):
                # 最小コストの候補値を計算する(始点から対象ノードまでの移動コスト + 対象ノードから隣接ノードまでの移動コスト + 隣接ノードからゴールまでの予測コスト)
                cost = (close[elem] - self.Manhattan_distance(elem, dst)) + self.moving_cost(elem, node, path) + self.Manhattan_distance(node, dst)
                # 隣接ノードがopenリストにもcloseリストにも含まれていない場合
                if node not in open and node not in close:
                    # 隣接ノードをopenリストへ追加する
                    open[node] = cost
                    path.set_path(elem, node)
                # 隣接ノードがopenリストにある場合
                if node in open:
                    # cost < f(node)の場合、f(node) = costとする
                    if cost < open[node]:
                        open[node] = cost
                        # 記録してある隣接ノードの親をelemに置き換える
                        path.set_path(elem, node)
                # 隣接ノードがcloseリストにある場合
                if node in close:
                    # f(node)を計算する
                    # cost < f(node)の場合、f(node) = costとする
                    if cost < close[node]:
                        open[node] = cost
                        # 記録してある隣接ノードの親をelemに置き換える
                        path.set_path(elem, node)


    def moving_cost(self, src, dst, path):
        """
        2点間の移動コストを計算して返す。

        Parameters
        ----------
        src : tuple
            始点の座標
        dst : tuple
            終点の座標
        path : dict
            運搬経路
        """
        # 始点にブロックが置かれているかどうかを調べる
        has_block = src in self.cross_circles.open
        # 走行体の向きを求める
        direction = self.current_direction(src, path)
        # 走行体が水平に進むとき
        if src[0] == dst[0]:
            if direction == 0: # 90度右に旋回するとき
                return self.spin90(has_block)

            if direction == 2: # 直進するとき
                return self.straight(has_block, src[1] > dst[1])
            
            if direction == 4: # 90度左に旋回するとき
                return self.spin90(has_block)
            
            if direction == 6: # 180度旋回して直進するとき
                return self.straight(has_block, src[1] < dst[1])

        # 走行体が垂直に進むとき
        if src[1] == dst[1]:
            if direction == 0: # 180度旋回して直進するとき
                return self.straight(has_block, src[0] < dst[0])
        
            if direction == 2: # 90度右に旋回するとき
                return self.spin90(has_block)
           
            if direction == 4: # 直進するとき
                return self.straight(has_block, src[0] > dst[0])

            if direction == 6: # 90度左に旋回するとき
                return  self.spin90(has_block)
        raise ValueError('src or dst is invalid!')


    def straight(self, has_block, should_turn):
        """
        直線のコストを返す。

        Parameters
        ----------
        has_block : bool
            始点にブロックが置いてあるかどうか
        should_turn : bool
            旋回が必要かどうか
        """
        if should_turn:
            return self.spin180(has_block)

        if has_block:
            return 4
        return 1            


    def spin90(self, has_block):
        """
        90度回頭するコストを返す。

        Parameters
        ----------
        has_block : bool
            始点にブロックが置いてあるかどうか
        """
        if has_block:
            return 2
        return 2


    def spin180(self, has_block):
        """
        180度回頭するコストを返す

        Parameters
        ----------
        has_block : bool
            始点にブロックが置いてあるかどうか
        """
        if has_block:
            return 5
        return 1