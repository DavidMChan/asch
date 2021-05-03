from abc import ABC, abstractclassmethod
import random

from typing import List, Dict, Any

from asch.server.participants import Participant


class BaseGame(ABC):

    @abstractclassmethod
    def name(cls) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def build_path(cls) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def conditions(cls) -> List[str]:
        raise NotImplementedError()

    @abstractclassmethod
    def new_experiment_sequence(cls, condition: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    @classmethod
    def new_participant(cls, condition: str = None) -> Dict[str, Any]:
        # Randomly select a condition
        if condition is None:
            condition = random.choice(cls.conditions())

        # Construct an sequence of tasks
        tasks = cls.new_experiment_sequence(condition)

        participant = Participant(experiment=cls.name(),
                                  condition=condition,
                                  tasks=tasks)
        # Upload the new data
        return Participant.new(participant)

    @classmethod
    def on_finished(data: Dict[str, Any]) -> Dict[str, Any]:
        return data
