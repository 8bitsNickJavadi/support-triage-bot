def retrieve_node(state: dict) -> dict:
    print(f"\n=== retrieve_node ===")
    print(f"Input state keys: {list(state.keys())}")

    retriever = state.get("faq_retriever")
    ticket = state.get("ticket", "")

    if not retriever or not ticket:
        print("ERROR: Missing retriever or ticket in state. Skipping FAQ retrieval.")
        return {"faq_passages": []}

    try:
        docs = retriever.get_relevant_documents(ticket)
        passages = [d.page_content for d in docs]
        print(f"Retrieved {len(passages)} FAQ passages.")
        return {"faq_passages": passages}
    except Exception as e:
        print(f"Error during FAQ retrieval: {str(e)}")
        return {"faq_passages": []}
