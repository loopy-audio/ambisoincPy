import numpy as np
from speaker import Speaker

speaker = Speaker("creep.mp3", output_format='both')

speaker.add_effect((0, 10), {'type': 'static', 'position': (0.0, np.pi/2, 2.0)})
speaker.add_effect((10, 20), {'type': 'move', 'start': (-np.pi/2, np.pi/2, 1.5), 'end': (np.pi/2, np.pi/2, 1.5)})
speaker.add_effect((20, 30), {'type': 'move', 'start': (0.0, np.pi/2, 0.5), 'end': (np.pi, np.pi/2, 10.0)})
speaker.add_effect((30, 40), {'type': 'spin_horizontal', 'revolutions': 3, 'clockwise': True})
speaker.add_effect((40, 50), {'type': 'spin_horizontal', 'revolutions': 2, 'clockwise': False})
speaker.add_effect((50, 60), {'type': 'spin_vertical', 'revolutions': 2})
speaker.add_effect((60, 70), {'type': 'randomise', 'n_movements': 5, 'seed': 42})
speaker.add_effect((70, 80), {'type': 'randomise', 'n_movements': 8})
speaker.add_effect((80, 90), {'type': 'static', 'position': (0.0, 0.1, 5.0)})
speaker.add_effect((90, 100), {'type': 'move', 'start': (-np.pi/2, 3*np.pi/4, 0.8), 'end': (np.pi/2, np.pi/4, 6.0)})
speaker.add_effect((100, 120), {'type': 'randomise', 'n_movements': 10, 'seed': 123})

speaker.render(output_path="test_all_effects.wav")

