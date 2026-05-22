import pathlib
import sys


if __package__ in (None, ""):
    sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))


from langgraph.graph import (
    StateGraph,
    END
)

from app.agents.state import AgentState

from app.agents.classifier import (
    classify_intent
)

from app.memory.retriever import (
    retrieve_memory
)

from app.agents.router import (
    choose_agent
)

from app.agents.conditional_edges import (
    route_agent
)

from app.agents import (
    scheduling_agent,
    leave_agent,
    compliance_agent,
    clarification_agent
)

from app.memory.store_memory import (
    memory_node
)

from app.audit.logger import (
    audit_node
)


workflow = StateGraph(AgentState)


# nodes
workflow.add_node(
    "classifier",
    classify_intent
)

workflow.add_node(
    "memory_retrieval",
    retrieve_memory
)

workflow.add_node(
    "router",
    choose_agent
)

workflow.add_node(
    "scheduling",
    scheduling_agent.handle
)

workflow.add_node(
    "leave",
    leave_agent.handle
)

workflow.add_node(
    "compliance",
    compliance_agent.handle
)

workflow.add_node(
    "clarification",
    clarification_agent.handle
)

workflow.add_node(
    "memory_store",
    memory_node
)

workflow.add_node(
    "audit",
    audit_node
)


# flow
workflow.set_entry_point(
    "classifier"
)

workflow.add_edge(
    "classifier",
    "memory_retrieval"
)

workflow.add_edge(
    "memory_retrieval",
    "router"
)


# dynamic routing
workflow.add_conditional_edges(
    "router",
    route_agent,
    {
        "scheduling": "scheduling",
        "leave": "leave",
        "compliance": "compliance",
        "clarification": "clarification"
    }
)


# after agents
workflow.add_edge(
    "scheduling",
    "memory_store"
)

workflow.add_edge(
    "leave",
    "memory_store"
)

workflow.add_edge(
    "compliance",
    "memory_store"
)

workflow.add_edge(
    "clarification",
    "memory_store"
)

workflow.add_edge(
    "memory_store",
    "audit"
)

workflow.add_edge(
    "audit",
    END
)


graph = workflow.compile()