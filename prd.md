PRODUCT REQUIREMENTS DOCUMENT

Product Name: WalletMind

Problem

Crypto lenders and crypto neobanks need a way to evaluate the reliability of a wallet before issuing credit. Traditional credit scoring systems do not exist for blockchain wallets. WalletMind solves this by analyzing on-chain activity and generating a credit score and behavioral explanation.

Goal

Build an MVP system that:

• Accepts a crypto wallet address  
• Fetches blockchain transaction data  
• Extracts behavioral features  
• Calculates a wallet credit score  
• Generates an explanation of the score  
• Returns results through an API and simple dashboard

Target Users

• crypto fintech companies  
• DeFi lending protocols  
• crypto banks  
• blockchain analytics platforms

MVP Scope

The system must support:

• Ethereum wallets
• transaction analysis
• behavioral feature extraction
• credit score calculation
• explanation generation
• FastAPI backend
• minimal frontend dashboard

Non Goals (for MVP)

• multi-chain support
• real ML training pipelines
• production database
• authentication systems

Those will be future upgrades.

User Flow

User enters wallet address

System performs:

wallet analysis pipeline:

wallet_address
→ fetch transaction history
→ compute wallet behavioral features
→ calculate credit score
→ generate explanation
→ return structured response

Output

wallet credit report including:

wallet_address
credit_score
risk_level
behavioral_features
explanation