
from .base import BaseGame

import random


class Blicket(BaseGame):

    @staticmethod
    def name():
        return 'blicket'

    @staticmethod
    def conditions():
        return ['conjunctive', 'disjunctive']

    @staticmethod
    def new_experiment_sequence(condition: str):

        # Get a random pair of objects which form the blickets. The game handles the rest.
        objects = [0,1,2]
        random.shuffle(objects)
        blickets = set(objects[:2])

        return [{
            'rule': condition,
            'is_blicket': ''.join('1' if i in blickets else '0' for i in range(3)),
        }]
