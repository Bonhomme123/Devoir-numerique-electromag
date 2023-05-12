from typing import NamedTuple, Union, Tuple

import numpy as np


class Position(NamedTuple):
    x: Union[int, slice]
    y: Union[int, slice]


class Current(NamedTuple):
    x: float
    y: float
    z: float = 0


class Wire:

    def __init__(self, start: Tuple[int, int], stop: Tuple[int, int], current: Current, voltage: float):
        if start[0] == stop[0]:
            self._vertical = True
            self._horizontal = False
        elif start[1] == stop[1]:
            self._vertical = False
            self._horizontal = True
        else:
            self._vertical = False
            self._horizontal = False

        if not self._vertical and not self._horizontal:
            raise ValueError("A wire can only be defined as a vertical or horizontal straight line.")

        self._start = start
        self._stop = stop
        self._current = current
        self._voltage = voltage

    @property
    def position(self) -> Position:
        if self._vertical:
            if self._start[1] > self._stop[1]:
                stop_smidgen, step = 0, -1
            else:
                stop_smidgen, step = 1, 1
            numpy_slice = np.s_[self._start[0], slice(self._start[1], self._stop[1] + stop_smidgen, step)]
            return Position(x=numpy_slice[0], y=numpy_slice[1])
        elif self._horizontal:
            if self._start[0] > self._stop[0]:
                stop_smidgen, step = 0, -1
            else:
                stop_smidgen, step = 1, 1
            numpy_slice = np.s_[slice(self._start[0], self._stop[0] + stop_smidgen, step), self._start[1]]
            return Position(x=numpy_slice[0], y=numpy_slice[1])

    @property
    def current(self) -> Current:
        return self._current

    @property
    def voltage(self) -> float:
        return self._voltage
