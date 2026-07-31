import unittest
import numpy as np
import torch
import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from features.streamflow_routing import MuskingumCungeRouter
from models.physics_informed_loss import MassConservationLoss, CombinedHydroLoss
from models.data_assimilation_enkf import EnsembleKalmanFilter

class TestStreamflowRouting(unittest.TestCase):
    def setUp(self):
        self.router = MuskingumCungeRouter()
        
    def test_add_sector_and_connection(self):
        self.router.add_sector('S1', k=1.0, x=0.2)
        self.router.add_sector('S2', k=1.5, x=0.3)
        self.router.add_connection('S1', 'S2')
        self.assertTrue('S1' in self.router.graph)
        self.assertTrue('S2' in self.router.graph)
        self.assertTrue(self.router.graph.has_edge('S1', 'S2'))
        
    def test_cycle_prevention(self):
        self.router.add_sector('S1', 1.0, 0.2)
        self.router.add_sector('S2', 1.0, 0.2)
        self.router.add_connection('S1', 'S2')
        with self.assertRaises(ValueError):
            self.router.add_connection('S2', 'S1')
            
    def test_simulate_network(self):
        self.router.add_sector('S1', k=2.0, x=0.2)
        self.router.add_sector('S2', k=3.0, x=0.3)
        self.router.add_connection('S1', 'S2')
        
        inflows = {
            'S1': np.array([10.0, 20.0, 30.0, 20.0, 10.0])
        }
        
        outflows = self.router.simulate_network(inflows, dt=1.0)
        self.assertIn('S1', outflows)
        self.assertIn('S2', outflows)
        self.assertEqual(len(outflows['S2']), 5)


class TestPhysicsInformedLoss(unittest.TestCase):
    def test_mass_conservation_loss(self):
        loss_fn = MassConservationLoss(weight=1.0)
        
        batch, time_steps, space_steps = 2, 5, 4
        A = torch.ones((batch, time_steps, space_steps))
        Q = torch.ones((batch, time_steps, space_steps))
        q = torch.zeros((batch, time_steps, space_steps))
        
        dt = torch.tensor(1.0)
        dx = torch.tensor(1.0)
        
        # With constants, derivatives are 0, loss should be 0
        loss = loss_fn(A, Q, q, dt, dx)
        self.assertAlmostEqual(loss.item(), 0.0)


class TestDataAssimilationEnKF(unittest.TestCase):
    def test_enkf_flow(self):
        state_dim = 3
        obs_dim = 2
        N = 10
        enkf = EnsembleKalmanFilter(n_ensembles=N, state_dim=state_dim, obs_dim=obs_dim)
        
        init_mean = np.array([1.0, 2.0, 3.0])
        init_cov = np.eye(state_dim)
        enkf.initialize_ensembles(init_mean, init_cov)
        
        self.assertEqual(enkf.X.shape, (state_dim, N))
        
        def mock_model(state):
            return state * 1.1
            
        q_cov = np.eye(state_dim) * 0.1
        enkf.predict(mock_model, q_cov)
        
        obs = np.array([1.5, 2.5])
        H = np.array([[1, 0, 0], [0, 1, 0]])
        r_cov = np.eye(obs_dim) * 0.1
        
        enkf.update(obs, H, r_cov)
        
        est = enkf.get_state_estimate()
        self.assertEqual(est.shape, (state_dim,))

if __name__ == '__main__':
    unittest.main()
