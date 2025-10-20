import numpy as np
import soundfile as sf
from typing import Dict, Tuple, Any

from effects import EFFECT_HANDLERS
from audio_processing import DistanceFilter
from rendering import render_ambisonic_and_binaural


class Speaker():
    
    def __init__(self, track, order=1, output_format='binaural', 
                 lp_base=10000.0, lp_rolloff=1.0, distance_rolloff=1.0):
        
        self.ambi_order = order
        self.output_format = output_format
        self.track, self.fs = sf.read(track, always_2d=True)
        self.mono_track = np.mean(self.track, axis=1).astype(np.float32)
        
        self.distance_filter = DistanceFilter(self.fs, lp_base, lp_rolloff)
        self.distance_rolloff = float(distance_rolloff)
        
        n_samples = len(self.mono_track)
        self.azimuth = np.zeros(n_samples, dtype=np.float32)
        self.elevation = np.full(n_samples, np.pi/2, dtype=np.float32)
        self.distance = np.ones(n_samples, dtype=np.float32)
        
        self.effects = {}
        
        print(f"Loaded {len(self.mono_track)} samples at {self.fs} Hz")
        print(f"Output format: {self.output_format}")
    
    def add_effect(self, time_range: Tuple[float, float], effect: Dict[str, Any]):
        
        start_time, end_time = time_range
        if start_time < 0 or end_time > len(self.mono_track) / self.fs:
            raise ValueError(f"Time range {time_range} outside track duration")
        if start_time >= end_time:
            raise ValueError(f"Invalid time range: start >= end")
        
        self.effects[time_range] = effect
        print(f"Added effect '{effect.get('type', 'unknown')}' for time range {time_range}")
    
    def clear_effects(self):
        
        self.effects = {}
        n_samples = len(self.mono_track)
        self.azimuth = np.zeros(n_samples, dtype=np.float32)
        self.elevation = np.full(n_samples, np.pi/2, dtype=np.float32)
        self.distance = np.ones(n_samples, dtype=np.float32)
    
    def render(self, output_path="output.wav", sofa_path=None):
        
        n_samples = len(self.mono_track)
        self.azimuth = np.zeros(n_samples, dtype=np.float32)
        self.elevation = np.full(n_samples, np.pi/2, dtype=np.float32)
        self.distance = np.ones(n_samples, dtype=np.float32)
        
        sorted_effects = sorted(self.effects.items(), key=lambda x: x[0][0])
        
        for (start_time, end_time), effect in sorted_effects:
            start_sample = int(start_time * self.fs)
            end_sample = int(end_time * self.fs)
            effect_type = effect.get('type')
            
            handler = EFFECT_HANDLERS.get(effect_type)
            if handler:
                handler(self.azimuth, self.elevation, self.distance,
                       start_sample, end_sample, effect, self.fs)
            else:
                print(f"Warning: Unknown effect type '{effect_type}' - skipping")
        
        return render_ambisonic_and_binaural(
            self.mono_track, self.azimuth, self.elevation, self.distance,
            self.distance_filter, self.ambi_order, self.fs,
            self.output_format, output_path, sofa_path
        )
