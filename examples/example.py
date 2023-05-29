#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN EXAMPLE
# Uses repository as package.
#
# NOTE: !! first install the package (see examples/README.md) !!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
from r_open_fractal import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'out');
T_MAX = 5;
PROB_NOISE = 0.;
SETTINGS = peano.PlotSettings(
    curve = peano.PlotSettingsAspect(
        show = True,
        colour = 'blue',
        lw = 2,
    ),
    fill = peano.PlotSettingsAspect(
        show = True,
        colour = hsv_to_rgb((150/360, 0.70, 0.5)),
    ),
    grid = peano.PlotSettingsAspect(
        show = True,
        colour = 'black',
        lw = 1,
    ),
    frame = peano.PlotSettingsAspect(
        show = True,
        colour = 'black',
        lw = 1,
    ),
    orientation = peano.EnumMatrixPlotOrientation.flipped_rows,
    transparent = True,
    scale = [256, 256],
    dpi = 128,
    fps = 8,
    mirror = True,
);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    # create gif
    images = list(peano.iterator(N=T_MAX, noise=PROB_NOISE));
    peano.visualise_animation(
        images,
        path = f'{OUTPUT_PATH}/example-peano.gif',
        settings = SETTINGS,
    );

    # create images
    for cb in peano.plot_iterator(
        images,
        path = lambda t: f'{OUTPUT_PATH}/example-peano-{t}.png',
        settings = SETTINGS,
    ):
        cb();

    # create ascii output
    n = min(T_MAX, 5);
    sides = [ 2**(k+1) for k in range(n) ];
    text = merge_text_blocks_horizontally(*[
        peano.visualise_ascii(A, sz=(h, h))
        for A, h in zip(images, sides)
    ]);
    print(text);
