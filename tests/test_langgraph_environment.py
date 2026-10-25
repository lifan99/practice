"""Validate installed stream interfaces using the provided probe graph."""

from langgraph_practice.runtime_fixtures import create_probe_graph


def test_langgraph_update_and_event_stream_interfaces():
    graph = create_probe_graph()
    updates = list(graph.stream({"value": 3}, stream_mode="updates", version="v2"))
    assert [part["data"] for part in updates] == [{"double": {"twice": 6}}, {"finish": {"result": 7}}]
    with graph.stream_events({"value": 3}, version="v3") as stream:
        assert list(stream.values)[-1] == {"value": 3, "twice": 6, "result": 7}
        assert stream.output == {"value": 3, "twice": 6, "result": 7}
        assert stream.interrupted is False
