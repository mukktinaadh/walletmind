from pydantic import BaseModel
from typing import Dict, Any

class WalletAnalysisRequest(BaseModel):
    wallet_address: str

class WalletFeatures(BaseModel):
    transaction_count: int
    unique_counterparties: int
    total_volume: float
    average_transaction_size: float
    high_value_transactions: int
    wallet_age_days: float
    defi_interaction_count: int
    counterparty_diversity_score: float
    stablecoin_ratio: float
    counterparty_reuse_ratio: float
    counterparty_entropy: float
    exchange_interaction_count: int

class ScoreBreakdown(BaseModel):
    activity_score: int
    volume_score: int
    diversity_score: int
    stability_score: int
    defi_score: int
    age_score: int
    network_score: int

class GraphMetrics(BaseModel):
    degree_centrality: float
    clustering_coefficient: float
    network_density: float
    cluster_count: int
    largest_cluster_size: int

class CreditCapacity(BaseModel):
    recommended_credit_limit: float
    liquidation_risk: float
    underwriting_confidence: float

from typing import Dict, Any, List

class WalletAnalysisResponse(BaseModel):
    wallet_address: str
    credit_score: int
    reputation_score: int
    risk_level: str
    reputation_level: str
    features: WalletFeatures
    score_breakdown: ScoreBreakdown
    graph_metrics: GraphMetrics
    risk_flags: List[str]
    credit_capacity: CreditCapacity
    explanation: str
