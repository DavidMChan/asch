
from typing import Dict

from .base import BaseGame  # noqa: F401

# Register your experiments here
from .blicket import *  # noqa: F401
from .maze import *  # noqa: F401

EXPERIMENT_TYPES: Dict[str, BaseGame] = {t.name(): t for t in BaseGame.__subclasses__()}
