from .base import BaseGame

import random

task1 = {
    "type" : "inference",
    "name" : "conjunctive_train",
    "maxObjectsOnDetector": 3,
    "shuffle" : False,
    "rule": "conjunctive",
    "detector_pattern": 0,
    "blicket_arrangement": [1, 0, 1],
    "blicket_colors": [9, 3, 4],
    "blicket_shapes": [0, 1, 2]
}

task2 = {
    "type" : "inference",
    "name" : "conjunctive_test",
    "maxObjectsOnDetector": 3,
    "shuffle" : True,
    "rule": "conjunctive",
    "detector_pattern": 2,
    "blicket_arrangement": [1, 0, 1],
    "blicket_colors": [6, 7, 8],
    "blicket_shapes": [6, 7, 8]
}

tasks = [task1, task2]


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
        return tasks
