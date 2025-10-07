"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple


class Facing(Enum):  # Facing 我们定义为一个枚举类，用于定义方向。如有疑问可以自行 Google / Ask AI
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid():
    def __init__(self, width: int, height: int, enemy_pos: tuple):  # DO NOT EDIT THIS METHOD
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}  # 用于存储位置历史，键为步数，值为坐标

    @property
    def current_pos(self) -> Tuple[int, int]:
        """
        current_pos 属性的 getter，返回私有属性 _current_pos
        """
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:
        """
        current_pos 属性的 setter（作为第 1 题留空）

        要求：
          - 接受一个长度为 2 的 tuple (x, y)
          - 若传入非 tuple 或长度不为 2，应抛出 TypeError
          - 将 x, y 强制转换为 int ，检查是否超出了宽高范围，如果任何一个超出则将其限制在最大宽高范围即可
          - 处理后存入 self._current_pos
        """
        if not isinstance(value,tuple) or len(value)!=2:
            raise TypeError("Input must be a tuple of length 2")
        x,y=value
        x=int(x)
        y=int(y)
        if x<0:
            x=0
        elif x>self.width:
            x=self.width
        if y<0:
            y=0
        elif y>self.height:
            y=self.height
        self._current_pos=(x,y)
    def move_forward(self) -> Tuple[int, int]:  # type: ignore
        '''
        让机器人向当前方向走一格
        返回新的坐标 (x,y) 同时更新成员变量
        利用好上面的 setter
        以右为X轴正方向，上为Y轴正方向
        '''
        x,y=self.current_pos
        if self.current_direction==Facing.UP:
            y+=1
        elif self.current_direction==Facing.DOWN:
            y-=1
        elif self.current_direction==Facing.LEFT:
            x-=1
        elif self.current_direction==Facing.RIGHT:
            x+=1
        self.current_pos=(x,y)
        return self.current_pos
    def turn_left(self) -> Facing:  # type: ignore
        '''
        让机器人逆时针转向
        返回一个新方向 (Facing.UP/DOWN/LEFT/RIGHT)
        '''
        if self.current_direction==Facing.UP:
            self.current_direction=Facing.LEFT
        elif self.current_direction==Facing.LEFT:
            self.current_direction=Facing.DOWN
        elif self.current_direction==Facing.DOWN:
            self.current_direction=Facing.RIGHT
        elif self.current_direction==Facing.RIGHT:
            self.current_direction=Facing.UP
        return self.current_direction

    def turn_right(self) -> Facing:  # type: ignore
        '''
        让机器人顺时针转向
        '''
        if self.current_direction==Facing.UP:
            self.current_direction=Facing.RIGHT
        elif self.current_direction==Facing.RIGHT:
            self.current_direction=Facing.DOWN
        elif self.current_direction==Facing.DOWN:
            self.current_direction=Facing.LEFT
        elif self.current_direction==Facing.LEFT:
            self.current_direction=Facing.UP
        return self.current_direction
    def find_enemy(self) -> bool:  # type: ignore
        '''
        如果找到敌人（机器人和敌人坐标一致），就返回true
        '''
        return self.current_pos==self.enemy_pos
    def record_position(self, step: int) -> None:
        '''
        将当前位置记录到 position_history 字典中
        键(key)为步数 step，值(value)为当前坐标 self.current_pos
        例如：step=1 时，记录 {1: (0, 0)}
        '''
        self.position_history[step]=self.current_pos

    def get_position_at_step(self, step: int) -> tuple:  # type: ignore
        '''
        从 position_history 字典中获取指定步数的坐标
        如果该步数不存在，返回 None
        '''
        return self.position_history.get(step,None)
    

"""
在这里你需要实现 AdvancedGrid 类，继承自 Grid 类，并添加以下功能：
1. 追踪移动步数
2. 计算到敌人的曼哈顿距离

类名：AdvancedGrid
继承自：Grid
包含以下新属性：
- steps: int - 追踪移动步数，初始值为 0

包含以下方法：
1. move_forward(self) -> Tuple[int, int]
    调用父类的 move_forward 方法完成移动
    新增实现：移动步数 self.steps 加 1
    返回：移动后新坐标

2. distance_to_enemy(self) -> int
    计算当前位置到敌人位置的曼哈顿距离
    曼哈顿距离 = |x1 - x2| + |y1 - y2|
    返回：曼哈顿距离值

"""
class AdvancedGrid(Grid):
    def __init__(self, width, height, enemy_pos):
        super().__init__(width, height, enemy_pos)
        self.steps=0

    def move_forward(self) -> Tuple[int, int]:
        self.steps+=1
        return super().move_forward()
    def distance_to_enemy(self) -> int:
        x1,y1=self.current_pos
        x2,y2=self.enemy_pos
        return abs(x1-x2)+abs(y1-y2)# Testing package

