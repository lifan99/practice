"""Core 3: cosine geometry, invalid dimensions, and stable exact ranking."""

from copy import deepcopy

import pytest

from rag_practice.core.exercises.level03_vectors import cosine_similarity, top_k_vectors

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("left,right,expected", [
    ([1, 0], [3, 0], 1.0), ([1, 0], [0, 1], 0.0),
    ([1, 0], [-1, 0], -1.0), ([0, 0], [1, 2], 0.0),
    ([0, 0], [0, 0], 0.0), ([1, 1], [1, 0], 2 ** -0.5),
])
def test_cosine(left, right, expected):
    assert cosine_similarity(left, right) == pytest.approx(expected)


@pytest.mark.parametrize("left,right", [
    ([], []), ([1], [1, 2]), ([float("nan")], [1]),
    ([1], [float("inf")]), ([float("-inf")], [1]),
])
def test_invalid_vectors(left, right):
    with pytest.raises(ValueError):
        cosine_similarity(left, right)


def test_ranking_handles_negative_scores_ties_and_does_not_mutate():
    vectors = [[-1, 0], [1, 0], [2, 0], [0, 0]]
    snapshot = deepcopy(vectors)
    result = top_k_vectors([1, 0], vectors, 10)
    assert [index for index, _ in result] == [1, 2, 3, 0]
    assert [score for _, score in result] == pytest.approx([1, 1, 0, -1])
    assert vectors == snapshot


def test_top_k_validates_all_rows_before_truncating():
    with pytest.raises(ValueError):
        top_k_vectors([1, 0], [[1, 0], [1]], 1)


def test_empty_candidates_still_validate_query_and_k():
    assert top_k_vectors([1, 0], [], 1) == []
    with pytest.raises(ValueError):
        top_k_vectors([], [], 1)
    with pytest.raises(ValueError):
        top_k_vectors([1], [], 0)
