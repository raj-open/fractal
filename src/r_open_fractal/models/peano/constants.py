#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ...thirdparty.maths import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'INITIAL_SHAPES_EXTREME',
    'INITIAL_SHAPES_SIDES',
    'INITIAL_SHAPES_CORNERS',
    'INITIAL_SHAPES_DIAGONALS',
    'INITIAL_SHAPES_STANDARD',
    'INITIAL_SHAPES_ALL',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INITIAL_SHAPES_EXTREME = [
    np.asarray([[0, 0], [0, 0]]),
    np.asarray([[1, 1], [1, 1]]),
];

INITIAL_SHAPES_SIDES = [
    np.asarray([[0, 0], [1, 1]]),
    np.asarray([[1, 1], [0, 0]]),
    np.asarray([[0, 1], [0, 1]]),
    np.asarray([[1, 0], [1, 0]]),
];

INITIAL_SHAPES_CORNERS = [
    np.asarray([[0, 0], [0, 1]]),
    np.asarray([[0, 0], [1, 0]]),
    np.asarray([[0, 1], [0, 0]]),
    np.asarray([[1, 0], [0, 0]]),

    np.asarray([[1, 1], [1, 0]]),
    np.asarray([[1, 1], [0, 1]]),
    np.asarray([[1, 0], [1, 1]]),
    np.asarray([[0, 1], [1, 1]]),
];

INITIAL_SHAPES_DIAGONALS = [
    np.asarray([[1, 0], [0, 1]]),
    np.asarray([[0, 1], [1, 0]]),
];

INITIAL_SHAPES_STANDARD = \
    INITIAL_SHAPES_SIDES[:] \
    + INITIAL_SHAPES_CORNERS[:];

INITIAL_SHAPES_ALL = INITIAL_SHAPES_EXTREME[:] \
    + INITIAL_SHAPES_SIDES[:] \
    + INITIAL_SHAPES_CORNERS[:] \
    + INITIAL_SHAPES_STANDARD[:] \
    + INITIAL_SHAPES_DIAGONALS[:];
