import heapq
from block_bingo_coordinate import Color

class Node():
    '''
    各ノード（交点サークル、中点、ブロックサークル）を表す。
    ブロックサークルは使用しないが、座標を揃えるために存在する。
    C:交点サークル
    M:中点
    数字:ブロックサークル
    全てのC、M、数字に座標を割り当てる。

    (0,0) C--M--C--M--C--M--C  (0,6)
          M  1  M  2  M  3  M
          C--M--C--M--C--M--C
          M  4  M  5  M  6  M
          C--M--C--M--C--M--C
          M  7  M  8  M  9  M
    (6,0) C--M--C--M--C--M--C  (6,6)

    方角: 上向きを0とし、時計回りに45度=1、90度=2、135度=3・・・315度=7とする
            0
           7 1
          6   2
           5 3
            4

    Attributes:
        coorinate: (tuple) 座標
        block_color: (Color) 置かれているブロックの色、ブロックがない場合はNone、ブロックサークルは全てNone
        connected_node: (list) 隣接しているノードのリスト
    '''
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.block_color = None
        self.connected_node = []


class CrossCircleCoordinate():
    '''交点サークル、中点、ブロックサークルの全体を表す。

    Attributes:
        node_list: (list) Nodeクラスのリスト
    '''
    def __init__(self, block_coordinate):
        self.node_list = []
        for y in range(7):
            for x in range(7):
                self.node_list.append(Node((y, x)))
        
        self.setup_connected_node()
        self.setup_block_color(block_coordinate)
    

    def get_node(self, coordinate):
        for n in self.node_list:
            if n.coordinate == coordinate:
                return n
        return None


    def setup_block_color(self, block_coordinate):
        for n in self.node_list:
            if n.coordinate in block_coordinate:
                n.block_color = block_coordinate[n.coordinate]

    
    def setup_connected_node(self):
        CONNECTED_NODE_LIST = [
            [
                [(0, 1), (1, 0)],
                [(0, 0), (0, 2), (1, 0), (1, 2)],
                [(0, 1), (0, 3), (1, 2)],
                [(0, 2), (0, 4), (1, 2), (1, 4)],
                [(0, 3), (0, 5), (1, 4)],
                [(0, 4), (0, 6), (1, 4), (1, 6)],
                [(0, 5), (1, 6)]
            ],
            [
                [(0, 0), (0, 1), (2, 0), (2, 1)],
                [],
                [(0, 1), (0, 2), (0, 3), (2, 1), (2, 2), (2, 3)],
                [],
                [(0, 3), (0, 4), (0, 5), (2, 3), (2, 4), (2, 5)],
                [],
                [(0, 5), (0, 6), (2, 5), (2, 6)]
            ],
            [
                [(1, 0), (2, 1), (3, 0)],
                [(1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2)],
                [(1, 2), (2, 1), (2, 3), (3, 2)],
                [(1, 2), (1, 4), (2, 2), (2, 4), (3, 2), (3, 4)],
                [(1, 4), (2, 3), (2, 5), (3, 4)],
                [(1, 4), (1, 6), (2, 4), (2, 6), (3, 4), (3, 6)],
                [(1, 6), (2, 5), (3, 6)]
            ],
            [
                [(2, 0), (2, 1), (4, 0), (4, 1)],
                [],
                [(2, 1), (2, 2), (2, 3), (4, 1), (4, 2), (4, 3)],
                [],
                [(2, 3), (2, 4), (2, 5), (4, 3), (4, 4), (4, 5)],
                [],
                [(2, 5), (2, 6), (4, 5), (4, 6)]
            ],
            [
                [(3, 0), (4, 1), (5, 0)],
                [(3, 0), (3, 2), (4, 0), (4, 2), (5, 0), (5, 2)],
                [(3, 2), (4, 1), (4, 3), (5, 2)],
                [(3, 2), (3, 4), (4, 2), (4, 4), (5, 2), (5, 4)],
                [(3, 4), (4, 3), (4, 5), (5, 4)],
                [(3, 4), (3, 6), (4, 4), (4, 6), (5, 4), (5, 6)],
                [(3, 6), (4, 5), (5, 6)]
            ],
            [
                [(4, 0), (4, 1), (6, 0), (6, 1)],
                [],
                [(4, 1), (4, 2), (4, 3), (6, 1), (6, 2), (6, 3)],
                [],
                [(4, 3), (4, 4), (4, 5), (6, 3), (6, 4), (6, 5)],
                [],
                [(4, 5), (4, 6), (6, 5), (6, 6)]
            ],
            [
                [(5, 0), (6, 1)],
                [(5, 0), (5, 2), (6, 0), (6, 2)],
                [(5, 2), (6, 1), (6, 3)],
                [(5, 2), (5, 4), (6, 2), (6, 4)],
                [(5, 4), (6, 3), (6, 5)],
                [(5, 4), (5, 6), (6, 4), (6, 6)],
                [(5, 6), (6, 5)]
            ],
        ]

        for n in self.node_list:
            connected_coordinate = CONNECTED_NODE_LIST[n.coordinate[0]][n.coordinate[1]]
            connected_node = []
            for cc in connected_coordinate:
                connected_node.append(self.get_node(cc))

            n.connected_node = connected_node