import random

from main import AdvancedGrid, Facing, Grid  # type: ignore


class TestGrid:
    def setup_method(self):
        """在每个测试方法之前运行"""
        # choose sizes large enough for the movement tests
        self.width = random.randint(3, 7)
        self.height = random.randint(3, 7)
        enemy_x = random.randint(0, self.width)
        enemy_y = random.randint(0, self.height)
        self.enemy_pos = (enemy_x, enemy_y)
        self.grid = Grid(self.width, self.height, self.enemy_pos)

    def test_initialization(self):
        """测试Grid初始化是否正确"""
        assert self.grid.width == self.width
        assert self.grid.height == self.height
        assert self.grid.current_pos == (0, 0)
        assert self.grid.current_direction == Facing.UP
        x, y = self.grid.enemy_pos
        assert 0 <= x <= self.width
        assert 0 <= y <= self.height

    def test_current_pos_setter_accepts_and_casts(self):
        """测试 current_pos setter 是否接受浮点数并转换为整数"""
        g = Grid(5, 5, (0, 0))
        g.current_pos = (1.9, 2.1)  # type: ignore
        assert g.current_pos == (1, 2)

    def test_current_pos_setter_type_error(self):
        """测试 current_pos setter 在传入非法类型时抛出 TypeError"""
        g = Grid(5, 5, (0, 0))
        try:
            # list instead of tuple
            g.current_pos = [1, 2]  # type: ignore
            raise AssertionError("TypeError not raised for non-tuple value")
        except TypeError:
            pass

    def test_current_pos_setter_length_error(self):
        """测试 current_pos setter 在传入长度不为2的tuple时抛出 TypeError"""
        g = Grid(5, 5, (0, 0))
        try:
            g.current_pos = (1, 2, 3)  # type: ignore # length 3 tuple
            raise AssertionError("TypeError not raised for wrong length tuple")
        except TypeError:
            pass

    def test_current_pos_setter_clamps_to_bounds(self):
        """测试 current_pos setter 会将超出边界的值 clamp 到合法范围"""
        g = Grid(3, 4, (0, 0))
        # x beyond width, y beyond height
        g.current_pos = (10, 20)
        assert g.current_pos == (3, 4)
        # negative values clamp to 0
        g.current_pos = (-5, -2)
        assert g.current_pos == (0, 0)

    def test_move_forward_up(self):
        """测试向上移动"""
        self.grid.current_direction = Facing.UP
        self.grid.current_pos = (2, 2)
        new_pos = self.grid.move_forward()
        assert new_pos == (2, 3)
        assert self.grid.current_pos == new_pos

    def test_move_forward_right(self):
        """测试向右移动"""
        self.grid.current_direction = Facing.RIGHT
        self.grid.current_pos = (2, 2)
        new_pos = self.grid.move_forward()
        assert new_pos == (3, 2)
        assert self.grid.current_pos == new_pos

    def test_move_forward_down(self):
        """测试向下移动"""
        self.grid.current_direction = Facing.DOWN
        self.grid.current_pos = (2, 2)
        new_pos = self.grid.move_forward()
        assert new_pos == (2, 1)
        assert self.grid.current_pos == new_pos

    def test_move_forward_left(self):
        """测试向左移动"""
        self.grid.current_direction = Facing.LEFT
        self.grid.current_pos = (2, 2)
        new_pos = self.grid.move_forward()
        assert new_pos == (1, 2)
        assert self.grid.current_pos == new_pos

    def test_move_forward_boundary_check(self):
        """测试边界检查"""
        self.grid.current_direction = Facing.RIGHT
        # place at the right boundary
        self.grid.current_pos = (self.grid.width, min(2, self.grid.height))
        new_pos = self.grid.move_forward()
        assert new_pos == (self.grid.width, min(2, self.grid.height))

        self.grid.current_direction = Facing.LEFT
        self.grid.current_pos = (0, min(2, self.grid.height))
        new_pos = self.grid.move_forward()
        assert new_pos == (0, min(2, self.grid.height))

    def test_turn_left(self):
        """测试左转"""
        # UP -> LEFT
        self.grid.current_direction = Facing.UP
        new_direction = self.grid.turn_left()
        assert new_direction == Facing.LEFT
        assert self.grid.current_direction == Facing.LEFT

        # LEFT -> DOWN
        self.grid.current_direction = Facing.LEFT
        new_direction = self.grid.turn_left()
        assert new_direction == Facing.DOWN
        assert self.grid.current_direction == Facing.DOWN

        # DOWN -> RIGHT
        self.grid.current_direction = Facing.DOWN
        new_direction = self.grid.turn_left()
        assert new_direction == Facing.RIGHT
        assert self.grid.current_direction == Facing.RIGHT

        # RIGHT -> UP
        self.grid.current_direction = Facing.RIGHT
        new_direction = self.grid.turn_left()
        assert new_direction == Facing.UP
        assert self.grid.current_direction == Facing.UP

    def test_turn_right(self):
        """测试右转"""
        # UP -> RIGHT
        self.grid.current_direction = Facing.UP
        new_direction = self.grid.turn_right()
        assert new_direction == Facing.RIGHT
        assert self.grid.current_direction == Facing.RIGHT

        # RIGHT -> DOWN
        self.grid.current_direction = Facing.RIGHT
        new_direction = self.grid.turn_right()
        assert new_direction == Facing.DOWN
        assert self.grid.current_direction == Facing.DOWN

        # DOWN -> LEFT
        self.grid.current_direction = Facing.DOWN
        new_direction = self.grid.turn_right()
        assert new_direction == Facing.LEFT
        assert self.grid.current_direction == Facing.LEFT

        # LEFT -> UP
        self.grid.current_direction = Facing.LEFT
        new_direction = self.grid.turn_right()
        assert new_direction == Facing.UP
        assert self.grid.current_direction == Facing.UP

    def test_find_enemy_true(self):
        """测试找到敌人的情况"""
        # 将机器人移动到敌人位置
        self.grid.current_pos = self.grid.enemy_pos
        result = self.grid.find_enemy()
        assert result == True

    def test_find_enemy_false(self):
        """测试没找到敌人的情况"""
        enemy_x, enemy_y = self.grid.enemy_pos
        if (0, 0) != (enemy_x, enemy_y):
            self.grid.current_pos = (0, 0)
        else:
            self.grid.current_pos = (1, 1)

        result = self.grid.find_enemy()
        assert result == False

    # ===================== Question 4 Tests (字典操作) =====================
    def test_record_position(self):
        """测试记录位置到字典"""
        # choose positions that are within bounds (clamp if needed)
        p1 = (min(1, self.grid.width), min(2, self.grid.height))
        self.grid.current_pos = p1
        self.grid.record_position(1)
        assert 1 in self.grid.position_history
        assert self.grid.position_history[1] == p1

        p2 = (min(3, self.grid.width), min(4, self.grid.height))
        self.grid.current_pos = p2
        self.grid.record_position(2)
        assert 2 in self.grid.position_history
        assert self.grid.position_history[2] == p2

    def test_get_position_at_step(self):
        """测试从字典获取位置"""
        p1 = (min(1, self.grid.width), min(2, self.grid.height))
        self.grid.current_pos = p1
        self.grid.record_position(1)
        p2 = (min(3, self.grid.width), min(4, self.grid.height))
        self.grid.current_pos = p2
        self.grid.record_position(2)

        result = self.grid.get_position_at_step(1)
        assert result == p1

        result = self.grid.get_position_at_step(2)
        assert result == p2

        # 测试不存在的步数
        result = self.grid.get_position_at_step(99)
        assert result is None


