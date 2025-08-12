from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

_llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

_PROMPT = ChatPromptTemplate.from_template(
"""
Draft a friendly and helpful reply to the support ticket below.

Use the following context to help you:
- Customer record: {customer_record}
- Relevant FAQ passages:
{faq_passages}

---

Ticket:
{ticket}

Reply:
"""
)

def draft_node(state: dict) -> dict:
    print(f"\n=== draft_node ===")
    print(f"Input state keys: {list(state.keys())}")

    ticket = state.get("ticket", "")
    if not ticket:
        print("ERROR: Missing ticket in state. Cannot draft reply.")
        return {"draft_reply": "Error: Could not generate a reply due to missing ticket information."}

    try:
        messages = _PROMPT.format_messages(
            ticket=ticket,
            customer_record=state.get("customer_record", {}),
            faq_passages="\n---\n".join(state.get("faq_passages", []))
        )
        response = _llm.invoke(messages)
        draft_reply = response.content.strip()
        print(f"Generated draft reply (first 100 chars): {draft_reply[:100]}...")
        return {"draft_reply": draft_reply}

    except Exception as e:
        print(f"Error during draft generation: {str(e)}")
        return {"draft_reply": f"Error: Could not generate a reply. Details: {str(e)}"}
