"""Provided deterministic graph for stream and environment checks."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ProbeState(TypedDict, total=False):
    value: int
    twice: int
    result: int


def create_probe_graph():
    builder = StateGraph(ProbeState)
    builder.add_node("double", lambda state: {"twice": state["value"] * 2})
    builder.add_node("finish", lambda state: {"result": state["twice"] + 1})
    builder.add_edge(START, "double")
    builder.add_edge("double", "finish")
    builder.add_edge("finish", END)
    return builder.compile()
