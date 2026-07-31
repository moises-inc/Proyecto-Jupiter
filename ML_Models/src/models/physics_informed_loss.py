from typing import Tuple
import torch
import torch.nn as nn

class MassConservationLoss(nn.Module):
    """
    Physics-Informed Neural Network (PINN) loss for 1D Saint-Venant mass conservation equation:
    dA/dt + dQ/dx = q
    
    where:
    A = cross-sectional flow area
    Q = streamflow discharge
    t = time
    x = longitudinal distance
    q = lateral inflow/outflow per unit length
    """
    def __init__(self, weight: float = 1.0):
        super().__init__()
        self.weight = weight
        self.mse = nn.MSELoss()

    def forward(self, 
                A_pred: torch.Tensor, 
                Q_pred: torch.Tensor, 
                q_true: torch.Tensor, 
                dt: torch.Tensor, 
                dx: torch.Tensor) -> torch.Tensor:
        """
        Computes the physics-informed regularization loss.
        Expects tensors of shape (batch, time_steps, space_steps).
        
        :param A_pred: Predicted cross-sectional area
        :param Q_pred: Predicted streamflow
        :param q_true: Known lateral inflow
        :param dt: Time step size (or tensor of same dimension)
        :param dx: Space step size (or tensor of same dimension)
        """
        # Finite difference approximations
        # dA/dt approx (A[:, 1:, :] - A[:, :-1, :]) / dt
        dA_dt = (A_pred[:, 1:, :] - A_pred[:, :-1, :]) / dt
        
        # dQ/dx approx (Q[:, :, 1:] - Q[:, :, :-1]) / dx
        dQ_dx = (Q_pred[:, :, 1:] - Q_pred[:, :, :-1]) / dx
        
        # Align dimensions to compute residual in the overlapping interior domain
        # dA_dt has time size T-1, Q_pred has space size X
        # dQ_dx has time size T, Q_pred has space size X-1
        
        dA_dt_interior = dA_dt[:, :, :-1] # Shape: (batch, T-1, X-1)
        dQ_dx_interior = dQ_dx[:, :-1, :] # Shape: (batch, T-1, X-1)
        q_interior = q_true[:, :-1, :-1]  # Shape: (batch, T-1, X-1)
        
        # Residual of the continuity equation: R = dA/dt + dQ/dx - q
        residual = dA_dt_interior + dQ_dx_interior - q_interior
        
        # Physics loss is the mean squared error of the residual (it should be 0)
        physics_loss = torch.mean(residual ** 2)
        
        return self.weight * physics_loss

class CombinedHydroLoss(nn.Module):
    """
    Combines standard data-driven loss (e.g., MSE on discharge) with physics-informed regularization.
    """
    def __init__(self, physics_weight: float = 0.1):
        super().__init__()
        self.data_loss_fn = nn.MSELoss()
        self.physics_loss_fn = MassConservationLoss(weight=physics_weight)
        
    def forward(self, 
                Q_pred: torch.Tensor, Q_true: torch.Tensor,
                A_pred: torch.Tensor, q_true: torch.Tensor,
                dt: torch.Tensor, dx: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        
        data_loss = self.data_loss_fn(Q_pred, Q_true)
        physics_loss = self.physics_loss_fn(A_pred, Q_pred, q_true, dt, dx)
        
        total_loss = data_loss + physics_loss
        return total_loss, data_loss, physics_loss
