"""Level 4: check structured binding separately from provider capabilities."""

import pytest
from langchain_core.runnables import RunnableLambda

from langchain_practice.exercises.level02_tools import StudyPlan
from langchain_practice.exercises.level04_structured import generate_plan

pytestmark = pytest.mark.exercise


class StructuredModelStub:
    def __init__(self, output):
        self.output = output
        self.schemas, self.prompts = [], []

    def with_structured_output(self, schema):
        self.schemas.append(schema)

        def invoke(prompt):
            self.prompts.append(prompt.to_messages() if hasattr(prompt, "to_messages") else prompt)
            return self.output

        return RunnableLambda(invoke)


def test_structured_plan_binding_and_business_limit():
    plan = StudyPlan(topic="RAG", steps=["Read"], minutes=30)
    model = StructuredModelStub(plan)
    assert generate_plan(model, "  RAG  ", 30) is plan
    assert model.schemas == [StudyPlan]
    assert len(model.prompts) == 1
    assert any(message.type == "system" for message in model.prompts[0])
    human = "\n".join(message.content for message in model.prompts[0] if message.type == "human")
    assert "RAG" in human and "30" in human


def test_schema_valid_but_over_budget_is_rejected():
    model = StructuredModelStub(StudyPlan(topic="RAG", steps=["Read"], minutes=60))
    with pytest.raises(ValueError):
        generate_plan(model, "RAG", 30)
    assert len(model.prompts) == 1


@pytest.mark.parametrize("topic,budget", [(" ", 30), ("RAG", 0), ("RAG", 121)])
def test_invalid_input_does_not_bind_model(topic, budget):
    model = StructuredModelStub(None)
    with pytest.raises(ValueError):
        generate_plan(model, topic, budget)
    assert model.schemas == [] and model.prompts == []


def test_unexpected_structured_type_is_not_silently_repaired():
    model = StructuredModelStub({"topic": "RAG", "steps": ["Read"], "minutes": 30})
    with pytest.raises(TypeError):
        generate_plan(model, "RAG")


def test_binding_error_propagates():
    class FailingModel:
        def with_structured_output(self, schema):
            raise OSError("binding unavailable")

    with pytest.raises(OSError, match="binding unavailable"):
        generate_plan(FailingModel(), "RAG")
