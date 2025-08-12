def approval_node(state: dict) -> dict:
    print(f"\n=== approval_node ===")
    print(f"Input state keys: {list(state.keys())}")

    draft_reply = state.get("draft_reply", "")
    if not draft_reply or "Error:" in draft_reply:
        print("WARNING: No valid draft reply to approve. Bypassing approval.")
        # Set a decision that leads to the end, as there's nothing to approve.
        return {"approval_decision": "approve"}

    print("Draft is ready for review. Setting 'awaiting_approval' to True.")
    # This flag signals the CLI to pause and ask for user input.
    return {"awaiting_approval": True}
