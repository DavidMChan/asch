from .base import BaseGame

import random


class Blicket(BaseGame):

    @classmethod
    def name(cls):
        return 'blicket'

    @classmethod
    def build_path(cls):
        return 'blicket'

    @classmethod
    def conditions(cls):
        return ['conjunctive', 'disjunctive']

    @classmethod
    def new_experiment_sequence(cls, condition: str):

        # Get a random pair of objects which form the blickets. The game handles the rest.
        objects = [0, 1, 2]
        random.shuffle(objects)
        blickets = set(objects[:2])

        return [{
            'rule': condition,
            'is_blicket': ''.join('1' if i in blickets else '0' for i in range(3)),
        }]
