from typing import Dict, Any

def estimate_credit_capacity(
    credit_score: int,
    wallet_age_days: float,
    total_volume: float,
    counterparty_diversity_score: float,
    stablecoin_ratio: float,
    reputation_score: int,
    graph_density: float
) -> Dict[str, float]:
    """
    Estimate safe lending capacity based on V4 logic.
    Output: recommended_credit_limit, liquidation_risk, underwriting_confidence
    """
    
    base_limit = total_volume * 0.05
    risk_adjustment = credit_score / 1000.0
    
    recommended_credit_limit = base_limit * risk_adjustment
    liquidation_risk = 1.0 - risk_adjustment
    
    # Underwriting confidence (V4 signal) using reputation and graph density
    confidence = (reputation_score / 100.0)
    
    return {
        "recommended_credit_limit": float(f"{recommended_credit_limit:.2f}"),
        "liquidation_risk": float(f"{liquidation_risk:.4f}"),
        "underwriting_confidence": float(f"{confidence:.4f}")
    }
