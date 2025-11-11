from web3 import Web3
from web3.exceptions import TransactionNotFound
from config import INFURA_URL
import sys

# --- Initialize the Web3 Connection ---
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def get_transaction_data(txn_hash: str) -> dict | None:
    """
    Fetches real transaction data from the blockchain using a hash.
    This is now engineered to match the CSV-trained model features.
    """
    print(f"Fetching data for {txn_hash} from Infura...", file=sys.stderr)
    try:
        # 1. Get the main transaction details
        txn = w3.eth.get_transaction(txn_hash)
        
        # 2. Get the transaction "receipt"
        receipt = w3.eth.get_transaction_receipt(txn_hash)

        # --- Feature Engineering (to match the model) ---
        
        # Feature 1: 'Value'
        value_ether = w3.from_wei(txn['value'], 'ether')
        
        # Feature 2: 'input_data_length'
        input_len = len(txn['input'].hex().replace('0x', ''))

        # Feature 3: 'is_contract_interaction'
        # The receipt has a 'contractAddress' field if one was created.
        # We also check if the 'to' address is a known contract (has code).
        is_contract = False
        if receipt['contractAddress']:
            is_contract = True # It created a contract
        elif txn['to']:
            # Check if the 'to' address has code (is a contract)
            code = w3.eth.get_code(txn['to'])
            if len(code) > 0:
                is_contract = True # It's an interaction with an existing contract
        
        is_contract_int = 1 if is_contract else 0
        
        # --- Bundle features for the predictor ---
        features = {
            "hash": txn_hash,
            "from": txn['from'],
            "to": txn['to'],
            
            # These MUST match the training features
            "Value": value_ether,
            "input_data_length": input_len,
            "is_contract_interaction": is_contract_int,
            
            # Other data for the rules engine
            "from_account_txn_count": w3.eth.get_transaction_count(txn['from']),
            "status": receipt['status']
        }
        
        print(f"Successfully fetched data for {txn_hash}", file=sys.stderr)
        return features

    except TransactionNotFound:
        print(f"Error: Transaction hash {txn_hash} not found.", file=sys.stderr)
        return {"error": "Transaction not found"}
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        if "project id" in str(e).lower():
            return {"error": "Invalid or missing Infura Project ID in config.py"}
        return {"error": str(e)}