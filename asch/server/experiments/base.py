
from abc import ABC, abstractclassmethod
import random

from typing import List, Dict, Any

from asch.server.participants import PARTICIPANT_REGISTRY


class BaseGame(ABC):

    @abstractclassmethod
    def name(cls) -> str:
        return 'BaseGame'

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

        # Construct an experiment sequence
        experiment_sequence = cls.new_experiment_sequence(condition)

        # Build a participant
        participant = {
            '_participant_id': PARTICIPANT_REGISTRY.new(),
            '_current_experiment': 0,
            '_is_finished': len(experiment_sequence) <= 0,
            'condition': condition,
            'experiments': experiment_sequence,
            'results': [],
        }

        return participant

    @abstractclassmethod
    def on_finished(data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
