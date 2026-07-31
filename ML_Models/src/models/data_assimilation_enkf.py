from typing import Tuple
import numpy as np

class EnsembleKalmanFilter:
    """
    Ensemble Kalman Filter (EnKF) for real-time hydrological data assimilation.
    Used to dynamically update sector risk probabilities based on IoT gauge data.
    """
    def __init__(self, n_ensembles: int, state_dim: int, obs_dim: int):
        self.N = n_ensembles
        self.state_dim = state_dim
        self.obs_dim = obs_dim
        
        # Initialize ensemble matrix X: (state_dim, N)
        self.X = np.zeros((state_dim, n_ensembles))
        
    def initialize_ensembles(self, initial_state_mean: np.ndarray, initial_covariance: np.ndarray):
        """
        Initialize the ensemble members based on an initial prior distribution.
        """
        # Draw N samples from Multivariate Normal
        self.X = np.random.multivariate_normal(initial_state_mean, initial_covariance, self.N).T

    def predict(self, model_function, process_noise_cov: np.ndarray, *model_args):
        """
        Forecast step: Propagate all ensembles forward using the physical/ML model.
        
        :param model_function: A callable f(x, *args) representing the state transition.
        :param process_noise_cov: Covariance matrix of the model error Q.
        """
        # Apply model to each ensemble
        for i in range(self.N):
            self.X[:, i] = model_function(self.X[:, i], *model_args)
            
        # Add process noise
        process_noise = np.random.multivariate_normal(np.zeros(self.state_dim), process_noise_cov, self.N).T
        self.X += process_noise

    def update(self, observation: np.ndarray, obs_operator: np.ndarray, obs_noise_cov: np.ndarray):
        """
        Analysis/Update step: Incorporate real-time IoT gauge data.
        
        :param observation: Vector of current observations from IoT sensors.
        :param obs_operator: Matrix H mapping state space to observation space (obs_dim, state_dim).
        :param obs_noise_cov: Covariance matrix of observation errors R.
        """
        H = obs_operator
        R = obs_noise_cov
        
        # Generate perturbed observations
        obs_perturbations = np.random.multivariate_normal(np.zeros(self.obs_dim), R, self.N).T
        Y = np.tile(observation.reshape(-1, 1), (1, self.N)) + obs_perturbations
        
        # Calculate ensemble mean and anomalies
        x_mean = np.mean(self.X, axis=1, keepdims=True)
        A = self.X - x_mean
        
        # Predicted observations and their anomalies
        HX = H @ self.X
        hx_mean = np.mean(HX, axis=1, keepdims=True)
        HA = HX - hx_mean
        
        # Cross-covariance and Innovation covariance
        # P_ht = A @ HA.T / (self.N - 1)
        # S = HA @ HA.T / (self.N - 1) + R
        
        # Standard EnKF Kalman Gain formulation
        P_ht = (A @ HA.T) / (self.N - 1)
        S = (HA @ HA.T) / (self.N - 1) + R
        
        K = P_ht @ np.linalg.inv(S)
        
        # Update ensembles
        self.X = self.X + K @ (Y - HX)
        
    def get_state_estimate(self) -> np.ndarray:
        """
        Get the current best estimate of the state (ensemble mean).
        """
        return np.mean(self.X, axis=1)
        
    def get_state_covariance(self) -> np.ndarray:
        """
        Get the current uncertainty of the state (ensemble covariance).
        """
        x_mean = self.get_state_estimate().reshape(-1, 1)
        A = self.X - x_mean
        return (A @ A.T) / (self.N - 1)


def assimilate_iot_observations(
    enkf: EnsembleKalmanFilter,
    observed_precip_mm: float,
    forecast_precip_mm: float,
    obs_uncertainty_mm: float = 0.5
) -> Tuple[float, float]:
    """
    Assimilates a real-time CEAZAMET ground truth observation into the EnKF.
    Calculates the innovation (observed - forecast) and applies the update
    to the ensemble.

    State vector: [precip, temperature, wind_speed]
    Observation: [precip] (scalar from CEAZAMET station)

    Returns (corrected_precip, innovation).
    """
    innovation = observed_precip_mm - forecast_precip_mm

    state_est = enkf.get_state_estimate()
    state_est[0] = max(0.0, state_est[0] + 0.3 * innovation)

    y_obs = np.array([observed_precip_mm])
    H = np.array([[1.0, 0.0, 0.0]])
    R = np.eye(1) * obs_uncertainty_mm

    enkf.update(y_obs, H, R)
    corrected = float(enkf.get_state_estimate()[0])
    corrected = max(0.0, corrected)
    post_innovation = observed_precip_mm - corrected

    return corrected, post_innovation
