"""
    @file: block_circles_path.py
    @author: T.Miyaji
    @brief: ブロックサークル内の黒ブロックを運搬する経路計算クラス
"""
from block_bingo_coordinate import BlockCirclesCoordinate

class BlockCirclesTracks():
    def __init__(self, coordinate):
        """
        ブロックサークル間を移動する際の経路を格納する
        
        Parameters
        ----------
        coordinate : BlockCirclesCoordinate
            ブロックサークル番号に関連するサークルの座標
        """
        
        # 内回りの経路
        self.inner_tracks = [coordinate.get(1), coordinate.get(4),
                             coordinate.get(6), coordinate.get(7),
                             coordinate.get(8), coordinate.get(5),
                             coordinate.get(3), coordinate.get(2)]
        # 外回りの経路
        self.outer_tracks = [coordinate.get(1), coordinate.get(2),
                             coordinate.get(3), coordinate.get(5), 
                             coordinate.get(8), coordinate.get(7),
                             coordinate.get(6), coordinate.get(4)]

class BlockCirclesSolver():
    def __init__(self, bonus, black, color, is_left):
        """
        ブロックサークル内の黒ブロックを運搬する経路を計算するための情報を登録する。
        
        Parameters
        ----------
        bonus : int
            ボーナスサークル番号
        black : int
            ブロックサークル内の黒ブロックが置かれているサークル番号
        color : int
            ブロックサークル内のカラーブロックが置かれているサークル番号
        is_left : bool
            Lコースかどうか
        """
        self.bonus = bonus
        self.black = black
        self.color = color
        self.is_left = is_left
        self.coordinate = BlockCirclesCoordinate(is_left, bonus)
    
    def solve(self):
        """
        ブロックサークル内の黒ブロック運搬経路を計算する。
        """
        tracks = BlockCirclesTracks(self.coordinate)
        
        # ブロックサークルに進入するサークル番号を計算する
        enter = self.enter_block_circle()
        
        # 黒ブロックを取得するための経路を計算する
        catch_path = self.path_to_catch_block(enter, tracks)
        
        # 黒ブロックが置かれたサークルからボーナスサークルまでの経路を計算する
        placement_path = self.path_to_bonus_circle(tracks)
        
        return [enter] + catch_path + placement_path
            
    def subset_of_tracks(self, start, goal, tracks):
        """
        経路の部分集合を取得する。
        
        Parameters
        ----------
        start : tuple
            始点となるサークルの座標
        goal : tuple
            終点となるサークルの座標
        tracks : list
            経路
        """
        # 始点または終点が経路に存在しない場合は、Noneを返す
        if start not in tracks or goal not in tracks:
            return None

        # 始点は部分集合に含めないために1を足す        
        start_index = tracks.index(start) + 1
        # 終点は部分集合に含めるために1を足す
        goal_index = tracks.index(goal) + 1
        
        # 始点が終点よりも後ろにある場合、始点と経路の末尾、経路の先頭と終点までの部分集合を連結して返す(循環リスト)
        if goal_index < start_index:
            # 始点と経路の末尾までの部分集合を取得する
            back = tracks[start_index : len(tracks)]
            # 経路の先頭と終点までの部分集合を取得する
            front = tracks[0 : goal_index]
            return back + front
            
        return tracks[(start_index) % len(tracks) : goal_index]
    
    def enter_block_circle(self):
        """
        ブロックサークルに進入するサークル番号を計算する。
        """
        # 原則としてLコースのときは、4番サークルに進入する (Rコースのときは、5番サークル)
        enter = self.coordinate.get(4) if self.is_left else self.coordinate.get(5)
        # 代替策としてLコースのときは、6番サークルに進入する (Rコースのときは、8番サークル)
        plan_b = self.coordinate.get(6) if self.is_left else self.coordinate.get(8)
        
        # 進入サークルにカラーブロックが置いてあるかチェックする
        if enter == self.coordinate.get(self.color):
            enter = plan_b
        
        # 代替策のサークルに黒ブロックが置いてあるかチェックする
        if plan_b == self.coordinate.get(self.black):
            enter = plan_b
        
        return enter

    def path_to_catch_block(self, enter, tracks):
        """
        黒ブロックを取得するための経路を計算する。
        
        Parameters
        ----------
        enter : tuple
            進入するサークルの座標
        tracks : list
            経路
        """
        # 原則として内回りの経路を選択する
        path = self.subset_of_tracks(enter, self.coordinate.get(self.black), tracks.inner_tracks)
        
        # 選択した経路内にカラーブロックが置かれているサークルがあるかチェックする
        if self.coordinate.get(self.color) in path:
            path = self.subset_of_tracks(enter, self.coordinate.get(self.black), tracks.outer_tracks)
        
        return path

    def path_to_bonus_circle(self, tracks):
        """
        黒ブロックが置かれたサークルからボーナスサークルまでの経路を計算する。
        
        Parameters
        ----------
        tracks : list
            経路
        """
        # 原則として内回りの経路を選択する
        path = self.subset_of_tracks(self.coordinate.get(self.black), self.coordinate.get(self.bonus), tracks.inner_tracks)
        outer_path = self.subset_of_tracks(self.coordinate.get(self.black), self.coordinate.get(self.bonus), tracks.outer_tracks)
        
        # 選択した経路内にカラーブロックが置かれているサークルがあるかチェックする
        if self.coordinate.get(self.color) in path[0:-1]:
            path = self.subset_of_tracks(self.coordinate.get(self.black), self.coordinate.get(self.bonus), tracks.outer_tracks)
        # 内回り、外回りの両方にもゴールを除いてカラーブロックが置かれていないとき
        elif self.coordinate.get(self.color) not in outer_path[0:-1]:
            # 内回りよりも外回りの方が早い場合は、外回りを採用する
            path = outer_path if len(outer_path) < len(path) else path
        return path
