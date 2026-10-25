"""Level 4: check real parallel branches and deterministic report assembly."""

from copy import deepcopy
from threading import Barrier

import pytest
from langgraph.graph.state import CompiledStateGraph

from langgraph_practice.level04_parallel import build_parallel_review

pytestmark = pytest.mark.exercise


def test_reviewers_run_concurrently_and_report_is_sorted():
    barrier = Barrier(2)
    calls = []

    def reviewer(name):
        def run(text):
            calls.append((name, text))
            barrier.wait(timeout=5)
            return f"{name} feedback"
        return run

    graph = build_parallel_review({"clarity": reviewer("clarity"), "accuracy": reviewer("accuracy")})
    assert isinstance(graph, CompiledStateGraph)
    initial = {"text": "  draft  "}
    snapshot = deepcopy(initial)
    result = graph.invoke(initial)
    assert sorted(calls) == [("accuracy", "draft"), ("clarity", "draft")]
    assert sorted(result["reviews"], key=lambda item: item["name"]) == [{"name": "accuracy", "feedback": "accuracy feedback"}, {"name": "clarity", "feedback": "clarity feedback"}]
    assert result["report"] == "accuracy: accuracy feedback\nclarity: clarity feedback"
    assert result["text"] == "draft" and initial == snapshot


def test_review_graph_does_not_leak_previous_results():
    graph = build_parallel_review({"only": lambda text: text.upper()})
    graph.invoke({"text": "first"})
    result = graph.invoke({"text": "second"})
    assert result["reviews"] == [{"name": "only", "feedback": "SECOND"}]


@pytest.mark.parametrize("reviewers", [{}, {" ": lambda _: "x"}, {"9bad": lambda _: "x"}])
def test_invalid_reviewer_configuration(reviewers):
    with pytest.raises(ValueError):
        build_parallel_review(reviewers)


def test_blank_draft_does_not_call_reviewers():
    def forbidden(_):
        pytest.fail("Blank input must not be reviewed.")

    graph = build_parallel_review({"only": forbidden})
    with pytest.raises(ValueError):
        graph.invoke({"text": " \n"})
