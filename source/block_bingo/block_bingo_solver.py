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
