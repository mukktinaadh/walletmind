import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from typing import List, Dict, Any

def compute_graph_metrics(transactions: List[Dict[str, Any]], wallet_address: str) -> Dict[str, float]:
    """
    Build a wallet interaction graph and compute metrics.
    Avoids heavy graph calculations for large networks by capping edges.
    """
    if not transactions:
        return {
            "degree_centrality": 0.0,
            "clustering_coefficient": 0.0,
            "network_density": 0.0,
            "cluster_count": 0,
            "largest_cluster_size": 0
        }
        
    # Cap transactions to prevent heavy computation
    txs_to_process = transactions[:500]
    
    G = nx.Graph()
    
    # Ensure the main wallet is in the graph
    main_wallet = wallet_address.lower()
    G.add_node(main_wallet)
    
    for tx in txs_to_process:
        from_addr = tx.get("from", "").lower()
        to_addr = tx.get("to", "").lower()
        
        if from_addr and to_addr:
            # We use an undirected graph to just measure proximity and clusters
            nodes_to_add = 0
            if from_addr not in G: nodes_to_add += 1
            if to_addr not in G: nodes_to_add += 1
            
            if G.number_of_nodes() + nodes_to_add > 200:
                # If we exceed 200 nodes, only add edges between already known nodes
                if from_addr in G and to_addr in G:
                    G.add_edge(from_addr, to_addr)
                continue
                
            G.add_edge(from_addr, to_addr)
            
    num_nodes = G.number_of_nodes()
    
    if num_nodes <= 1:
        return {
            "degree_centrality": 0.0,
            "clustering_coefficient": 0.0,
            "network_density": 0.0,
            "cluster_count": 0,
            "largest_cluster_size": 0
        }
        
    try:
        # Degree centrality of the main wallet
        deg_centrality = nx.degree_centrality(G).get(main_wallet, 0.0)
        
        # Clustering coefficient of the main wallet
        clustering_coeff = nx.clustering(G, main_wallet)
        
        # Network density of the ego-network (or full network)
        density = nx.density(G)
        
        # Cluster Detection using greedy modularity communities
        communities = list(greedy_modularity_communities(G))
        cluster_count = len(communities)
        largest_cluster = max([len(c) for c in communities]) if communities else 0
        
        return {
            "degree_centrality": round(deg_centrality, 4),
            "clustering_coefficient": round(clustering_coeff, 4),
            "network_density": round(density, 4),
            "cluster_count": cluster_count,
            "largest_cluster_size": largest_cluster
        }
    except Exception:
        # Fallback in case of math errors on edge cases
        return {
            "degree_centrality": 0.0,
            "clustering_coefficient": 0.0,
            "network_density": 0.0,
            "cluster_count": 0,
            "largest_cluster_size": 0
        }
