from abc import ABCMeta, abstractmethod


class ActionDefinition(metaclass=ABCMeta):
    def __init__(self):
        self._name = None
        self._point_with_block = None
        self._point_without_block = None

    @property
    @abstractmethod
    def point_with_block(self):
        pass

    @property
    @abstractmethod
    def point_without_block(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass


class Rotation90(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        return 3

    def point_with_block(self):
        return 3

    def name(self):
        return 'r'


class Rotation180(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        return 2

    def point_with_block(self):
        return 6

    def name(self):
        return 'b'


class StraightAhead(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        return 1

    def point_with_block(self):
        return 5

    def name(self):
        return 's'


class Turning(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        return 1

    def point_with_block(self):
        raise ModuleNotFoundError

    def name(self):
        return 't'


class PutBlock(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        raise ModuleNotFoundError

    def point_with_block(self):
        raise ModuleNotFoundError

    def name(self):
        return 'p'


class GetBlock(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        raise ModuleNotFoundError

    def point_with_block(self):
        raise ModuleNotFoundError

    def name(self):
        return 'g'


class MoveBlockCircle(ActionDefinition):
    def __init__(self):
        super().__init__()

    def point_without_block(self):
        raise ModuleNotFoundError

    def point_with_block(self):
        raise ModuleNotFoundError

    def name(self):
        return 'c'


if __name__ == '__main__':
    r90 = Rotation90()
    a = r90.point_with_block
    r180 = Rotation180()