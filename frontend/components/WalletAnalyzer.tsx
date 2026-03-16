"use client";

import { useState } from "react";
import { Search, Activity, AlertTriangle, ShieldCheck } from "lucide-react";

type AnalysisResult = {
    wallet_address: string;
    credit_score: number;
    reputation_score: number;
    risk_level: "low" | "medium" | "high";
    reputation_level: "trusted" | "neutral" | "risky";
    risk_flags: string[];
    features: {
        transaction_count: number;
        unique_counterparties: number;
        total_volume: number;
        average_transaction_size: number;
        high_value_transactions: number;
        wallet_age_days: number;
    };
    score_breakdown: {
        activity_score: number;
        volume_score: number;
        diversity_score: number;
        stability_score: number;
        defi_score: number;
        age_score: number;
        network_score: number;
    };
    graph_metrics: {
        degree_centrality: number;
        clustering_coefficient: number;
        network_density: number;
        cluster_count: number;
        largest_cluster_size: number;
    };
    credit_capacity: {
        recommended_credit_limit: number;
        liquidation_risk: number;
        underwriting_confidence: number;
    };
    explanation: string;
};

export default function WalletAnalyzer() {
    const [address, setAddress] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const analyzeWallet = async () => {
        if (!address.trim()) {
            setError("Please enter a valid wallet address.");
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const response = await fetch(`${apiUrl}/analyze-wallet`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ wallet_address: address }),
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => null);
                throw new Error(errData?.detail || "Failed to analyze wallet. The backend might be unreachable.");
            }

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (level: string) => {
        switch (level) {
            case "low":
            case "trusted":
                return "text-green-500 bg-green-500/10 border-green-500/20";
            case "medium":
            case "neutral":
                return "text-yellow-500 bg-yellow-500/10 border-yellow-500/20";
            case "high":
            case "risky":
                return "text-red-500 bg-red-500/10 border-red-500/20";
            default:
                return "text-gray-500 bg-gray-500/10 border-gray-500/20";
        }
    };

    const getRiskIcon = (level: string) => {
        switch (level) {
            case "low":
                return <ShieldCheck className="w-5 h-5 text-green-500" />;
            case "medium":
                return <Activity className="w-5 h-5 text-yellow-500" />;
            case "high":
                return <AlertTriangle className="w-5 h-5 text-red-500" />;
            default:
                return null;
        }
    };

    return (
        <div className="w-full max-w-2xl mx-auto space-y-6">
            {/* Search Bar */}
            <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative flex-1">
                    <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
                        <Search className="w-5 h-5 text-gray-400" />
                    </div>
                    <input
                        type="text"
                        className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-white placeholder-gray-500 transition-all font-mono"
                        placeholder="Enter Ethereum 0x..."
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && analyzeWallet()}
                    />
                </div>
                <button
                    onClick={analyzeWallet}
                    disabled={loading}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[120px]"
                >
                    {loading ? (
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                        "Analyze"
                    )}
                </button>
            </div>

            {/* Error Message */}
            {error && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
                    <p className="text-sm">{error}</p>
                </div>
            )}

            {/* Analysis Results */}
            {result && (
                <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Score Card */}
                        <div className="p-6 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center justify-center space-y-2">
                            <span className="text-sm text-gray-400 uppercase tracking-wider font-semibold">Credit Score</span>
                            <div className="text-5xl font-bold font-mono text-white">
                                {result.credit_score}
                                <span className="text-xl text-gray-500">/1000</span>
                            </div>
                        </div>

                        {/* Reputation Card */}
                        <div className={`p-6 rounded-2xl border flex flex-col items-center justify-center space-y-3 ${getRiskColor(result.reputation_level)}`}>
                            <span className="text-sm uppercase tracking-wider font-semibold opacity-80">Reputation</span>
                            <div className="text-4xl font-bold font-mono">
                                {result.reputation_score}
                                <span className="text-lg opacity-60">/100</span>
                            </div>
                        </div>

                        {/* Risk Level Card */}
                        <div className={`p-6 rounded-2xl border flex flex-col items-center justify-center space-y-3 ${getRiskColor(result.risk_level)}`}>
                            <span className="text-sm uppercase tracking-wider font-semibold opacity-80">Risk Level</span>
                            <div className="flex items-center gap-2">
                                {getRiskIcon(result.risk_level)}
                                <span className="text-3xl font-bold capitalize">{result.risk_level}</span>
                            </div>
                        </div>
                    </div>

                    {/* Risk Flags */}
                    {result.risk_flags.length > 0 && (
                        <div className="p-5 rounded-xl bg-red-500/10 border border-red-500/20 flex flex-col space-y-3">
                            <div className="flex items-center gap-2 text-red-400 font-semibold mb-2">
                                <AlertTriangle className="w-5 h-5" />
                                <span>Fraud & Risk Signals Detected</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {result.risk_flags.map((flag, idx) => (
                                    <span key={idx} className="px-3 py-1 bg-red-500/20 text-red-300 rounded-full text-xs font-mono uppercase tracking-widest">{flag.replace(/_/g, " ")}</span>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Credit Capacity */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="p-5 rounded-xl bg-white/5 border border-white/10 flex flex-col gap-2">
                            <span className="text-gray-400 font-medium text-xs uppercase tracking-wider">Rec. Credit Limit</span>
                            <span className="text-2xl font-bold text-blue-400 font-mono">
                                {result.credit_capacity.recommended_credit_limit.toFixed(2)} ETH
                            </span>
                        </div>
                        <div className="p-5 rounded-xl bg-white/5 border border-white/10 flex flex-col gap-2">
                            <span className="text-gray-400 font-medium text-xs uppercase tracking-wider">Liquidation Risk</span>
                            <span className={`text-2xl font-bold font-mono ${result.credit_capacity.liquidation_risk > 0.5 ? 'text-red-400' : 'text-green-400'}`}>
                                {(result.credit_capacity.liquidation_risk * 100).toFixed(1)}%
                            </span>
                        </div>
                        <div className="p-5 rounded-xl bg-white/5 border border-white/10 flex flex-col gap-2">
                            <span className="text-gray-400 font-medium text-xs uppercase tracking-wider">UW Confidence</span>
                            <span className={`text-2xl font-bold font-mono ${result.credit_capacity.underwriting_confidence < 0.5 ? 'text-yellow-500' : 'text-green-500'}`}>
                                {(result.credit_capacity.underwriting_confidence * 100).toFixed(1)}%
                            </span>
                        </div>
                    </div>

                    {/* Explanation */}
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10 space-y-3">
                        <h3 className="text-lg font-semibold text-white">AI Analysis</h3>
                        <p className="text-gray-300 leading-relaxed">{result.explanation}</p>
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                            <div className="text-xs text-gray-400 mb-1">Transactions</div>
                            <div className="text-lg font-semibold text-white font-mono">{result.features.transaction_count}</div>
                        </div>
                        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                            <div className="text-xs text-gray-400 mb-1">Volume (ETH)</div>
                            <div className="text-lg font-semibold text-white font-mono">{result.features.total_volume}</div>
                        </div>
                        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                            <div className="text-xs text-gray-400 mb-1">Counterparties</div>
                            <div className="text-lg font-semibold text-white font-mono">{result.features.unique_counterparties}</div>
                        </div>
                        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                            <div className="text-xs text-gray-400 mb-1">Age (Years)</div>
                            <div className="text-lg font-semibold text-white font-mono">{(result.features.wallet_age_days / 365).toFixed(1)}</div>
                        </div>
                    </div>

                    {/* Graph Metrics */}
                    <div className="p-5 rounded-2xl bg-white/5 border border-white/10">
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Network Cluster & Proximity</h3>
                        <div className="grid grid-cols-5 gap-2 text-center items-center">
                            <div>
                                <div className="text-xs text-gray-500 mb-1">Clustering</div>
                                <div className="text-md font-medium text-white font-mono">{result.graph_metrics.clustering_coefficient.toFixed(3)}</div>
                            </div>
                            <div>
                                <div className="text-xs text-gray-500 mb-1">Density</div>
                                <div className="text-md font-medium text-white font-mono">{result.graph_metrics.network_density.toFixed(3)}</div>
                            </div>
                            <div>
                                <div className="text-xs text-gray-500 mb-1">Centrality</div>
                                <div className="text-md font-medium text-white font-mono">{result.graph_metrics.degree_centrality.toFixed(3)}</div>
                            </div>
                            <div className="border-l border-white/10 pl-2">
                                <div className="text-xs text-gray-500 mb-1">Communities</div>
                                <div className="text-md font-medium text-blue-400 font-mono">{result.graph_metrics.cluster_count}</div>
                            </div>
                            <div>
                                <div className="text-xs text-gray-500 mb-1">Largest Ring</div>
                                <div className="text-md font-medium text-blue-400 font-mono">{result.graph_metrics.largest_cluster_size}</div>
                            </div>
                        </div>
                    </div>

                    {/* Score Breakdown */}
                    <div className="p-5 rounded-2xl bg-white/5 border border-white/10">
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Score Breakdown</h3>
                        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">Activity</span><span className="text-white font-mono">{result.score_breakdown.activity_score}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">Volume</span><span className="text-white font-mono">{result.score_breakdown.volume_score}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">Diversity</span><span className="text-white font-mono">{result.score_breakdown.diversity_score}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">Stability</span><span className="text-white font-mono">{result.score_breakdown.stability_score}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">DeFi</span><span className="text-white font-mono">{result.score_breakdown.defi_score}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">Network</span><span className="text-white font-mono">{result.score_breakdown.network_score}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1">
                                <span className="text-gray-400">Age</span><span className="text-white font-mono">{result.score_breakdown.age_score}</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
