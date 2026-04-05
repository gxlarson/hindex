"""Unit tests for hindex bibliometric calculations.

Tests cover all index calculation functions with edge cases,
typical inputs, and boundary conditions.
"""

import pytest
from math import sqrt

from hindex import (
    h_index,
    normalized_h_index,
    i10_index,
    o_index,
    g_index,
    w_index,
    e_index,
)


class TestHIndex:
    """Tests for h-index calculation."""

    @pytest.mark.parametrize(
        "citations,expected",
        [
            ([], 0),
            ([0], 0),
            ([0, 0, 0, 0, 0], 0),
            ([1], 1),
            ([5], 1),
            ([1, 1, 1, 1, 1], 1),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5),
            ([5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 5),
            ([5, 5, 5], 3),
            ([1000000, 3, 2, 1], 2),
            ([900, 2, 10, 4, 1], 3),
            ([150, 30, 20, 10, 9, 8, 3, 1, 0, 0], 6),
        ],
        ids=[
            "empty_list",
            "single_zero",
            "all_zeros",
            "single_one",
            "single_five",
            "all_ones",
            "sequence_1_to_10",
            "ten_fives",
            "three_fives",
            "one_highly_cited",
            "mixed_citations",
            "realistic_distribution",
        ],
    )
    def test_h_index(self, citations, expected):
        assert h_index(citations) == expected

    def test_order_independence(self):
        """H-index should be the same regardless of input order."""
        citations = [10, 1, 5, 3, 8]
        reversed_citations = citations[::-1]
        assert h_index(citations) == h_index(reversed_citations)


class TestNormalizedHIndex:
    """Tests for normalized h-index calculation."""

    @pytest.mark.parametrize(
        "citations,scale,expected",
        [
            ([1, 2, 3, 4, 5], 1, 3.0),
            ([1, 2, 3, 4, 5], 2, 1.5),
            ([1, 2, 3, 4, 5], 10, 0.3),
            ([], 5, 0.0),
            ([100, 100, 100], 3, 1.0),
        ],
        ids=[
            "scale_1",
            "scale_2",
            "scale_10",
            "empty_list",
            "perfect_normalized",
        ],
    )
    def test_normalized_h_index(self, citations, scale, expected):
        assert normalized_h_index(citations, scale) == expected

    def test_scale_zero_raises(self):
        """Division by zero should raise an error."""
        with pytest.raises(ZeroDivisionError):
            normalized_h_index([1, 2, 3], 0)


class TestI10Index:
    """Tests for i10-index calculation."""

    @pytest.mark.parametrize(
        "citations,expected",
        [
            ([], 0),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 0),
            ([10], 1),
            ([11], 1),
            ([9], 0),
            ([10, 20, 30, 19, 8, 9, 0, 33, 10101], 6),
            ([10, 10, 10, 10, 10], 5),
        ],
        ids=[
            "empty_list",
            "all_below_10",
            "exactly_10",
            "just_above_10",
            "just_below_10",
            "mixed_values",
            "all_exactly_10",
        ],
    )
    def test_i10_index(self, citations, expected):
        assert i10_index(citations) == expected


class TestOIndex:
    """Tests for o-index calculation (geometric mean of max citations and h-index)."""

    @pytest.mark.parametrize(
        "citations,expected",
        [
            ([1], sqrt(1 * 1)),
            ([4, 4, 4, 4], sqrt(4 * 4)),
            ([100, 1, 1, 1], sqrt(100 * 1)),
            ([25, 25, 25, 25, 25], sqrt(25 * 5)),
            ([16, 9, 4, 1], sqrt(16 * 3)),
        ],
        ids=[
            "single_element",
            "uniform_citations",
            "one_highly_cited",
            "five_with_25_each",
            "decreasing_squares",
        ],
    )
    def test_o_index(self, citations, expected):
        assert o_index(citations) == pytest.approx(expected)

    def test_empty_list(self):
        """Empty list should return 0.0."""
        assert o_index([]) == 0.0


class TestGIndex:
    """Tests for g-index calculation.

    The g-index is the largest number g such that the top g papers
    have together at least g^2 citations.
    """

    @pytest.mark.parametrize(
        "citations,expected",
        [
            ([], 0),
            ([0], 0),
            ([1], 1),
            ([4], 1),  # 1 paper, g cannot exceed paper count
            ([9], 1),  # 1 paper, g cannot exceed paper count
            ([1, 1, 1, 1], 1),  # cumulative 4, but g=2 needs 4 citations and top 2 only have 2
            ([10, 10, 10], 3),  # 3 papers, cumulative 30 >= 9
            ([25, 8, 5, 3, 3], 5),  # 5 papers, cumulative 44 >= 25
            ([100], 1),  # 1 paper, g cannot exceed paper count
            ([4, 4, 4, 4], 4),  # 4 papers, cumulative 16 >= 16
        ],
        ids=[
            "empty_list",
            "single_zero",
            "single_one",
            "single_four",
            "single_nine",
            "four_ones",
            "three_tens",
            "mixed_citations",
            "single_100",
            "four_fours",
        ],
    )
    def test_g_index(self, citations, expected):
        assert g_index(citations) == expected


class TestWIndex:
    """Tests for w-index calculation.

    The w-index counts papers meeting escalating thresholds:
    1st paper needs >= 10 citations, 2nd needs >= 20, etc.
    """

    @pytest.mark.parametrize(
        "citations,expected",
        [
            ([], 0),
            ([9], 0),
            ([10], 1),
            ([15], 1),
            ([20, 10], 1),  # 2nd paper (10) < 20 threshold
            ([30, 20, 10], 2),  # 3rd paper (10) < 30 threshold
            ([100, 50, 30, 25], 3),  # 4th paper (25) < 40 threshold
            ([10, 10, 10], 1),
            ([5, 5, 5, 5], 0),
            ([100, 50, 40, 40], 4),  # 100>=10, 50>=20, 40>=30, 40>=40
        ],
        ids=[
            "empty_list",
            "below_first_threshold",
            "exactly_first_threshold",
            "above_first_threshold",
            "second_below_threshold",
            "third_below_threshold",
            "fourth_below_threshold",
            "all_tens",
            "all_below_threshold",
            "perfect_w4",
        ],
    )
    def test_w_index(self, citations, expected):
        assert w_index(citations) == expected


class TestEIndex:
    """Tests for e-index calculation.

    The e-index measures excess citations beyond the h-index requirement.
    For the h highest-cited papers, it's sqrt(sum of (citations - h)).
    """

    @pytest.mark.parametrize(
        "citations,expected",
        [
            ([1], sqrt(1 - 1)),
            ([5, 5, 5, 5, 5], sqrt(5 * (5 - 5))),
            ([10, 10, 1], sqrt((10 - 2) + (10 - 2))),
            ([6, 6, 6, 6, 6, 6], sqrt(6 * (6 - 6))),
            ([10, 8, 6, 4, 2], sqrt((10 - 4) + (8 - 4) + (6 - 4) + (4 - 4))),
        ],
        ids=[
            "single_one",
            "exact_h_index_match",
            "excess_citations",
            "six_papers_six_each",
            "decreasing_sequence",
        ],
    )
    def test_e_index(self, citations, expected):
        assert e_index(citations) == pytest.approx(expected)

    def test_empty_list(self):
        """Empty list should return 0."""
        assert e_index([]) == 0.0
