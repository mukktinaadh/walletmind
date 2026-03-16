# WalletMind — On-Chain Credit Intelligence Engine

WalletMind analyzes Ethereum wallets using behavioral signals, network graph analytics, and reputation scoring to estimate creditworthiness and lending capacity in Web3.

## Live Demo
[https://walletmind.vercel.app](https://walletmind.vercel.app)

### Example Wallets:
*   **Vitalik:** `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
*   **Uniswap Router:** `0x7a250d5630b4cf539739df2c5dacab4c659f2488`

## Deployment Guide

### Verification of Vercel Compatibility
The WalletMind architecture consists of a Next.js frontend and a FastAPI backend. 

*   **Frontend**: The Next.js frontend is **fully compatible** with Vercel and is optimized for its edge network.
*   **Backend**: The FastAPI backend is technically capable of running on Vercel via Serverless Functions mapping (`vercel.json`), but **it is not recommended**. Vercel imposes strict 10-second (hobby) or 60-second (pro) execution timeouts and limited memory scaling, which can cause network/graph calculation functions and large Etherscan API batch fetches to timeout or crash.
*   **Recommended Deployment Architecture**:
    *   **Frontend**: Hosted on [Vercel](https://vercel.com).
    *   **Backend**: Hosted on [Render](https://render.com), [Railway](https://railway.app), or [Fly.io](https://fly.io) as a persistent single-instance service capable of handling heavy pandas/networkx background data tasks.

### Frontend Deployment (Vercel)
1. Fork or clone this repository to your GitHub account.
2. In the Vercel dashboard, click **Add New...** -> **Project** and select this repository.
3. Configure the **Root Directory** as `frontend`.
4. In **Environment Variables**, add:
   *   `NEXT_PUBLIC_API_URL`: Set this to your deployed backend URL (e.g., `https://walletmind-api.onrender.com`).
5. The build settings should automatically use:
   *   Build Command: `npm run build`
   *   Install Command: `npm install`
6. Click **Deploy**.

### Backend Deployment (Render / Railway / Fly.io)
**Example using Render:**
1. In the Render dashboard, create a new **Web Service**.
2. Connect your GitHub repository.
3. Configure the following deployment settings:
   *   **Root Directory**: `backend`
   *   **Environment**: Python
   *   **Build Command**: `pip install -r requirements.txt`
   *   **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. In the **Environment Variables** section, add:
   *   `ETHERSCAN_API_KEY`: Your Etherscan API Key for transaction fetching.
5. Click **Create Web Service**.

Once the backend is deployed, copy its URL and use it to set the `NEXT_PUBLIC_API_URL` environment variable for your Vercel frontend.
