from dataclasses import dataclass
from typing import Optional, List

from src.models.channel import Channel


@dataclass(frozen=True)
class Environment:
    id: str
    name: str
    src_url: Optional[str]
    channels: List[Channel]
    attribution: str  # Attribution for the mix
