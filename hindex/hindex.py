"""Bibliometric index calculations for measuring research impact.

This module provides functions for computing various author-level metrics
including the h-index and related variants.
"""

from math import sqrt
from typing import List, Tuple


def _sorted_and_h(in_list: List[int]) -> Tuple[List[int], int]:
    """Sort the list and compute h-index in a single pass.

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        A tuple of (sorted_list, h_index).
    """
    if not in_list:
        return [], 0
    sorted_list = sorted(in_list, reverse=True)
    h = 0
    for i, count in enumerate(sorted_list):
        if count > i:
            h += 1
        else:
            break
    return sorted_list, h


def h_index(in_list: List[int]) -> int:
    """Calculate the h-index from a list of citation counts.

    The h-index is defined as the maximum value h such that the author
    has published h papers that have each been cited at least h times.

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        The h-index value.

    Example:
        >>> h_index([10, 8, 5, 4, 3])
        4
    """
    _, h = _sorted_and_h(in_list)
    return h


def normalized_h_index(in_list: List[int], scale: float) -> float:
    """Calculate the h-index normalized by a scale factor.

    Useful for comparing researchers across different career lengths
    or fields with different citation practices.

    Args:
        in_list: List of citation counts for each publication.
        scale: The normalization factor (e.g., years of career, field average).

    Returns:
        The h-index divided by the scale factor.

    Raises:
        ZeroDivisionError: If scale is zero.
    """
    h = h_index(in_list)
    return h / float(scale)


def i10_index(in_list: List[int]) -> int:
    """Calculate the i10-index from a list of citation counts.

    The i10-index is the number of publications with at least 10 citations.
    This metric was introduced by Google Scholar.

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        The count of publications with 10 or more citations.

    Example:
        >>> i10_index([15, 10, 8, 3])
        2
    """
    return sum(1 for count in in_list if count >= 10)


def o_index(in_list: List[int]) -> float:
    """Calculate the o-index from a list of citation counts.

    The o-index is the geometric mean of the h-index and the maximum
    citation count: sqrt(h * max_citations).

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        The o-index value, or 0.0 if the list is empty.

    Example:
        >>> o_index([100, 50, 25, 10])
        20.0  # h=4, max=100, sqrt(4*100)=20
    """
    sorted_list, h = _sorted_and_h(in_list)
    if not sorted_list:
        return 0.0
    return sqrt(sorted_list[0] * h)


def g_index(in_list: List[int]) -> int:
    """Calculate the g-index from a list of citation counts.

    The g-index is the largest number g such that the top g publications
    have together received at least g^2 citations.

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        The g-index value.

    Example:
        >>> g_index([10, 10, 10])
        3  # cumulative 30 >= 9
    """
    g = 0
    if not in_list:
        return g
    tally = 0
    for i, count in enumerate(sorted(in_list, reverse=True)):
        if (tally + count) >= (g+1)**2:
            tally += count
            g += 1
        else:
            break
    return g


def w_index(in_list: List[int]) -> int:
    """Calculate the w-index from a list of citation counts.

    The w-index counts publications meeting escalating citation thresholds:
    the 1st paper needs >= 10 citations, 2nd needs >= 20, 3rd needs >= 30, etc.

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        The w-index value.

    Example:
        >>> w_index([100, 50, 30])
        3  # 100>=10, 50>=20, 30>=30
    """
    w = 0
    if not in_list:
        return w
    for count in sorted(in_list, reverse=True):
        threshold = 10 * (w + 1)
        if count >= threshold:
            w += 1
        else:
            break
    return w


def e_index(in_list: List[int]) -> float:
    """Calculate the e-index from a list of citation counts.

    The e-index measures the excess citations received by the h-core
    (the top h publications). It is the square root of the sum of
    (citations - h) for each paper in the h-core.

    Args:
        in_list: List of citation counts for each publication.

    Returns:
        The e-index value.

    Example:
        >>> e_index([10, 8, 5, 3, 1])  # h=3
        3.87  # sqrt((10-3) + (8-3) + (5-3))
    """
    sorted_list, h = _sorted_and_h(in_list)
    if not sorted_list:
        return 0.0
    e_sq = sum(count - h for count in sorted_list[:h])
    return sqrt(e_sq)
