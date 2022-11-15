import os

repo_root_dir = os.path.dirname(os.path.realpath(__file__))

config = {
    'paths': {
        'audio': os.path.abspath(os.path.join(repo_root_dir, 'data', 'audio')),
        'environments_file': os.path.abspath(os.path.join(repo_root_dir, 'data', 'environments.json')),
    },
    'clock': {
        'tick_amount': 10
    }
}
