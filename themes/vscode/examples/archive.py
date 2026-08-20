"""Classify observations before committing them to the Helsing archive."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol


class Threat(StrEnum):
    CLEAR = "clear"
    OBSERVED = "observed"
    SEVERE = "severe"


@dataclass(frozen=True, slots=True)
class Observation:
    subject: str
    shadows: int
    invited: bool = False
    recorded_at: datetime = datetime.now(UTC)


class Archive(Protocol):
    async def store(self, observation: Observation, threat: Threat) -> None: ...


def classify(observation: Observation) -> Threat:
    match observation:
        case Observation(invited=True):
            return Threat.CLEAR
        case Observation(shadows=count) if count >= 3:
            return Threat.SEVERE
        case Observation(shadows=count) if count > 0:
            return Threat.OBSERVED
        case _:
            return Threat.CLEAR


async def record(archive: Archive, observation: Observation) -> str:
    threat = classify(observation)
    await archive.store(observation, threat)
    return f"{observation.subject}: {threat.value}"
