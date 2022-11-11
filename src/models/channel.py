from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    id: str
    name: str
    filepath: str  # filepath of the sound file relative to the local audio directory
    mute: bool
    crossfade: bool
    volume: int
    balance: float  # -1.0 to 1.0 where 0.0 is center and -1.0 is 100% left and 1.0 is 100% right
    random: bool
    random_interval_count: int  # The number of times to play the sound in the random interval. Only used if random is True.
    random_interval_duration: int  # The duration of the random interval in seconds. Only used if random is True.
