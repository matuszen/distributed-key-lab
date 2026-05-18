"""Shared type definitions for domain modules."""

from dataclasses import dataclass

from ecdsa.ellipticcurve import Point


@dataclass(frozen=True)
class Share:
    x: int
    y: int


@dataclass(frozen=True)
class VSSPackage:
    share: Share
    commitments: list[Point]
