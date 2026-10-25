LangGraph represents workflows with shared state, nodes, and edges.
A graph can route between nodes and repeat work until a stopping condition holds.

A checkpoint records graph state for a particular execution thread.
An in-memory checkpoint is not durable storage across process restarts.
