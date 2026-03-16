import WalletAnalyzer from "@/components/WalletAnalyzer";

export default function Home() {
    return (
        <main className="min-h-screen bg-[#0a0a0a] text-white flex flex-col items-center p-6 md:p-24 selection:bg-blue-500/30 selection:text-blue-200">

            {/* Background Gradients */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-900/20 blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/20 blur-[120px]" />
            </div>

            {/* Header Section */}
            <div className="max-w-3xl w-full text-center space-y-6 mb-12 mt-12">
                <div className="inline-flex items-center justify-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-4">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                    </span>
                    WalletMind MVP
                </div>

                <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-br from-white via-white to-gray-400 pb-2">
                    AI Credit Scoring <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                        for Web3
                    </span>
                </h1>

                <p className="text-lg text-gray-400 max-w-2xl mx-auto">
                    Analyze any Ethereum wallet address instantly. We extract transaction features, evaluate network diversity, and compute an AI-driven credit score with clear risk levels.
                </p>
            </div>

            {/* Analyzer Component */}
            <WalletAnalyzer />

        </main>
    );
}
