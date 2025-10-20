import numpy as np


def apply_move(azimuth, elevation, distance, start_idx, end_idx, effect, fs):
    
    start_pos = effect.get('start', (0, np.pi/2, 1.0))
    end_pos = effect.get('end', (0, np.pi/2, 1.0))
    
    start_azi, start_elev, start_dist = start_pos
    end_azi, end_elev, end_dist = end_pos
    
    n = end_idx - start_idx
    t = np.linspace(0, 1, n)
    
    azimuth[start_idx:end_idx] = start_azi + (end_azi - start_azi) * t
    elevation[start_idx:end_idx] = start_elev + (end_elev - start_elev) * t
    distance[start_idx:end_idx] = start_dist + (end_dist - start_dist) * t


def apply_spin_horizontal(azimuth, elevation, distance, start_idx, end_idx, effect, fs):
    
    revolutions = effect.get('revolutions', 1)
    clockwise = effect.get('clockwise', True)
    speed = effect.get('speed', 1)
    
    n = end_idx - start_idx
    duration = n / fs
    rotation_period = duration / (revolutions * speed)
    
    t = np.arange(n) / fs
    azi = 2 * np.pi * (t / rotation_period)
    if not clockwise:
        azi = -azi
    
    azimuth[start_idx:end_idx] = azi
    if 'elevation' in effect:
        elevation[start_idx:end_idx] = effect['elevation']


def apply_spin_vertical(azimuth, elevation, distance, start_idx, end_idx, effect, fs):
    
    revolutions = effect.get('revolutions', 1)
    clockwise = effect.get('clockwise', True)
    speed = effect.get('speed', 1)
    
    n = end_idx - start_idx
    duration = n / fs
    
    t = np.arange(n) / fs
    elev = np.pi/2 + np.pi * np.sin(2 * np.pi * revolutions * t / duration)
    if not clockwise:
        elev = np.pi - elev
    
    elevation[start_idx:end_idx] = elev


def apply_randomise(azimuth, elevation, distance, start_idx, end_idx, effect, fs):
    
    n_movements = effect.get('n_movements', 5)
    seed = effect.get('seed', None)
    
    if seed is not None:
        np.random.seed(seed)
    
    n = end_idx - start_idx
    
    azimuths = np.random.uniform(0, 2 * np.pi, n_movements + 1)
    elevations = np.random.uniform(0, np.pi, n_movements + 1)
    distances = np.random.uniform(0.5, 5.0, n_movements + 1)
    
    if start_idx > 0:
        azimuths[0] = azimuth[start_idx - 1]
        elevations[0] = elevation[start_idx - 1]
        distances[0] = distance[start_idx - 1]
    
    samples_per_movement = n // n_movements
    
    for i in range(n_movements):
        seg_start = start_idx + i * samples_per_movement
        seg_end = start_idx + (i + 1) * samples_per_movement if i < n_movements - 1 else end_idx
        seg_n = seg_end - seg_start
        
        t = np.linspace(0, 1, seg_n)
        azimuth[seg_start:seg_end] = azimuths[i] + (azimuths[i+1] - azimuths[i]) * t
        elevation[seg_start:seg_end] = elevations[i] + (elevations[i+1] - elevations[i]) * t
        distance[seg_start:seg_end] = distances[i] + (distances[i+1] - distances[i]) * t


def apply_static(azimuth, elevation, distance, start_idx, end_idx, effect, fs):
    
    position = effect.get('position', (0, np.pi/2, 1.0))
    azi, elev, dist = position
    
    azimuth[start_idx:end_idx] = azi
    elevation[start_idx:end_idx] = elev
    distance[start_idx:end_idx] = dist


EFFECT_HANDLERS = {
    'move': apply_move,
    'spin_horizontal': apply_spin_horizontal,
    'spin_vertical': apply_spin_vertical,
    'randomise': apply_randomise,
    'static': apply_static,
}
