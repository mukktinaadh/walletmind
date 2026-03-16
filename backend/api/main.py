from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models import WalletAnalysisRequest, WalletAnalysisResponse, WalletFeatures, GraphMetrics, CreditCapacity
from blockchain.data_fetcher import fetch_wallet_transactions
from scoring.features import extract_features
from scoring.model import compute_credit_score
from scoring.network_graph import compute_graph_metrics
from scoring.credit_capacity import estimate_credit_capacity
from scoring.reputation import compute_wallet_reputation
from scoring.risk_flags import detect_risk_flags
from ai.explanations import generate_explanation

app = FastAPI(title="WalletMind API", description="V4 API for analyzing wallet behavior", version="4.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/analyze-wallet", response_model=WalletAnalysisResponse)
def analyze_wallet(request: WalletAnalysisRequest):
    """
    Analyze an Ethereum wallet address and return a credit score, risk level, graph metrics, capacity and explanation.
    """
    wallet_address = request.wallet_address.strip()
    if not wallet_address:
        raise HTTPException(status_code=400, detail="Invalid wallet address provided")
        
    try:
        # Step 1: Fetch transactions
        transactions = fetch_wallet_transactions(wallet_address)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Blockchain API failure: {str(e)}")
        
    try:
        # Step 2: Extract features
        features = extract_features(transactions)
        
        # Step 3: Compute graph metrics
        graph_metrics = compute_graph_metrics(transactions, wallet_address)
        
        # Step 4: Compute credit score
        score_data = compute_credit_score(features, graph_metrics)
        credit_score = score_data["credit_score"]
        risk_level = score_data["risk_level"]
        
        # Step 5: Compute V4 Reputation & Risk Flags
        reputation_data = compute_wallet_reputation(features, graph_metrics)
        reputation_score = reputation_data["reputation_score"]
        reputation_level = reputation_data["reputation_level"]
        
        risk_flags = detect_risk_flags(features, graph_metrics)
        
        # Step 6: Estimate credit capacity (V4 includes reputation and graph density)
        capacity_data = estimate_credit_capacity(
            credit_score=credit_score,
            wallet_age_days=features.get("wallet_age_days", 0.0),
            total_volume=features.get("total_volume", 0.0),
            counterparty_diversity_score=features.get("counterparty_diversity_score", 0.0),
            stablecoin_ratio=features.get("stablecoin_ratio", 0.0),
            reputation_score=reputation_score,
            graph_density=graph_metrics.get("network_density", 0.0)
        )
        
        # Step 7: Generate explanation
        explanation = generate_explanation(credit_score, risk_level, features, graph_metrics)
        
        # Prepare response
        return WalletAnalysisResponse(
            wallet_address=wallet_address,
            credit_score=credit_score,
            reputation_score=reputation_score,
            risk_level=risk_level,
            reputation_level=reputation_level,
            features=WalletFeatures(**features),
            score_breakdown=score_data["score_breakdown"],
            graph_metrics=GraphMetrics(**graph_metrics),
            risk_flags=risk_flags,
            credit_capacity=CreditCapacity(**capacity_data),
            explanation=explanation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during analysis: {str(e)}")
