import numpy as np
from scipy.optimize import linear_sum_assignment

def compute_mahalanobis_distance(z, z_pred, S):
    """
    Computes the squared Mahalanobis distance.
    
    Args:
        z: Actual measurement (shape: N x 1)
        z_pred: Predicted measurement (shape: N x 1)
        S: Innovation covariance matrix from the EKF (shape: N x N)
        
    Returns:
        float: The squared Mahalanobis distance
    """
    y = z - z_pred
    return (y.T @ np.linalg.pinv(S) @ y).item()

def associate_detections_to_tracks(detections, tracks, gating_threshold=9.49):
    """
    Associates N detections to M tracks using the Hungarian algorithm
    with Mahalanobis distance gating.
    
    Args:
        detections: List of numpy arrays representing new measurements
        tracks: List of active track objects
        gating_threshold: Chi-squared 95% threshold for gating
        
    Returns:
        matches: List of tuples (track_idx, det_idx)
        unmatched_tracks: List of track indices
        unmatched_detections: List of detection indices
    """
    if len(tracks) == 0:
        return [], [], list(range(len(detections)))
        
    if len(detections) == 0:
        return [], list(range(len(tracks))), []

    cost_matrix = np.zeros((len(tracks), len(detections)))
    
    for t_idx, track in enumerate(tracks):
        z_pred, S = track.get_projected_measurement_and_covariance()
        
        for d_idx, z in enumerate(detections):
            z = np.asarray(z).reshape(-1, 1)
            dist = compute_mahalanobis_distance(z, z_pred, S)
            
            # Gating: penalize impossible matches heavily
            if dist > gating_threshold:
                cost_matrix[t_idx, d_idx] = 1e5
            else:
                cost_matrix[t_idx, d_idx] = dist

    # Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    matches = []
    unmatched_tracks = []
    unmatched_detections = list(range(len(detections)))
    
    for t_idx, d_idx in zip(row_ind, col_ind):
        if cost_matrix[t_idx, d_idx] < 1e5:
            matches.append((t_idx, d_idx))
            if d_idx in unmatched_detections:
                unmatched_detections.remove(d_idx)
        else:
            unmatched_tracks.append(t_idx)
            
    for t_idx in range(len(tracks)):
        if not any(m[0] == t_idx for m in matches) and t_idx not in unmatched_tracks:
            unmatched_tracks.append(t_idx)

    return matches, unmatched_tracks, unmatched_detections
