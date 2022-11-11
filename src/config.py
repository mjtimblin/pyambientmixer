import os

src_dir = os.path.dirname(os.path.realpath(__file__))

config = {
    'paths': {
        'src_dir': src_dir,
        'audio': os.path.abspath(os.path.join(src_dir, '..', 'data', 'audio')),
        'environments_file': os.path.abspath(os.path.join(src_dir, '..', 'data', 'environments.json')),
    },
    'clock': {
        'tick_amount': 10
    }
}
