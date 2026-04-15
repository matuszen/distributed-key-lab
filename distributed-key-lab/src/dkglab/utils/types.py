from dataclasses import dataclass
from ecdsa.ellipticcurve import Point

@dataclass(frozen=True)
class Share:
    x: int  # Participant index
    y: int  # Share value

@dataclass(frozen=True)
class VSSPackage:
    share: Share
    commitments: list[Point]