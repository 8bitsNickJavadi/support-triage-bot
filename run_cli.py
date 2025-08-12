import sys
from dotenv import load_dotenv; load_dotenv()
from graph import triage_app

def run_workflow():
    print("\n=== New Ticket ===")
    print("Enter a new support ticket:")
    print("Ticket text (press Ctrl+D or Ctrl+Z then Enter to finish):")
    lines = sys.stdin.readlines()
    ticket = "".join(lines).strip()
    
    if not ticket:
        print("\nNo ticket text provided.")
        return

    name = input("Customer name (optional): ").strip()
    email = input("Customer email (optional): ").strip()

    # Initialize the state for the entire workflow as a plain dict
    current_state = {
        "ticket": ticket,
        "name": name,
        "email": email,
    }

    # The main loop for the graph execution and human approval
    while True:
        print(f"\nDEBUG: Invoking graph with state keys: {list(current_state.keys())}")
        # Pass the full current state to the graph
        result = triage_app.invoke(current_state)
        # The result is the new, complete state. Replace local copy.
        current_state = result or {}

        # If the graph is no longer awaiting approval, the workflow is complete.
        if not current_state.get("awaiting_approval"):
            print("\n=== Workflow Complete ===")
            print(f"Final Reply:\n---\n{current_state.get('draft_reply', 'No reply generated.')}")
            break

        # --- Human-in-the-loop --- #
        print("\n=== Approval Required ===")
        print(f"Draft Reply:\n---\n{current_state.get('draft_reply','')}\n---")
        
        decision = input("Approve, Revise, or Quit? (a/r/q): ").strip().lower()

        if decision == 'a':
            # Set the decision and turn off the approval flag to continue the graph
            current_state["approval_decision"] = "approve"
            current_state["awaiting_approval"] = False
        elif decision == 'r':
            feedback = input("Revision feedback: ").strip()
            # Set the decision and feedback to route to the 'revise' node
            current_state["reviewer_feedback"] = feedback
            current_state["approval_decision"] = "revise"
            current_state["awaiting_approval"] = False
        else:
            print("Exiting workflow.")
            break

def main():
    while True:
        run_workflow()
        again = input("\nProcess another ticket? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
