import numpy as np
from tracker import MultiObjectTracker

def test_synthetic_data():
    np.random.seed(42)
    tracker = MultiObjectTracker()
    
    # Simulate two objects walking in straight lines
    # Object 1: starts at (0, 0, 0), moves (+1, +0.5, 0) per sec
    # Object 2: starts at (10, 10, 0), moves (-1, -1, 0) per sec
    dt = 0.1
    steps = 100
    
    gt_obj1 = np.array([0.0, 0.0, 0.0])
    v1 = np.array([1.0, 0.5, 0.0])
    
    gt_obj2 = np.array([10.0, 10.0, 0.0])
    v2 = np.array([-1.0, -1.0, 0.0])
    
    # Noise standard deviation
    noise_std = 0.5
    
    for step in range(steps):
        # Move objects
        gt_obj1 += v1 * dt
        gt_obj2 += v2 * dt
        
        # Generate noisy detections
        det1 = gt_obj1 + np.random.normal(0, noise_std, 3)
        det2 = gt_obj2 + np.random.normal(0, noise_std, 3)
        
        # Occasionally miss a detection
        detections = []
        if np.random.rand() > 0.1:
            detections.append(det1)
        if np.random.rand() > 0.1:
            detections.append(det2)
            
        # Run tracker
        active_states = tracker.step(detections, dt)
        
        if step == steps - 1:
            print(f"Final step {step}:")
            print(f"GT Obj 1: {gt_obj1}")
            print(f"GT Obj 2: {gt_obj2}")
            print(f"Tracker states:")
            for state in active_states:
                print(f"ID {state[0]}: Pos ({state[1]:.2f}, {state[2]:.2f}, {state[3]:.2f}) "
                      f"Vel ({state[4]:.2f}, {state[5]:.2f}, {state[6]:.2f})")
                
            # Assertions to ensure it works
            assert len(active_states) == 2, f"Expected 2 tracks, got {len(active_states)}"
            
            # Check velocity estimates
            v_estimates = [state[4:7] for state in active_states]
            for v_est in v_estimates:
                dist1 = np.linalg.norm(np.array(v_est) - v1)
                dist2 = np.linalg.norm(np.array(v_est) - v2)
                assert min(dist1, dist2) < 1.0, f"Velocity estimate {v_est} is too far from true velocities"
                
    print("\nSynthetic tracking test passed successfully!")

if __name__ == "__main__":
    test_synthetic_data()
