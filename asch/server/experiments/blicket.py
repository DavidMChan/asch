import random

from .base import BaseGame


conditions = {
    'B1': {
        "type": "inference",
        "name": "B1_conjunctive_train",
        "maxObjectsOnDetector": 3,
        "shuffle": False,
        "rule": "conjunctive",
        "detector_pattern": 0,
        "blicket_arrangement": [1, 0, 1],
        "blicket_colors": [0, 1, 2],
        "blicket_shapes": [0, 1, 2]
    },
    'B2': {
        "type": "inference",
        "name" : "B2_disjunctive_trainV2",
        "maxObjectsOnDetector": 3,
        "shuffle" : False,
        "rule": "disjunctive",
        "detector_pattern": 1,
        "blicket_arrangement": [1, 0, 0],
        "blicket_colors": [3, 4, 5],
        "blicket_shapes": [3, 4, 5]
    },
    'B3': {
        "type": "inference",
        "name": "B3_conjunctive_test",
        "maxObjectsOnDetector": 3,
        "shuffle": True,
        "rule": "conjunctive",
        "detector_pattern": 2,
        "blicket_arrangement": [1, 0, 1],
        "blicket_colors": [6, 7, 8],
        "blicket_shapes": [6, 7, 8]
    },
    'B4': {
        "type": "inference",
        "name" : "B4_disjunctive_testV2",
        "maxObjectsOnDetector": 3,
        "shuffle" : True,
        "rule": "disjunctive",
        "detector_pattern": 2,
        "blicket_arrangement": [1, 0, 0],
        "blicket_colors": [6, 7, 8],
        "blicket_shapes": [6, 7, 8]
    },
    'B5': {
        "type": "inference",
        "name" : "B5_disappearing_demo",
        "maxObjectsOnDetector": 3,
        "shuffle" : False,
        "rule": "B5",
        "detector_pattern": 0,
        "blicket_arrangement": [1, 0, 1],
        "blicket_colors": [0, 1, 2],
        "blicket_shapes": [0, 1, 2]
    }
    'B6': {
        "type": "inference",
        "name": "B6_conjunctive_train_dots",
        "maxObjectsOnDetector": 3,
        "shuffle": False,
        "rule": "conjunctive",
        "detector_pattern": 1,
        "blicket_arrangement": [1, 0, 1],
        "blicket_colors": [0, 1, 2],
        "blicket_shapes": [0, 1, 2]
    },
    'B7': {
        "type": "inference",
        "name" : "B7_disjunctive_trainV2_stripes",
        "maxObjectsOnDetector": 3,
        "shuffle" : False,
        "rule": "disjunctive",
        "detector_pattern": 1,
        "blicket_arrangement": [1, 0, 0],
        "blicket_colors": [3, 4, 5],
        "blicket_shapes": [3, 4, 5]
    },
    'C1': {
        "type": "inference",
        "name": "C1_conjunctive_test",
        "maxObjectsOnDetector": 3,
        "shuffle": True,
        "rule": "conjunctive",
        "detector_pattern": 2,
        "blicket_arrangement": [1, 0, 1],
        "blicket_colors": [6, 7, 8],
        "blicket_shapes": [6, 7, 8],
        "tutorial_number": 0
    },
    'C2': {
        "type": "inference",
        "name": "C2_disjunctive_test",
        "maxObjectsOnDetector": 3,
        "shuffle": True,
        "rule": "conjunctive",
        "detector_pattern": 2,
        "blicket_arrangement": [0, 0, 1],
        "blicket_colors": [6, 7, 8],
        "blicket_shapes": [6, 7, 8],
        "tutorial_number": 0
    },
    'C3': {
        "type": "inference",
        "name": "C3_conjunctive_test",
        "maxObjectsOnDetector": 3,
        "shuffle": True,
        "rule": "conjunctive",
        "detector_pattern": 2,
        "blicket_arrangement": [1, 0, 1],
        "blicket_colors": [6, 7, 8],
        "blicket_shapes": [6, 7, 8],
        "tutorial_number": 1
    },
    'C4': {
        "type": "inference",
        "name": "C4_disjunctive_test",
        "maxObjectsOnDetector": 3,
        "shuffle": True,
        "rule": "conjunctive",
        "detector_pattern": 2,
        "blicket_arrangement": [0, 0, 1],
        "blicket_colors": [6, 7, 8],
        "blicket_shapes": [6, 7, 8],
        "tutorial_number": 1
    }
}


# tutorial number 0 conjunctive is strips and disjunctive is dots

class Blicket(BaseGame):

    @classmethod
    def name(cls):
        return 'blicket'

    @classmethod
    def build_path(cls):
        return 'blicket'

    @classmethod
    def conditions(cls):
        return ['B1', 'B2', 'B3', 'B4', 'B5']

    @classmethod
    def new_experiment_sequence(cls, condition: str):

        # Get a random pair of objects which form the blickets. The game handles the rest.
        if condition in conditions.keys():
            return [conditions[condition]]
        else:
            return [list(conditions.values())[0]]
