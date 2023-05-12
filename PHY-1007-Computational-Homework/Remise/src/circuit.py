from typing import List

from src.wire import Wire


class Circuit:

    def __init__(self, wires: List[Wire]):
        self._wires = wires

    @property
    def wires(self):
        return self._wires
