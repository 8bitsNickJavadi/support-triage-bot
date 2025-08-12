import pandas as pd

try:
    CUSTOMERS = pd.read_csv("data/customers.csv")
except FileNotFoundError:
    print("ERROR: data/customers.csv not found. Enrich node will be skipped.")
    CUSTOMERS = pd.DataFrame()

def enrich_node(state: dict) -> dict:
    print(f"\n=== enrich_node ===")
    print(f"Input state keys: {list(state.keys())}")

    if CUSTOMERS.empty:
        return {"customer_record": {}}

    email = state.get("email", "").strip().lower()
    name = state.get("name", "").strip().lower()
    match = pd.DataFrame()

    if email:
        match = CUSTOMERS[CUSTOMERS["email"].str.lower() == email]
    if match.empty and name:
        # A simple partial match for demonstration
        match = CUSTOMERS[CUSTOMERS["name"].str.lower().str.contains(name)]

    if not match.empty:
        customer_record = match.to_dict(orient="records")[0]
        print(f"Found customer record: {customer_record}")
        return {"customer_record": customer_record}
    else:
        print("No customer record found.")
        return {"customer_record": {}}
