import os
import sys
from random import randint

import pygame

from config import config
from models.channel import Channel


class PlayerChannel:
    def __init__(self, channel_index, channel_model: Channel):
        self.channel_model = channel_model
        self.channel_index = channel_index
        self.channel_object = pygame.mixer.Channel(channel_index)
        self.play_at = []
        self.current_tick = 0

        audio_filepath = os.path.join(config['paths']['audio'], self.channel_model.filepath)
        try:
            self.sound_object = pygame.mixer.Sound(audio_filepath)
            self.sound_object.set_volume(int(self.channel_model.volume) / 100.0)

            left_volume = 1.0 if (self.channel_model.balance <= 0) else (1.0 - self.channel_model.balance)
            right_volume = 1.0 if (self.channel_model.balance >= 0) else (1.0 + self.channel_model.balance)
            self.channel_object.set_volume(left_volume, right_volume)
        except:
            print('Error while loading sound ""?'.format(audio_filepath))
            sys.exit()

    def __repr__(self):
        if self.channel_model.random:
            return "Channel {channel_id} : {name} (random {ran} per {ran_duration} seconds), (volume {vol}, balance {bal})".format(
                channel_id=self.channel_index + 1,
                name=self.channel_model.name,
                vol=self.channel_model.volume,
                bal=self.channel_model.balance,
                ran=self.channel_model.random_interval_count,
                ran_duration=self.channel_model.random_interval_duration
            )
        else:
            return "Channel {channel_id} : {name} (looping), (volume {vol}, balance {bal})".format(
                channel_id=self.channel_index + 1,
                name=self.channel_model.name,
                vol=self.channel_model.volume,
                bal=self.channel_model.balance
            )

    def compute_next_ticks(self):
        val = self.channel_model.random_interval_duration * config['clock']['tick_amount']
        sound_len = self.sound_object.get_length() * 1.5
        self.play_at = self.chop_interval(self.channel_model.random_interval_count, 100, val, sound_len)

    def play(self, force=False):
        fade_ms = 75 if self.channel_model.crossfade else 0
        if not self.channel_model.random and not self.channel_model.mute:
            self.channel_object.play(self.sound_object, loops=-1, fade_ms=fade_ms)
        if force:
            self.channel_object.play(self.sound_object, fade_ms=fade_ms)

    def tick(self):
        if self.channel_model.random and not self.channel_model.mute:
            if len(self.play_at) > 0:
                self.current_tick += 1
                ref = self.play_at[0]
                if self.current_tick > ref:
                    # print("Playing : {}".format(self.play_at))
                    self.play_at.pop(0)
                    if len(self.play_at) >= 1:
                        self.play(True)
            else:
                self.current_tick = 0
                self.compute_next_ticks()
        # print("Recomputed : {}".format(self.play_at))

    def chop_interval(self, num, prec, max, len):
        values = []
        num += 1
        for i in range(num):
            values.append(randint(0, prec))
        norm = sum(values)
        anc = 0
        max_ar = max - 1.5 * len * num
        for i in range(num):
            old = values[i]
            values[i] += anc
            anc += old
            values[i] /= norm
            values[i] *= max_ar + i * 1.5 * len
            values[i] = int(values[i])
        return values
