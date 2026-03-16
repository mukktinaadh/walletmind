from typing import Dict, Any, List

def detect_risk_flags(features: Dict[str, Any], graph_metrics: Dict[str, float]) -> List[str]:
    """
    Detect risk flags (fraud signals) based on behavioral heuritsics and graph shape.
    """
    
    flags = []
    
    # 1. High velocity transfers (many transactions in very short timespan proxy via high volume vs low age)
    tx_count = features.get("transaction_count", 0)
    age_days = features.get("wallet_age_days", 0.0)
    
    if tx_count > 100 and age_days < 7.0:
        flags.append("high_velocity_transfers")
        
    # 2. Large Number of Unique Counterparties (Scattershot)
    unique_counterparties = features.get("unique_counterparties", 0)
    if unique_counterparties > 100 and (features.get("counterparty_reuse_ratio", 0.0) < 0.1):
        flags.append("abnormal_counterparty_spread")
        
    # 3. Sudden spikes in volume (Proxy via average size vs total)
    avg_size = features.get("average_transaction_size", 0.0)
    high_value = features.get("high_value_transactions", 0)
    if high_value > 10 and avg_size > 10.0:
        flags.append("sudden_volume_spikes")
        
    # 4. Extremely dense graph clusters (Bot ring/Sybil detection)
    clustering = graph_metrics.get("clustering_coefficient", 0.0)
    density = graph_metrics.get("network_density", 0.0)
    
    if clustering > 0.4 and density > 0.2:
        flags.append("suspicious_network_cluster")
        
    # 5. Wash trading signal (High tx, low unique counterparties, high reuse)
    reuse = features.get("counterparty_reuse_ratio", 0.0)
    if tx_count > 50 and reuse > 0.8:
        flags.append("potential_wash_trading")
        
    return flags
