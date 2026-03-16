import time
import requests
from typing import List, Dict, Any
from api.config import settings

def fetch_wallet_transactions(wallet_address: str) -> List[Dict[str, Any]]:
    """
    Fetch Ethereum wallet transaction history.
    Uses Etherscan API. Falls back to mock data if API key is missing or request fails.
    """
    if not wallet_address:
        raise ValueError("Wallet address cannot be empty")
        
    api_key = settings.ETHERSCAN_API_KEY
    if api_key:
        url = "https://api.etherscan.io/v2/api"
        params = {
            "chainid": 1,
            "module": "account",
            "action": "txlist",
            "address": wallet_address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": 500,
            "sort": "desc",
            "apikey": api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                message = data.get("message", "")
                result = data.get("result", [])
                
                if status == "1":
                    return _normalize_transactions(result)
                elif status == "0" and "No transactions found" in message:
                    return []
                elif status == "0" and "rate limit" in str(result).lower():
                    raise RuntimeError("Etherscan API rate limit exceeded")
                elif status == "0" and "Invalid Address" in result:
                    raise ValueError("Invalid wallet address format")
                else:
                    raise RuntimeError(f"Etherscan error: {result}")
            else:
                raise RuntimeError(f"HTTP {response.status_code} from Etherscan")
        except requests.Timeout:
            raise RuntimeError("Blockchain API timeout")
        except requests.RequestException as e:
            raise RuntimeError(f"Network error: {str(e)}")
            
    # Fallback to mock data only if NO api key was configured
    return _generate_mock_transactions(wallet_address)

def _normalize_transactions(raw_txs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize required fields from Etherscan response."""
    normalized = []
    for tx in raw_txs:
        normalized.append({
            "from": tx.get("from", ""),
            "to": tx.get("to", ""),
            "value": tx.get("value", "0"),
            "timestamp": tx.get("timeStamp", "")
        })
    return normalized

def _generate_mock_transactions(wallet_address: str) -> List[Dict[str, Any]]:
    """Generate mock transactions for fallback."""
    current_time = int(time.time())
    
    # Generate deterministic but realistic looking mock data based on address length
    num_txs = 10 + (len(wallet_address) % 40)
    
    mock_txs = []
    for i in range(num_txs):
        is_outgoing = i % 2 == 0
        from_addr = wallet_address if is_outgoing else f"0xmocksender{i}abcdef"
        to_addr = f"0xmockreceiver{i}abcdef" if is_outgoing else wallet_address
        
        # Value in wei (simulate varying amounts)
        value_eth = (i * 0.1) + 0.05
        value_wei = str(int(value_eth * 10**18))
        
        mock_txs.append({
            "from": from_addr,
            "to": to_addr,
            "value": value_wei,
            "timestamp": str(current_time - (i * 86400))  # 1 day apart
        })
        
    return mock_txs
