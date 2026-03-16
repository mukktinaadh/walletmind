import time
import math
from typing import List, Dict, Any

DEFI_CONTRACTS = {
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d", # Uniswap V2 Router
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45", # Uniswap V3 Router
    "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9", # Aave V2
    "0x87870bca3f3fd6335c3f4ce8392d69350b4fa4e2", # Aave V3
    "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5", # Compound cETH
    "0xdc24316b9ae028f1497c275eb9192a3ea0f67022", # Curve stETH
    "0xba12222222228d8ba445958a75a0704d566bf2c8", # Balancer Vault
}

STABLECOIN_CONTRACTS = {
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", # USDC
    "0xdac17f958d2ee523a2206206994597c13d831ec7", # USDT
    "0x6b175474e89094c44da98b954eedeac495271d0f", # DAI
}

EXCHANGE_CONTRACTS = {
    "0x28c6c06298d514db089934071355e22af16ababf", # Binance 14
    "0x503828976d22510aad0201ac7ec88293211d23da", # Coinbase
    "0x267be1c1d684ffcb8bc992224cb5d40ee3cb2ab1", # Kraken
    "0x5f65f7b609678448494de4c87521cdf6cef1e932", # Gemini
    "0x6cc5f688a315f3dc28a7781717a9a798a59fda7b", # OKX
}

def extract_features(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    HIGH_VALUE_THRESHOLD_ETH = 1.0
    WEI_TO_ETH = 10**18
    
    transaction_count = len(transactions)
    
    if transaction_count == 0:
        return {
            "transaction_count": 0,
            "unique_counterparties": 0,
            "total_volume": 0.0,
            "average_transaction_size": 0.0,
            "high_value_transactions": 0,
            "wallet_age_days": 0.0,
            "defi_interaction_count": 0,
            "counterparty_diversity_score": 0.0,
            "stablecoin_ratio": 0.0,
            "counterparty_reuse_ratio": 0.0,
            "counterparty_entropy": 0.0,
            "exchange_interaction_count": 0
        }
        
    counterparty_counts = {}
    total_volume_eth = 0.0
    high_value_tx_count = 0
    stablecoin_volume = 0.0
    defi_interaction_count = 0
    exchange_interaction_count = 0
    
    earliest_timestamp = float('inf')
    
    for tx in transactions:
        from_addr = tx.get("from", "").lower()
        to_addr = tx.get("to", "").lower()
        
        # Track counterparty interaction frequencies
        if from_addr:
            counterparty_counts[from_addr] = counterparty_counts.get(from_addr, 0) + 1
        if to_addr:
            counterparty_counts[to_addr] = counterparty_counts.get(to_addr, 0) + 1
            
        try:
            value_wei = float(tx.get("value", "0"))
            value_eth = value_wei / WEI_TO_ETH
        except ValueError:
            value_eth = 0.0
            
        total_volume_eth += value_eth
        
        if value_eth > HIGH_VALUE_THRESHOLD_ETH:
            high_value_tx_count += 1
            
        # DeFi detection
        if to_addr in DEFI_CONTRACTS or from_addr in DEFI_CONTRACTS:
            defi_interaction_count += 1
            
        # Exchange detection
        if to_addr in EXCHANGE_CONTRACTS or from_addr in EXCHANGE_CONTRACTS:
            exchange_interaction_count += 1
            
        # Stablecoin detection
        if to_addr in STABLECOIN_CONTRACTS or from_addr in STABLECOIN_CONTRACTS:
            stablecoin_volume += max(value_eth, 0.0) 
            if value_eth == 0:
                stablecoin_volume += 1.0
                total_volume_eth += 1.0
                
        # Timestamp for wallet age
        try:
            ts = int(tx.get("timestamp", "0"))
            if ts > 0 and ts < earliest_timestamp:
                earliest_timestamp = ts
        except ValueError:
            pass
            
    average_tx_size = total_volume_eth / transaction_count if transaction_count > 0 else 0.0
    
    # Counterparty metrics
    unique_counterparties = len(counterparty_counts)
    counterparty_diversity_score = unique_counterparties / transaction_count if transaction_count > 0 else 0.0
    
    repeat_interactions = transaction_count - unique_counterparties
    counterparty_reuse_ratio = max(0.0, repeat_interactions / transaction_count) if transaction_count > 0 else 0.0
    
    # Counterparty Entropy
    entropy = 0.0
    total_interactions = sum(counterparty_counts.values())
    if total_interactions > 0:
        for count in counterparty_counts.values():
            p = count / total_interactions
            entropy -= p * math.log2(p)
    
    wallet_age_days = 0.0
    if earliest_timestamp != float('inf'):
        wallet_age_days = (time.time() - earliest_timestamp) / 86400.0
        
    stablecoin_ratio = stablecoin_volume / total_volume_eth if total_volume_eth > 0 else 0.0
    
    return {
        "transaction_count": transaction_count,
        "unique_counterparties": unique_counterparties,
        "total_volume": round(total_volume_eth, 4),
        "average_transaction_size": round(average_tx_size, 4),
        "high_value_transactions": high_value_tx_count,
        "wallet_age_days": round(max(0.0, wallet_age_days), 2),
        "defi_interaction_count": defi_interaction_count,
        "counterparty_diversity_score": round(counterparty_diversity_score, 4),
        "stablecoin_ratio": round(min(1.0, stablecoin_ratio), 4),
        "counterparty_reuse_ratio": round(counterparty_reuse_ratio, 4),
        "counterparty_entropy": round(entropy, 4),
        "exchange_interaction_count": exchange_interaction_count
    }
