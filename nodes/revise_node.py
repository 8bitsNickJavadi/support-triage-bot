from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

_llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

_PROMPT = ChatPromptTemplate.from_template(
"""
Revise the draft reply for the support ticket based on the reviewer's feedback.

Original Ticket:
{ticket}

Previous Draft:
{draft_reply}

Reviewer Feedback:
{reviewer_feedback}

---

Revised Reply:
"""
)

def revise_node(state: dict) -> dict:
    print(f"\n=== revise_node ===")
    print(f"Input state keys: {list(state.keys())}")

    try:
        messages = _PROMPT.format_messages(
            ticket=state.get("ticket", ""),
            draft_reply=state.get("draft_reply", ""),
            reviewer_feedback=state.get("reviewer_feedback", "")
        )
        response = _llm.invoke(messages)
        new_draft = response.content.strip()
        
        current_revisions = state.get("revisions", 0) + 1
        print(f"Generated revised draft. Revision count: {current_revisions}")

        return {
            "draft_reply": new_draft,
            "revisions": current_revisions,
            "awaiting_approval": False, # Reset for the next approval cycle
        }

    except Exception as e:
        print(f"Error during revision: {str(e)}")
        return {
            "draft_reply": f"Error during revision: {str(e)}",
            "awaiting_approval": False,
        }
