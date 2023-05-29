# Fractal #

This is a python package with methods for self-similar structures.

## Quick guide to usage ##

You need at least `python 3.11`. Install the package via

```bash
python3 -m pip install git+https://github.com/raj-open/fractal.git@main
```

Use the package as follows:

```py
from r_open_fractal import *;

# create fractal objects as list (defaults as generator)
images = list(peano.iterator(N=5, noise=0.));

# define settings for plots:
settings = peano.PlotSettings(
    scale = [256, 256],
    # use intellisense to see other required/optional arguments
    ...
);

# store as images:
for cb in peano.plot_iterator(images, path=lambda t: f'path/to/output_{t}.png', settings=settings):
    # note that this is a callback function
    cb();

# store as gif-animation:
peano.visualise_animation(images, path='path/to/output.gif', settings=settings);
```

See [examples/README.md](examples/README.md) for more information
and [examples/example.py](examples/example.py) for a full example.
