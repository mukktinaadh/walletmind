from typing import Dict, Any, Tuple

def compute_credit_score(features: Dict[str, Any], graph_metrics: Dict[str, float]) -> Dict[str, Any]:
    """
    Compute V3 credit score based on behavioral features and network graph metrics.
    Score range: 0-1000
    """
    
    tx_count = features.get("transaction_count", 0)
    total_volume = features.get("total_volume", 0.0)
    diversity_score = features.get("counterparty_diversity_score", 0.0)
    entropy = features.get("counterparty_entropy", 0.0)
    reuse_ratio = features.get("counterparty_reuse_ratio", 0.0)
    exchange_count = features.get("exchange_interaction_count", 0)
    defi_count = features.get("defi_interaction_count", 0)
    stablecoin_ratio = features.get("stablecoin_ratio", 0.0)
    wallet_age_days = features.get("wallet_age_days", 0.0)
    
    clustering = graph_metrics.get("clustering_coefficient", 0.0)
    centrality = graph_metrics.get("degree_centrality", 0.0)
    
    # Calculate V3 weighted scores
    
    # 1. Activity (max 200): Mix of raw tx count and exchange interaction validation
    activity_base = min(tx_count / 500.0, 1.0) * 150
    exchange_bonus = min(exchange_count / 10.0, 1.0) * 50
    activity_score = int(activity_base + exchange_bonus)
    
    # 2. Volume (max 150)
    volume_score = int(min(total_volume / 100.0, 1.0) * 150)
    
    # 3. Diversity & Behavior (max 200): High entropy and healthy reuse means good behavior
    diversity_base = min(diversity_score, 1.0) * 100
    entropy_bonus = min(entropy / 5.0, 1.0) * 50
    reuse_bonus = min(reuse_ratio / 0.5, 1.0) * 50
    diversity_final = int(diversity_base + entropy_bonus + reuse_bonus)
    
    # 4. Stability & DeFi (max 150)
    stability_base = min(stablecoin_ratio, 1.0) * 100
    defi_bonus = min(defi_count / 20.0, 1.0) * 50
    stability_score = int(stability_base + defi_bonus)
    
    # 5. Network (max 200): Based on graph centrality and clustering
    network_base = min(centrality / 0.1, 1.0) * 100
    clustering_bonus = min(clustering / 0.5, 1.0) * 100
    network_score = int(network_base + clustering_bonus)
    
    # 6. Age (max 100)
    age_score = int(min(wallet_age_days / 365.0, 1.0) * 100)
    
    raw_score = sum([activity_score, volume_score, diversity_final, stability_score, network_score, age_score])
    final_score = max(0, min(1000, raw_score))
    
    # Determine risk level
    if final_score >= 800:
        risk_level = "low"
    elif final_score >= 500:
        risk_level = "medium"
    else:
        risk_level = "high"
        
    return {
        "credit_score": final_score,
        "risk_level": risk_level,
        "score_breakdown": {
            "activity_score": activity_score,
            "volume_score": volume_score,
            "diversity_score": diversity_final,
            "stability_score": stability_score,
            "defi_score": int(defi_bonus),
            "age_score": age_score,
            "network_score": network_score
        }
    }
