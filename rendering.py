import numpy as np
import soundfile as sf
import spaudiopy as spa


def render_ambisonic_and_binaural(mono_track, azimuth, elevation, distance, 
                                   distance_filter, ambi_order, fs, 
                                   output_format, output_path, sofa_path=None):
   
    n_samples = len(mono_track)
    n_channels = (ambi_order + 1) ** 2
    
    distance_filter.reset_state()
    
    ambi_signals = np.zeros((n_channels, n_samples), dtype=np.float32)
    
    block_size = 4096
    for start in range(0, n_samples, block_size):
        end = min(start + block_size, n_samples)
        
        Y = spa.sph.sh_matrix(ambi_order, azimuth[start:end], elevation[start:end])
        
        dist_block = distance[start:end]
        filtered = distance_filter.process_block(mono_track[start:end], dist_block)
        
        for ch in range(n_channels):
            ambi_signals[ch, start:end] = filtered * Y[:, ch]
    
    output_files = []
    base_name = output_path.rsplit('.', 1)[0]
    
    if output_format in ['ambisonic', 'both']:
        ambi_path = f"{base_name}_ambisonic.wav"
        sf.write(ambi_path, ambi_signals.T, fs)
        print(f"Saved ambisonic: {ambi_path}")
        output_files.append(ambi_path)
    
    if output_format in ['binaural', 'both']:
        bin_path = f"{base_name}_binaural.wav"
        
        hrirs = spa.io.load_sofa_hrirs(sofa_path) if sofa_path else spa.io.load_hrirs(fs)
        hrirs_decoded = spa.decoder.magls_bin(hrirs, ambi_order)
        stereo = spa.decoder.sh2bin(ambi_signals, hrirs_decoded)
        
        sf.write(bin_path, stereo.T, fs)
        print(f"Saved binaural: {bin_path}")
        output_files.append(bin_path)
    
    return output_files if len(output_files) > 1 else output_files[0]