class TestAdvancedGrid:
    """测试 Question 5 - 类的继承"""

    def setup_method(self):
        """在每个测试方法之前运行"""
        # choose a width large enough for two right moves from x=2 -> ensure tests stable
        self.width = 7
        self.height = 7
        self.enemy_pos = (5, 5)
        self.grid = AdvancedGrid(self.width, self.height, self.enemy_pos)

    def test_inheritance_initialization(self):
        """测试子类正确继承并初始化父类属性"""
        assert self.grid.width == self.width
        assert self.grid.height == self.height
        assert self.grid.current_pos == (0, 0)
        assert self.grid.current_direction == Facing.UP
        assert self.grid.enemy_pos == self.enemy_pos
        # 测试新增的属性
        assert hasattr(self.grid, 'steps')
        assert self.grid.steps == 0

    def test_move_forward_with_steps(self):
        """测试重写的 move_forward 方法会增加步数"""
        initial_steps = self.grid.steps
        self.grid.current_direction = Facing.RIGHT
        self.grid.current_pos = (2, 2)

        self.grid.move_forward()
        assert self.grid.steps == initial_steps + 1
        assert self.grid.current_pos == (3, 2)

        self.grid.move_forward()
        assert self.grid.steps == initial_steps + 2
        assert self.grid.current_pos == (4, 2)

    def test_distance_to_enemy(self):
        """测试计算到敌人的曼哈顿距离"""
        # 敌人在 (5, 5)，机器人在 (0, 0)
        self.grid.current_pos = (0, 0)
        distance = self.grid.distance_to_enemy()
        assert distance == 10  # |5-0| + |5-0| = 10

        # 机器人在 (3, 2)
        self.grid.current_pos = (3, 2)
        distance = self.grid.distance_to_enemy()
        assert distance == 5  # |5-3| + |5-2| = 5

        # 机器人和敌人重合
        self.grid.current_pos = (5, 5)
        distance = self.grid.distance_to_enemy()
        assert distance == 0

    def test_advanced_grid_has_parent_methods(self):
        """测试子类可以使用父类的方法"""
        # 测试 turn_left
        self.grid.current_direction = Facing.UP
        new_direction = self.grid.turn_left()
        assert new_direction == Facing.LEFT

        # 测试 find_enemy
        self.grid.current_pos = self.enemy_pos
        assert self.grid.find_enemy() == True