class CrossCircleSolver():
    '''ある交点サークル(または中点)から別の交点サークル(または中点)への移動経路を計算する。
    属性:
        crossCircleCoordinate: (CrossCirclecoordinate) ブロックビンゴエリアの状態を表す
        direction: (int) 開始ノードでの走行体の向きを表す
    '''
    def __init__(self, direction, block_coordinate):
        self.crossCircleCoordinate = CrossCircleCoordinate(block_coordinate)
        self.direction = direction

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


    def solve_cross_circle(self, num_first_block_circle, current_coordinate):
        bingo_circle_list = self.select_bingo(num_first_block_circle)
        goal_coordinate_list = self.convert_to_goal_coordinate(bingo_circle_list)

        start = current_coordinate
        commands = ''
        for i, block_circle in enumerate(bingo_circle_list):
            # ブロックサークルの色を取得
            color = self.get_circle_color(block_circle)
            # ブロックサークルの色と同じ色のカラーブロックがある場所の座標を取得する
            block_coordinate = self.select_block_coordinate(color, start)
            goal = block_coordinate
            # 現在地からカラーブロックがある場所への経路を取得する
            route = self.aster(start, goal)
            commands += self.route_to_commands(route)
            # print(route)
            # print(commands)

            # カラーブロックがある場所からブロックサークルの左の中点までの経路を取得する
            start = goal
            goal = goal_coordinate_list[i]
            route = self.aster(start, goal)
            commands += self.route_to_commands(route)
            # commands += self.ブロック設置コマンド
            # print(route)
            # print(commands)

            # カラーブロックの左の中点を現在地にする
            start = goal
        return commands


    def route_to_commands(self, route):
        '''ルートをコマンドに変換する
        '''
        commands = ''
        # 経路を元にコマンドを作成する
        for i in range(1, len(route)):
            # 現在地から見た場合の次の座標の方角
            next_direction = self.get_next_direction(route[i-1], route[i])
            # 現在の方角から次の座標の方角を向くのに必要な回頭角度を取得
            rotation_angel = self.get_rotation_angle(self.direction, next_direction)
            
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
            self.direction = next_direction
        
        return commands


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
            

    def get_circle_color(self, num_block_circle):
        BLOCK_CIRCLE_COLOR = {
            1: Color.YELLOW,
            2: Color.GREEN,
            3: Color.RED,
            4: Color.BLUE,
            5: Color.YELLOW,
            6: Color.GREEN,
            7: Color.RED,
            8: Color.BLUE
        }
        return BLOCK_CIRCLE_COLOR[num_block_circle]


    def select_block_coordinate(self, block_color, current_coordinate):
        candidate = []
        for node in self.crossCircleCoordinate.node_list:
            if node.block_color == block_color:
                candidate.append(node.coordinate)

        if len(candidate) == 0:
            return None
        elif len(candidate) == 1:
            return candidate[0]
        else:
            diff_1 = abs(current_coordinate[0] - candidate[0][0]) + abs(current_coordinate[1] - candidate[0][1])
            diff_2 = abs(current_coordinate[0] - candidate[1][0]) + abs(current_coordinate[1] - candidate[1][1])
            if diff_1 < diff_2:
                return candidate[0]
            else:
                return candidate[1]


    def select_bingo(self, num_first_block_circle):
        bingo_list = []
        bingo_candidate = [
            [1, 2, 3],
            [3, 5, 8],
            [6, 7, 8],
            [1, 4, 6]
        ]

        selected_index = []
        for i,candidate in enumerate(bingo_candidate):
            if num_first_block_circle in candidate:
                bingo_list.extend(candidate)
                selected_index.append(i)

        if len(bingo_list) == 3:
            num = bingo_list[0]
            for i,candidate in enumerate(bingo_candidate):
                if (num in candidate) and (not i in selected_index):
                    bingo_list.extend(candidate)

        # bingo_listからnum_first_block_circleを除外したリストを返すようにする
        return list(set(bingo_list)) 


    def convert_to_goal_coordinate(self, bingo_list):
        '''ブロックサークル番号をブロックサークルの左側の中点の座標に変換する
        Args:
            (list) ビンゴにするブロックサークル番号のリスト
        Returns:
            (list) 各ブロックサークルの左側の中点の座標
        '''
        GOAL_COORDINATE = {
            1: (1,0),
            2: (1,2),
            3: (1,4),
            4: (3,0),
            5: (3,4),
            6: (5,0),
            7: (5,2),
            8: (5,4),
        }

        coordinate_list = []
        for num in bingo_list:
            coordinate_list.append(GOAL_COORDINATE[num])

        return coordinate_list


    def aster(self, start, goal):
        '''A*アルゴリズムを用いて、startからgoalまでの経路を求める
        Args:
            start: (tuple) スタートの座標
            goal: (tuple) ゴールの座標
        Returns:
            (list) 座標のリスト
            リストの最初はstart、最後はgoalである
            例:[(0,0), (0,1), (0,3)]
        '''
        passed_list = [start]
        start_cost = self.cost_g(passed_list) + self.cost_h(start, goal)
        checked = {start: start_cost}
        searching_heap = []
        heapq.heappush(searching_heap, (start_cost, passed_list))

        while len(searching_heap) > 0:
            cost, passed_list = heapq.heappop(searching_heap)
            # 最後に探索したノードを取得
            last_passed_node = self.crossCircleCoordinate.get_node(passed_list[-1])
            # 最後に探索したノードが目的地なら探索ヒープを返す
            if last_passed_node.coordinate == goal:
                return passed_list

            # 最後に探索したノードに隣接するノードを探索
            for node in last_passed_node.connected_node:
                if node.block_color == None or node.coordinate == goal:
                    # ブロックが置いていないノードのみ探索する。ただし、ゴールはブロックが置いていても探索する
                    # 経路リストに探索中の座標を追加した一時リストを作成
                    tmp_passed_list = passed_list + [node.coordinate]
                    # 一時リストのスコアを計算
                    tmp_cost = self.cost_g(tmp_passed_list) + self.cost_h(node.coordinate, goal)
                    # 探索中の座標が、他の経路で探索済みかどうかチェック
                    # 探索済みの場合、前回のスコアと今回のスコアを比較
                    # 今回のスコアのほうが大きい場合、次のノードの探索へ
                    if node.coordinate in checked and checked[node.coordinate] <= tmp_cost:
                        continue
                    # 今回のスコアのほうが小さい場合、チェック済みリストに格納
                    # 探索ヒープにスコアと経路リストを格納
                    checked[node.coordinate] = tmp_cost
                    heapq.heappush(searching_heap, (tmp_cost, tmp_passed_list))

        return []


    def cost_h(self, current, goal):
        return abs(goal[0] - current[0]) + abs(goal[1] - current[1])


    def cost_g(self, route):
        COST_1 = 1
        COST_2 = 2
        COST_3 = 3
        COST_4 = 4
        COST_5 = 5
        move_cost = 0
        current_direction = self.direction
        current_coor = route[0]
        # print(route)
        for i in range(1, len(route)):
            next_coor = route[i]
            if current_coor == next_coor:
                continue

            next_direction = self.get_next_direction(current_coor, next_coor)
            rotation_angle = self.get_rotation_angle(current_direction, next_direction)

            abs_rotation_angle = abs(rotation_angle)
            if abs_rotation_angle == 0:
                move_cost += COST_1
            elif abs_rotation_angle == 45:
                move_cost += COST_2
            elif abs_rotation_angle == 90:
                move_cost += COST_3
            elif abs_rotation_angle == 135:
                move_cost += COST_4
            else:
                move_cost += COST_5

            current_direction = next_direction

        return move_cost


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


if __name__ == '__main__':
    block_coordinate = {(0,0): Color.BLUE, (0,4): Color.BLACK, (2,2): Color.GREEN, (2,6): Color.RED, (4,0): Color.RED, (4,4): Color.YELLOW, (6,2): Color.BLUE, (6,6): Color.GREEN}
    crossCircleSolver = CrossCircleSolver(1, block_coordinate)
    print(crossCircleSolver.solve_cross_circle(5, (0,6)))
    # print(crossCircleSolver.aster((6,2), (0,2)))