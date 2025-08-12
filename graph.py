from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from nodes.ingest_faq_node import ingest_faq_node
from nodes.classify_node import classify_node
from nodes.enrich_node import enrich_node
from nodes.retrieve_node import retrieve_node
from nodes.draft_node import draft_node
from nodes.approval_node import approval_node
from nodes.revise_node import revise_node

# Explicit state schema so LangGraph knows all keys and merges per-key
class TriageState(TypedDict, total=False):
    ticket: str
    name: str
    email: str
    category: str
    customer_record: Dict[str, Any]
    faq_retriever: Any
    faq_passages: List[str]
    draft_reply: str
    awaiting_approval: bool
    approval_decision: str
    reviewer_feedback: str
    revisions: int

# Pass-through entry node to seed initial input into state
def start_node(state: TriageState) -> TriageState:
    print("\n=== start_node ===")
    print(f"Input keys: {list(state.keys())}")
    return dict(state)

# Create the graph
graph = StateGraph(TriageState)

# Add all nodes
graph.add_node("start", start_node)
graph.add_node("ingest_faq", ingest_faq_node)
graph.add_node("classify", classify_node)
graph.add_node("enrich", enrich_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("draft", draft_node)
graph.add_node("approval", approval_node)
graph.add_node("revise", revise_node)

# Set the entry point
graph.set_entry_point("start")

# Define the edges
graph.add_edge("start", "ingest_faq")
graph.add_edge("ingest_faq", "classify")
graph.add_edge("classify", "enrich")
graph.add_edge("enrich", "retrieve")
graph.add_edge("retrieve", "draft")
graph.add_edge("draft", "approval")

def route_after_approval(state: TriageState):
    print(f"DEBUG: route_after_approval - Decision: {state.get('approval_decision')}, Revisions: {state.get('revisions', 0)}")
    decision = state.get("approval_decision", "")
    if decision == "approve":
        return END
    elif decision == "revise" and state.get("revisions", 0) < 3:
        return "revise"
    return END  # safety stop

# Add conditional edges
graph.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "revise": "revise",
        END: END,
    }
)

graph.add_edge("revise", "approval")

# Compile the graph
triage_app = graph.compile()

print("DEBUG: Graph compilation complete")
