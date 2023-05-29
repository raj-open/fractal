#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ..thirdparty.misc import *;
from ..thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'merge_text_blocks_horizontally',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TEXT METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def merge_text_blocks_horizontally(*imgs: str, sep: str = '    ') -> str:
    if len(imgs) == 0:
        return '';
    if len(imgs) == 1:
        return imgs[0];

    img = imgs[0];
    lines = re.split(pattern=r'\n', string=img) or [''];
    L = len(lines[0]);
    for img_ in imgs[1:]:
        lines_ = re.split(pattern=r'\n', string=img_) or [''];
        L_ = len(lines_[0]);
        empty = ' '*L;
        empty_ = ' '*L_;
        L += len(sep) + L_;
        h1 = len(lines);
        h2 = len(lines_);
        lines = [
            (lines[k] if k < h1 else empty) \
            + sep \
            + (lines_[k] if k < h2 else empty_)
            for k in range(max(h1, h2))
        ];

    lines = [ line.rstrip() for line in lines ];
    img = '\n'.join(lines);
    return img;
