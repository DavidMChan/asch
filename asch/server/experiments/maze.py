from .base import BaseGame


class Maze(BaseGame):

    @staticmethod
    def name():
        return 'maze'


class ICMLMaze(BaseGame):

    @staticmethod
    def name():
        return 'icml_maze'
