#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ...thirdparty.code import *;
from ...thirdparty.images import *;
from ...thirdparty.io import *;
from ...thirdparty.maths import *;
from ...thirdparty.system import *;
from ...thirdparty.types import *;

from ..generated.peano import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'create_plot',
    'plot',
    'plot_iterator',
    'visualise_ascii',
    'visualise_animation',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PLOTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def plot(A: np.ndarray, path: str, settings: PlotSettings) ->  np.ndarray:
    # create plot
    fig, axs = create_plot(A, settings = settings);
    # save plot
    fig.savefig(path, transparent=settings.transparent, dpi=settings.dpi);
    # read plot as RGBA-image
    frame = imageio.v3.imread(uri=path, plugin='pillow', mode='RGBA');
    return frame;

def plot_iterator(
    it: Iterator[np.ndarray],
    path: Callable[[int], str],
    settings: PlotSettings,
) -> Generator[None, None, Callable[[], np.ndarray]]:
    t = 0;
    for A in it:
        yield partial(plot, A=A, path=path(t), settings=settings);
        t += 1;
    return;

def create_plot(A: np.ndarray, settings: PlotSettings) -> tuple[Figure, Axes]:
    '''
    Plots Peano-like curve from matrix representation.
    '''
    # adjust orientation first.
    match settings.orientation:
        case EnumMatrixPlotOrientation.unchanged:
            pass;
        case EnumMatrixPlotOrientation.transposed:
            A = A.T;
        case EnumMatrixPlotOrientation.rotate_left:
            A = (A.T)[::-1, :];
        case EnumMatrixPlotOrientation.flipped_rows:
            A = A[::-1, :];
        case EnumMatrixPlotOrientation.flipped_columns:
            A = A[:, ::-1];
    # determine scale
    scale = settings.scale or A.shape;
    scale_x, scale_y = scale;
    scale = [scale_x/settings.dpi, scale_y/settings.dpi];
    [w, h] = scale;
    m, n = A.shape;
    # initialise figure + axes
    fig, axs = mplt.subplots(1, 1, constrained_layout=True, figsize=(w, h));
    axs.axis('off');
    '''
    Option: show filled in patches.
    '''
    if settings.fill.show:
        # plot patches
        for i, j in np.ndindex(A.shape):
            x, y = (j/n)*w, (i/m)*h;
            xx, yy = ((j+1)/n)*w, ((i+1)/m)*h;
            if A[i, j] == 1:
                axs.fill(
                    [x, xx, xx, x, x],
                    [y, y, yy, yy, y],
                    color = settings.fill.colour,
                );
    '''
    Option: show grid
    '''
    if settings.grid.show:
        # plot horizontal lines:
        for i in range(m + 1):
            y = (i/m)*h;
            axs.plot([0, w], [y, y], color=settings.grid.colour, linewidth=settings.grid.lw);
        # plot vertical lines:
        for j in range(n + 1):
            x = (j/n)*w;
            axs.plot([x, x], [0, h], color=settings.grid.colour, linewidth=settings.grid.lw);
    '''
    Option: show frame
    '''
    if settings.frame.show:
        axs.plot([0, w, w, 0, 0], [0, 0, h, h, 0], color=settings.frame.colour, linewidth=settings.frame.lw);
    '''
    Option: show curve - segments are determined by edges betwen neighbouring boxes
    '''
    if settings.curve.show:
        # horizontal segments for vertical neighbours: (x, yy) -> (xx, yy)
        for i, j in zip(*np.where(A[:-1, :] != A[1:, :])):
            x, y = (j/n)*w, (i/m)*h;
            xx, yy = ((j + 1)/n)*w, ((i + 1)/m)*h;
            axs.plot([x, xx], [yy, yy], color=settings.curve.colour, linewidth=settings.curve.lw);
        # vertical segments for horizontal neighbours: (xx, y) -> (xx, yy)
        for i, j in zip(*np.where(A[:, :-1] != A[:, 1:])):
            x, y = (j/n)*w, (i/m)*h;
            xx, yy = ((j + 1)/n)*w, ((i + 1)/m)*h;
            axs.plot([xx, xx], [y, yy], color=settings.curve.colour, linewidth=settings.curve.lw);
    return fig, axs;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ASCII PLOTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def visualise_ascii(
    X: np.ndarray,
    sz: tuple[int, int],
) -> str:
    m0, n0 = sz;
    m, n = X.shape;
    w = int(n/n0);
    r = n % n0;

    bar = '-'*n0 + '+';
    bar_long = '+' + bar*w;
    if r != 0:
         bar_long += '-'*r + '+';

    lines = [];
    for i in range(m):
        if i % m0 == 0:
            lines.append(bar_long);
        line = '';
        for j in range(n):
            if j % n0 == 0:
                line += '|';
            match X[i, j]:
                case 1:
                    line += 'x';
                # case 0:
                case _:
                    line += ' ';
        line += '|';
        lines.append(line);
    lines.append(bar_long);

    return '\n'.join(lines);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ANIMATION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def visualise_animation(
    it: Iterator[np.ndarray],
    path: str,
    settings: PlotSettings,
):
    with tempfile.TemporaryDirectory() as tmpdir:
        path_image = f'{tmpdir}/img.png'
        frames = [
            plot(A=A, path=path_image, settings=settings)
            for A in it
        ];
        if settings.mirror:
            frames = frames + frames[::-1][1:];

        n = len(frames);
        dt = 1/settings.fps;
        T = n*dt;
        create_path_if_not_exists(path, as_directory=False);
        imageio.v3.imwrite(
            uri = path,
            image = frames,
            plugin = 'pillow',
            mode = 'RGBA',
            loop = 0,
            transparency = 0,
            duration = T * 1000, # duration in ms
            disposal = 2,
        );
    return;
