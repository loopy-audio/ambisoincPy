import numpy as np


class DistanceFilter:
    
    def __init__(self, fs, lp_base=10000.0, lp_rolloff=1.0):
        
        self.fs = float(fs)
        self.lp_base = float(lp_base)
        self.lp_rolloff = float(lp_rolloff)
        
        self.x_prev = 0.0
        self.y_prev = 0.0
    
    def reset_state(self):
        
        self.x_prev = 0.0
        self.y_prev = 0.0
    
    def process_block(self, x_block, dist_block):
        
        mean_d = float(np.maximum(np.mean(dist_block), 1e-6))
        fc = max(1.0, min(self.fs / 2.1, self.lp_base / (mean_d ** self.lp_rolloff)))
        
        dt = 1.0 / self.fs
        RC = 1.0 / (2.0 * np.pi * fc)
        alpha = dt / (RC + dt)
        
        y_prev = float(self.y_prev)
        y_out = np.empty_like(x_block, dtype=np.float32)
        
        for i, x in enumerate(x_block):
            y = y_prev + alpha * (float(x) - y_prev)
            y_out[i] = y
            y_prev = y
        
        self.y_prev = y_prev
        
        return y_out
