from dataclasses import dataclass


@dataclass(frozen=True)
class Share:
    x: int
    y: int
