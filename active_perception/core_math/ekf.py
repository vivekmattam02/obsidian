import numpy as np

class ExtendedKalmanFilter:
    """
    A mathematically rigorous from-scratch implementation of the Extended Kalman Filter (EKF).
    Designed for nonlinear state estimation in 3D perception tracking.
    """
    def __init__(self, state_dim, meas_dim):
        # State vector
        self.x = np.zeros((state_dim, 1))
        # State covariance matrix (Uncertainty)
        self.P = np.eye(state_dim)
        # Process noise covariance
        self.Q = np.eye(state_dim)
        # Measurement noise covariance
        self.R = np.eye(meas_dim)

    def predict(self, f, F_jacobian):
        """
        Predicts the future state using the nonlinear transition function f(x)
        and updates the uncertainty using its Jacobian F.
        
        Args:
            f: function that takes the state x and returns the predicted state
            F_jacobian: function that takes the state x and returns the Jacobian matrix F
        """
        # 1. Compute the Jacobian of f at the current state (prior to state update)
        F = F_jacobian(self.x)

        # 2. Propagate the state through the nonlinear motion model
        self.x = f(self.x)
        
        # 3. Propagate the uncertainty
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z, h, H_jacobian):
        """
        Updates the state estimate with a new measurement z, using the nonlinear
        measurement function h(x) and its Jacobian H.
        
        Args:
            z: numpy array of shape (meas_dim, 1) representing the measurement
            h: function that takes state x and returns predicted measurement
            H_jacobian: function that takes state x and returns the Jacobian matrix H
        """
        # Ensure measurement is column vector
        z = np.asarray(z).reshape(-1, 1)

        # 1. Predicted measurement
        z_pred = h(self.x)
        
        # 2. Innovation (residual)
        y = z - z_pred
        
        # 3. Compute Jacobian of h at current state
        H = H_jacobian(self.x)
        
        # 4. Innovation covariance (S)
        S = H @ self.P @ H.T + self.R
        
        # 5. Kalman Gain (K)
        # Using pseudo-inverse for stability if S is near-singular
        K = self.P @ H.T @ np.linalg.pinv(S)
        
        # 6. Update State
        self.x = self.x + K @ y
        
        # 7. Update Covariance (Standard form)
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ H) @ self.P
