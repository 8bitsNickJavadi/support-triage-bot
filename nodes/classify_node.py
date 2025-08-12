from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

_PROMPT = ChatPromptTemplate.from_template(
"""
Classify the support ticket into one of: billing, account, technical, other.
Return just the label.
Ticket:
{ticket}
"""
)

def classify_node(state):
    print(f"\n=== classify_node ===")
    print(f"Input state keys: {list(state.keys())}")

    ticket = state.get("ticket", "")
    if not ticket:
        print("ERROR: No ticket found in state to classify.")
        return {"category": "other"}

    try:
        messages = _PROMPT.format_messages(ticket=ticket)
        response = _llm.invoke(messages)
        label = response.content.strip().lower()
        
        if label not in {"billing", "account", "technical", "other"}:
            print(f"Warning: Invalid label '{label}' from LLM, defaulting to 'other'")
            label = "other"
            
        print(f"Classified ticket as: {label}")
        return {"category": label}
        
    except Exception as e:
        print(f"Error in classify_node: {str(e)}")
        return {"category": "other"}
