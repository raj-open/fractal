#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ...thirdparty.code import *;
from ...thirdparty.types import *;
from ...thirdparty.misc import *;
from ...thirdparty.maths import *;

from ...setup import config;
from ..generated.peano import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'iterator',
    'hilbert_transformation',
    'text_to_matrix',
    'text_to_transformation',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_TRANSFORMATION = None;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - transformations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def iterator(
    N: int,
    noise: float = 0.,
    A0: Optional[str] = None,
) -> Generator[None, None, np.ndarray]:
    '''
    Generates sequences of Hilbert'ian Peano-curves.
    Optionally adds mutation errors

    ```
    A[i,j] ~> 1 ⊕ A[i,j]
    ```

    with probability given by `noise`.
    '''
    for t in range(N):
        if t == 0:
            if A0 is None:
                A0 = text_to_matrix(dedent(
                    '''
                    ··
                    ##
                    '''
                ));
            A = A0;
        else:
            A = hilbert_transformation(A);
            if noise > 0:
                A = add_noise_to_representation(A, p=noise);
        yield A;
    return;

def hilbert_transformation(A: np.ndarray) -> np.ndarray:
    global _TRANSFORMATION;
    if _TRANSFORMATION is None:
        trans = list(map(text_to_transformation, config.CONFIG_PEANO.transformations));
        _TRANSFORMATION = partial(apply_transform, trans=trans, sz=(2,2), SZ=(4,4));
    return _TRANSFORMATION(A);

def apply_transform(
    A: np.ndarray,
    trans: list[tuple[np.ndarray, np.ndarray]],
    sz: tuple[int, int],
    SZ: tuple[int, int],
) -> np.ndarray:
    m, n = A.shape;
    m0, n0 = sz;
    m1, n1 = SZ;
    L, W = int(m/m0), int(n/n0);
    B = np.zeros((L*m1, W*n1), dtype=np.uint8)
    # subdivide A into patches
    for i, j in np.ndindex(L, W):
        # get patch
        ii, jj = i*m0, j*n0;
        X = A[ii:, jj:][:m0, :n0];
        # obtain transform for patch:
        index = next(( k for k, (X_, _) in enumerate(trans) if np.array_equal(X, X_) ), -1);
        if index == -1:
            continue;
        # write to output in corresponding patch:
        ii, jj = i*m1, j*n1;
        B[ii:, jj:][:m1, :n1] = trans[index][1];
    return B;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - representations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def text_to_matrix(text: str) -> np.ndarray:
    text = re.sub(pattern=r'\||\+|\-', repl='', string=text);
    lines = re.split(pattern='\n', string=text);
    lines = [ line for line in lines if line.strip() != '' ];
    h = len(lines);
    w = len(lines[0]) if h > 0 else 0;
    A = np.zeros((h, w), dtype=np.uint8);
    for i, j in np.ndindex(A.shape):
        match lines[i][j]:
            case r'#':
                A[i, j] = 1;
            # case r'·':
            case _:
                A[i, j] = 0;
    return A;

def text_to_transformation(text: str) -> tuple[np.ndarray, np.ndarray]:
    lines = re.split(pattern='\n', string=text);
    lines1 = [];
    lines2 = [];
    pattern = r'^(.*?)\s+(.*)$';
    for line in lines:
        if re.match(pattern=pattern, string=line):
            line1 = re.sub(pattern=pattern, repl=r'\1', string=line);
            line2 = re.sub(pattern=pattern, repl=r'\2', string=line);
            lines1.append(line1);
            lines2.append(line2);

    text1 = '\n'.join(lines1);
    text2 = '\n'.join(lines2);
    X = text_to_matrix(text1);
    Y = text_to_matrix(text2);
    return X, Y;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY - matrices
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def rotate_matrix(A) -> np.ndarray:
    return A[::-1, :].T;

def vflip_matrix(A) -> np.ndarray:
    return A[::-1, :];

def hflip_matrix(A) -> np.ndarray:
    return A[:, ::-1];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY - effects
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_noise_to_representation(A: np.ndarray, p: float) -> np.ndarray:
    N = (np.random.rand(*A.shape) < p);
    A[N] = 1 - A[N];
    return A;
