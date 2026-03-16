from typing import Dict, Any

def generate_explanation(score: int, risk_level: str, features: Dict[str, Any], graph_metrics: Dict[str, float]) -> str:
    """
    Generate a concise V3 explanation referencing actual metrics from features and graph analysis.
    """
    tx_count = features.get("transaction_count", 0)
    counterparties = features.get("unique_counterparties", 0)
    wallet_age_years = features.get("wallet_age_days", 0.0) / 365.0
    stablecoin_ratio = features.get("stablecoin_ratio", 0.0)
    defi_interaction_count = features.get("defi_interaction_count", 0)
    clustering = graph_metrics.get("clustering_coefficient", 0.0)
    
    if tx_count == 0:
        return "This wallet has no transaction history, resulting in a low credit score and high risk level."
        
    stablecoin_desc = "Strong" if stablecoin_ratio > 0.5 else "Moderate" if stablecoin_ratio > 0.1 else "Limited"
    defi_desc = "high" if defi_interaction_count > 20 else "moderate" if defi_interaction_count > 5 else "low"
    
    clustering_desc = "high clustering" if clustering > 0.3 else "moderate connectivity" if clustering > 0.1 else "low clustering"
    behavior_desc = "organic behavior" if clustering <= 0.3 else "potential bot clusters or tightly knit network activity"
    
    activity_desc = "strong activity" if tx_count > 100 else "moderate activity" if tx_count > 20 else "limited activity"
    
    return f"This wallet has {activity_desc} with {tx_count} transactions across {counterparties} counterparties and a wallet age of {wallet_age_years:.1f} years. Network graph analysis shows {clustering_desc}, indicating {behavior_desc}. {stablecoin_desc} stablecoin usage and {defi_desc} DeFi interaction contribute to the {risk_level} risk rating."
