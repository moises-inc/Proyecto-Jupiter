import networkx as nx
import numpy as np
from typing import Dict, List, Tuple

class MuskingumCungeRouter:
    """
    Muskingum-Cunge hydrograph routing along a Directed Acyclic Graph (DAG)
    representing the river network of the 35 sectors.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_sector(self, sector_id: str, k: float, x: float):
        """
        Add a river sector node to the DAG.
        
        :param sector_id: Unique identifier for the sector (e.g., 'Precordillera_1')
        :param k: Storage time constant (travel time through the reach)
        :param x: Weighting factor (0 <= x <= 0.5)
        """
        if not (0 <= x <= 0.5):
            raise ValueError("Weighting factor X must be between 0 and 0.5")
        self.graph.add_node(sector_id, k=k, x=x)
        
    def add_connection(self, upstream_id: str, downstream_id: str):
        """
        Connect two sectors in the DAG.
        """
        if upstream_id not in self.graph or downstream_id not in self.graph:
            raise ValueError("Both sectors must be added before connecting")
        self.graph.add_edge(upstream_id, downstream_id)
        if not nx.is_directed_acyclic_graph(self.graph):
            self.graph.remove_edge(upstream_id, downstream_id)
            raise ValueError("Adding this connection creates a cycle. The network must be a DAG.")

    def route_reach(self, inflow: np.ndarray, dt: float, k: float, x: float) -> np.ndarray:
        """
        Route hydrograph through a single reach using Muskingum-Cunge method.
        
        Q_{j+1} = C_1 * I_{j+1} + C_2 * I_j + C_3 * Q_j
        """
        c0 = k - k * x + 0.5 * dt
        c1 = (0.5 * dt - k * x) / c0
        c2 = (0.5 * dt + k * x) / c0
        c3 = (k - k * x - 0.5 * dt) / c0
        
        n_steps = len(inflow)
        outflow = np.zeros(n_steps)
        
        # Initial condition: steady state assumption Q_0 = I_0
        outflow[0] = inflow[0]
        
        for j in range(n_steps - 1):
            outflow[j+1] = c1 * inflow[j+1] + c2 * inflow[j] + c3 * outflow[j]
            
        return outflow

    def simulate_network(self, inflows: Dict[str, np.ndarray], dt: float) -> Dict[str, np.ndarray]:
        """
        Simulate routing through the entire network DAG.
        
        :param inflows: Dictionary mapping sector_id to its initial external inflow time series.
        :param dt: Time step duration.
        :return: Dictionary of outflow time series for each sector.
        """
        outflows = {}
        # Iterate in topological order to ensure upstream reaches are processed before downstream
        for node in nx.topological_sort(self.graph):
            k = self.graph.nodes[node]['k']
            x = self.graph.nodes[node]['x']
            
            # Total inflow to this node is the external inflow plus outflows from upstream neighbors
            total_inflow = inflows.get(node, np.zeros(0))
            
            upstream_nodes = list(self.graph.predecessors(node))
            if upstream_nodes:
                if len(total_inflow) == 0:
                    total_inflow = np.zeros_like(outflows[upstream_nodes[0]])
                for up_node in upstream_nodes:
                    total_inflow += outflows[up_node]
            
            if len(total_inflow) == 0:
                raise ValueError(f"No inflow data available for node {node} and no upstream contributors.")
                
            outflows[node] = self.route_reach(total_inflow, dt, k, x)
            
        return outflows