class TestRandomized:
    """包含多次随机试验以捕捉边界和不同配置"""

    def test_move_forward_random_trials(self):
        """随机多次测试 move_forward 的正确性（可重复）"""
        trials = 100
        for _ in range(trials):
            width = random.randint(0, 8)
            height = random.randint(0, 8)
            enemy_pos = (random.randint(0, width), random.randint(0, height))
            grid = Grid(width, height, enemy_pos)

            # random position within bounds
            x = random.randint(0, width)
            y = random.randint(0, height)
            grid.current_pos = (x, y)

            # random facing
            grid.current_direction = random.choice(list(Facing))

            # compute expected
            ex_x, ex_y = x, y
            if grid.current_direction == Facing.UP:
                ex_y = min(height, y + 1)
            elif grid.current_direction == Facing.DOWN:
                ex_y = max(0, y - 1)
            elif grid.current_direction == Facing.RIGHT:
                ex_x = min(width, x + 1)
            elif grid.current_direction == Facing.LEFT:
                ex_x = max(0, x - 1)

            res = grid.move_forward()
            assert res == (ex_x, ex_y)
            assert grid.current_pos == (ex_x, ex_y)

    def test_turns_random_trials(self):
        """随机多次测试 turn_left 和 turn_right 的环转逻辑"""
        trials = 100
        for _ in range(trials):
            facing = random.choice(list(Facing))
            # left
            g = Grid(5, 5, (0, 0))
            g.current_direction = facing
            expected_left = Facing((facing.value + 1) % 4)
            expected_right = Facing((facing.value - 1) % 4)
            assert g.turn_left() == expected_left
            # reset and test right
            g.current_direction = facing
            assert g.turn_right() == expected_right

    def test_record_and_get_randomized(self):
        """随机测试字典记录与读取"""
        width = 6
        height = 6
        grid = Grid(width, height, (0, 0))
        records = {}
        steps = random.randint(5, 20)
        for s in range(1, steps + 1):
            pos = (random.randint(0, width), random.randint(0, height))
            grid.current_pos = pos
            grid.record_position(s)
            records[s] = pos

        for s in range(1, steps + 1):
            assert grid.get_position_at_step(s) == records.get(s)

    def test_advancedgrid_random_walk(self):
        """随机多次测试 AdvancedGrid 的步数统计与曼哈顿距离"""
        trials = 50
        for _ in range(trials):
            width = random.randint(3, 8)
            height = random.randint(3, 8)
            enemy = (random.randint(0, width), random.randint(0, height))
            g = AdvancedGrid(width, height, enemy)
            # perform a random number of moves and track expected position
            moves = random.randint(0, 10)
            # pick random starting pos within bounds
            sx = random.randint(0, width)
            sy = random.randint(0, height)
            g.current_pos = (sx, sy)
            g.steps = 0
            # random sequence of facings
            for i in range(moves):
                g.current_direction = random.choice(list(Facing))
                prev_pos = g.current_pos
                res = g.move_forward()
                # steps should increment by 1 each move
                assert g.steps == i + 1
                # position must be updated and within bounds
                px, py = res
                assert 0 <= px <= width
                assert 0 <= py <= height

            # test manhattan distance computation
            cx, cy = g.current_pos
            ex_dist = abs(cx - enemy[0]) + abs(cy - enemy[1])
            assert g.distance_to_enemy() == ex_dist
