"""
TODO
"""
from __future__ import print_function, division

import itertools
import cStringIO as StringIO
import numpy as np

from .constants import ArrayWithUnit

__all__ = [
    "Tensor",
]


class Tensor(object):
    """Representation of a 3x3 tensor"""
    def __init__(self, red_tensor, lattice):
        """
        Args:
            red_tensor:
                array-like object with the 9 cartesian components of the tensor
            lattice:
                Lattice object defining the reference system
        """
        self._reduced_tensor = red_tensor
        self._lattice = lattice

    @property
    def reduced_tensor(self):
        return self._reduced_tensor

    @property
    def cartesian_tensor(self):
        try:
            return self._cartesian_tensor
        except AttributeError:
            mat = self._lattice.matrix
            self._cartesian_tensor = np.dot(np.dot(np.transpose(mat),self._reduced_tensor),mat)
        
        return self._cartesian_tensor


    @classmethod
    def from_cartesian_tensor(cls,cartesian_tensor,lattice):
        mat = lattice.inv_matrix
        red_tensor = np.dot(np.dot(np.transpose(mat),cartesian_tensor),mat)
        return cls(red_tensor,lattice)



