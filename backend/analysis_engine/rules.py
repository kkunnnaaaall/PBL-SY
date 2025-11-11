from .blockchain_fetcher import get_transaction_data

# A real, known phishing address (the "Fake_Phishing1" from Etherscan)
KNOWN_PHISHING_ADDRESSES = {
    "0x0000111112222233333444445555566666777777": "Fake_Phishing1",
    "0xb3dAaA19D1111C52C3eF73d23255639F65B0A037": "Fake_Phishing_Finteria",
    # You would add more known addresses to this list
}

def check_rules(txn_hash: str) -> dict | None:
    """
    Checks a transaction against a set of hard-coded rules using real data.
    """
    # 1. Get the real transaction data
    data = get_transaction_data(txn_hash)

    # 1a. Handle errors from the fetcher
    if not data or data.get("error"):
        return {"status": "ERROR", "reason": data.get("error", "Failed to fetch data")}

    # --- Rule 1: Check against known address list ---
    if data['to'] in KNOWN_PHISHING_ADDRESSES:
        return {
            "status": "PHISHING",
            "reason": f"Transaction 'to' address matches known phishing list: {KNOWN_PHISHING_ADDRESSES[data['to']]}"
        }
    if data['from'] in KNOWN_PHISHING_ADDRESSES:
         return {
            "status": "PHISHING",
            "reason": f"Transaction 'from' address matches known phishing list: {KNOWN_PHISHING_ADDRESSES[data['from']]}"
        }

    # --- Rule 2: Zero-value transfer to a brand new account ---
    # This is a common pattern for "address poisoning" scams
    
    # ***** THIS IS THE LINE I FIXED *****
    if data['Value'] == 0 and data['from_account_txn_count'] < 2:
    # ***** WAS 'value', NOW 'Value' *****
    
        return {
            "status": "PHISHING",
            "reason": "Detected zero-value transfer from a new account (Address Poisoning Pattern)"
        }

    # --- Rule 3: Transaction failed ---
    # Many scam transactions fail because the contract logic is bad
    if data['status'] == 0:
        return {
            "status": "PHISHING",
            "reason": "Transaction failed. This is a common indicator for scam contract interactions."
        }

    # If no rules are matched, return None
    return None