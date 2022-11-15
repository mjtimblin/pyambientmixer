import argparse
import json
import os
import sys

import dacite
from typing import Optional

from config import config
from datasources import AmbientMixer
from models.environment import Environment

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from player import Player  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description='Download and play ambient-mixer presets locally.')
    parser.add_argument('--url', type=str, help='The url of the environment to download.')
    parser.add_argument('--environment', type=str, help='The name of the downloaded environment to play.')
    args = parser.parse_args()

    environment: Optional[Environment] = None

    if args.url is not None:
        datasource_classes = [AmbientMixer]
        for datasource_class in datasource_classes:
            if datasource_class.is_valid_url(args.url):
                instance = datasource_class(args.url)
                instance.load_environment()
                instance.save_environment()
                environment = instance.environment
                break
    elif args.environment is not None:
        if not os.path.exists(config['paths']['environments_file']):
            print('No environments have been downloaded yet. Download an environment first using the --url argument.')
            sys.exit(1)
        environments = json.loads(open(config['paths']['environments_file'], 'r').read())
        for e in environments:
            if e['id'] == args.environment:
                environment = dacite.from_dict(data_class=Environment, data=e)
                break
    else:
        print('Either --url or --environment is required.')
        parser.print_help()
        sys.exit(1)

    if environment is None:
        print('No environment found for url or name "{}"'.format(args.url or args.environment))
        sys.exit(1)

    print(f'Loaded environment: {environment.id}')
    player = Player()
    player.play(environment)


if __name__ == "__main__":
    main()
