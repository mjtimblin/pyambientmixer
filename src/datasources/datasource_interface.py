import json
import os
from dataclasses import asdict
from typing import Optional

from src.config import config
from src.models.environment import Environment


class DatasourceInterface:
    environment: Optional[Environment] = None

    def __init__(self, url):
        self.url = url

    # IMPLEMENT IN CHILD CLASS
    @staticmethod
    def is_valid_url(url):
        raise NotImplementedError

    # IMPLEMENT IN CHILD CLASS
    def load_environment(self):
        raise NotImplementedError

    def save_environment(self):
        if os.path.exists(config['paths']['environments_file']):
            environments = json.loads(open(config['paths']['environments_file'], 'r').read())
        else:
            environments = []

        if self.environment.id not in [e['id'] for e in environments]:
            print(f'Downloading environment from url: {self.environment.src_url}')
            environments.append(asdict(self.environment))
            open(config['paths']['environments_file'], 'w').write(json.dumps(environments, indent=2))
            print(f'Environment saved as id: {self.environment.id}')
