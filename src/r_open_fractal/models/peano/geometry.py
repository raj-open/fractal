# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ...thirdparty.code import *;
from ...thirdparty.maths import *;
from ...thirdparty.types import *;

from .constants import *;
from .methods import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'INITIAL_AREAS_STANDARD',
    'INITIAL_AREAS_ALL',
    'INITIAL_LENGTHS_STANDARD',
    'INITIAL_LENGTHS_ALL',
    'MUTATION_MATRIX_STANDARD',
    'MUTATION_MATRIX_ALL',
    'MUTATION_AREAS_STANDARD',
    'MUTATION_AREAS_ALL',
    'MUTATION_LENGTHS_STANDARD',
    'MUTATION_LENGTHS_ALL',
    'compute_curve_length',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GEOMETRICAL METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def compute_curve_length(A: np.ndarray) -> np.uint:
    '''
    The curve-length of a block is given by the number of (interior) contrasting edges.
    '''
    m, n = A.shape;
    ctr: np.uint = 0;
    for i, j in np.ndindex(A.shape):
        if i + 1 < m and A[i, j] != A[i+1, j]:
            ctr += 1;
        if j + 1 < n and A[i, j] != A[i, j + 1]:
            ctr += 1;
    return ctr;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LAZY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@make_lazy
def get_values(values: Callable[[np.ndarray], np.uint], shapes: list[np.ndarray]) -> np.ndarray:
    return np.asarray(list(map(values, shapes)), dtype=np.uint);

@make_lazy
def get_mutation_values(values: np.ndarray, mut: np.ndarray) -> np.ndarray:
    return values[:, np.newaxis] * mut;

@make_lazy
def get_mutation_matrix(
    shapes: list[np.ndarray],
    sz: tuple[int, int],
) -> np.ndarray:
    m0, n0 = sz;
    n = len(shapes);
    T = np.zeros((n, n), dtype=np.uint);
    for index, A in enumerate(shapes):
        B = hilbert_transformation(A);
        m, n = B.shape;
        h, w = int(m/m0), int(n/n0);
        for i, j in np.ndindex((h, w)):
            AA = B[i*m0:, j*n0:][:m0, :n0];
            index_ = next(( k for k, AAA in enumerate(shapes) if np.array_equal(AAA, AA) ), -1);
            if index_ == -1:
                continue;
            T[index_, index] += 1;
    return T;

MUTATION_MATRIX_STANDARD = get_mutation_matrix(shapes=INITIAL_SHAPES_STANDARD, sz = (2, 2));
MUTATION_MATRIX_ALL = get_mutation_matrix(shapes=INITIAL_SHAPES_ALL, sz = (2, 2));

INITIAL_AREAS_STANDARD = get_values(values=lambda A: np.sum(A), shapes=INITIAL_SHAPES_STANDARD);
INITIAL_AREAS_ALL = get_values(values=lambda A: np.sum(A), shapes=INITIAL_SHAPES_ALL);
INITIAL_LENGTHS_STANDARD = get_values(values=compute_curve_length, shapes=INITIAL_SHAPES_STANDARD);
INITIAL_LENGTHS_ALL = get_values(values=compute_curve_length, shapes=INITIAL_SHAPES_ALL);

MUTATION_AREAS_STANDARD = get_mutation_values(values=INITIAL_AREAS_STANDARD, mut=MUTATION_MATRIX_STANDARD);
MUTATION_AREAS_ALL = get_mutation_values(values=INITIAL_AREAS_ALL, mut=MUTATION_MATRIX_ALL);
MUTATION_LENGTHS_STANDARD = get_mutation_values(values=INITIAL_LENGTHS_STANDARD, mut=MUTATION_MATRIX_STANDARD);
MUTATION_LENGTHS_ALL = get_mutation_values(values=INITIAL_LENGTHS_ALL, mut=MUTATION_MATRIX_ALL);
