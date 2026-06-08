"""hindex - Bibliometric index calculations for measuring research impact."""

__version__ = "0.1.0"

__all__ = [
    "h_index",
    "normalized_h_index",
    "i10_index",
    "o_index",
    "g_index",
    "w_index",
    "e_index",
]

from .hindex import (
    e_index,
    g_index,
    h_index,
    i10_index,
    normalized_h_index,
    o_index,
    w_index,
)
