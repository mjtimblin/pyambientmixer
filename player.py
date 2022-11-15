import pygame

from config import config
from models.environment import Environment
from player_channel import PlayerChannel


class Player:
    def __init__(self):
        self.pygame_channels = []
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

    def play(self, environment: Environment):
        for i, channel_model in enumerate(environment.channels):
            channel = PlayerChannel(i, channel_model)
            self.pygame_channels.append(channel)
            print(f'Loaded {channel}')

        for channel in self.pygame_channels:
            channel.play()

        print('')
        print(environment.attribution)
        print('Press CTRL+C to exit.')

        while True:
            self.clock.tick(config['clock']['tick_amount'])
            for channel in self.pygame_channels:
                channel.tick()
