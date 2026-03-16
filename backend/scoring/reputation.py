from typing import Dict, Any, Tuple

def compute_wallet_reputation(features: Dict[str, Any], graph_metrics: Dict[str, float]) -> Dict[str, Any]:
    """
    Compute Wallet Reputation Score (0-100) based on on-chain behavior and network metrics.
    """
    
    age_days = features.get("wallet_age_days", 0.0)
    reuse_ratio = features.get("counterparty_reuse_ratio", 0.0)
    entropy = features.get("counterparty_entropy", 0.0)
    stablecoin_ratio = features.get("stablecoin_ratio", 0.0)
    exchange_count = features.get("exchange_interaction_count", 0)
    clustering = graph_metrics.get("clustering_coefficient", 0.0)
    
    # 1. Age Weight (max 20)
    age_score = min(age_days / 365.0, 1.0) * 20
    
    # 2. Network/Clustering Weight (max 30): High clustering might indicate bot/sybil behavior, lower is generally better for organic retail
    # If clustering is very high (>0.5), we heavily penalize it.
    network_score = max(0, (1.0 - (clustering * 1.5))) * 30
    
    # 3. Stability Weight (max 20)
    stability_score = min(stablecoin_ratio, 1.0) * 20
    
    # 4. Activity/Behavior Weight (max 30): Rewards healthy counterparty diversity and explicit, verified exchange checkpoints
    entropy_score = min(entropy / 5.0, 1.0) * 10
    reuse_score = min(reuse_ratio / 0.8, 1.0) * 10
    exchange_score = min(exchange_count / 5.0, 1.0) * 10
    activity_score = entropy_score + reuse_score + exchange_score
    
    raw_reputation = sum([age_score, network_score, stability_score, activity_score])
    reputation_score = int(max(0, min(100, raw_reputation)))
    
    # Assign Level
    if reputation_score >= 70:
        level = "trusted"
    elif reputation_score >= 40:
        level = "neutral"
    else:
        level = "risky"
        
    return {
        "reputation_score": reputation_score,
        "reputation_level": level
    }
