import numpy as np
from ekf import ExtendedKalmanFilter
from data_association import associate_detections_to_tracks

class TrackState:
    TENTATIVE = 1
    CONFIRMED = 2
    LOST = 3

class Track:
    def __init__(self, track_id, initial_z):
        self.track_id = track_id
        self.state = TrackState.TENTATIVE
        
        # State: [X, Y, Z, Vx, Vy, Vz]
        self.ekf = ExtendedKalmanFilter(state_dim=6, meas_dim=3)
        
        # High uncertainty for unobservable velocity
        self.ekf.P[3:, 3:] *= 10.0
        
        # Tune process noise Q and measurement noise R
        # Q dictates how much we trust the motion model
        self.ekf.Q = np.eye(6) * 0.1 
        self.ekf.Q[3:, 3:] *= 10.0 # Velocity is less predictable
        # R dictates how much we trust the measurement
        self.ekf.R = np.eye(3) * 0.5 
        
        z = np.asarray(initial_z).reshape(3, 1)
        self.ekf.x[:3] = z
        
        self.hits = 1
        self.age = 1
        self.time_since_update = 0
        
        # Tunable track lifecycle parameters
        self.n_init = 3
        self.max_age = 10
        
    def predict(self, dt):
        """Propagate state forward using constant velocity model"""
        def f(x):
            x_new = x.copy()
            x_new[0] += x[3] * dt
            x_new[1] += x[4] * dt
            x_new[2] += x[5] * dt
            return x_new
            
        def F_jacobian(x):
            F = np.eye(6)
            F[0, 3] = dt
            F[1, 4] = dt
            F[2, 5] = dt
            return F
            
        self.ekf.predict(f, F_jacobian)
        self.age += 1
        self.time_since_update += 1
        
    def update(self, z):
        """Update with new measurement"""
        def h(x):
            return x[:3] # We measure X, Y, Z directly in this simplified model
            
        def H_jacobian(x):
            H = np.zeros((3, 6))
            H[0, 0] = 1
            H[1, 1] = 1
            H[2, 2] = 1
            return H
            
        self.ekf.update(z, h, H_jacobian)
        self.hits += 1
        self.time_since_update = 0
        
        if self.state == TrackState.TENTATIVE and self.hits >= self.n_init:
            self.state = TrackState.CONFIRMED
        elif self.state == TrackState.LOST:
            self.state = TrackState.CONFIRMED
            
    def mark_missed(self):
        """Handle track that got no measurement"""
        if self.state == TrackState.TENTATIVE:
            self.state = TrackState.LOST 
        elif self.time_since_update > self.max_age:
            self.state = TrackState.LOST
            
    def is_dead(self):
        return self.state == TrackState.LOST and self.time_since_update > self.max_age
        
    def get_projected_measurement_and_covariance(self):
        """Used for data association (Mahalanobis distance)"""
        def h(x):
            return x[:3]
            
        def H_jacobian(x):
            H = np.zeros((3, 6))
            H[0, 0] = 1
            H[1, 1] = 1
            H[2, 2] = 1
            return H
            
        z_pred = h(self.ekf.x)
        H = H_jacobian(self.ekf.x)
        S = H @ self.ekf.P @ H.T + self.ekf.R
        return z_pred, S

class MultiObjectTracker:
    def __init__(self):
        self.tracks = []
        self.next_id = 1
        
    def step(self, detections, dt=0.1):
        """
        Run one step of the tracker.
        Args:
            detections: List of [X, Y, Z] measurements
            dt: Time step since last update
        Returns:
            List of confirmed tracks' states [id, X, Y, Z, Vx, Vy, Vz]
        """
        # 1. Predict
        for track in self.tracks:
            track.predict(dt)
            
        # 2. Associate
        matches, unmatched_tracks, unmatched_detections = associate_detections_to_tracks(
            detections, self.tracks, gating_threshold=9.49
        )
        
        # 3. Update matched tracks
        for t_idx, d_idx in matches:
            self.tracks[t_idx].update(detections[d_idx])
            
        # 4. Handle unmatched tracks (missed detections)
        for t_idx in unmatched_tracks:
            self.tracks[t_idx].mark_missed()
            
        # 5. Handle unmatched detections (new track births)
        for d_idx in unmatched_detections:
            new_track = Track(self.next_id, detections[d_idx])
            self.tracks.append(new_track)
            self.next_id += 1
            
        # 6. Remove dead tracks
        self.tracks = [t for t in self.tracks if not t.is_dead()]
        
        # Return only confirmed tracks for visualization/downstream
        active_states = []
        for t in self.tracks:
            if t.state == TrackState.CONFIRMED:
                state = [t.track_id] + t.ekf.x.flatten().tolist()
                active_states.append(state)
                
        return active_states
