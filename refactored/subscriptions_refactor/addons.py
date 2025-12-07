"""Addon fee accumulation for subscriptions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class AddonConfig:
    addon_type: str = "addon"


class AddonCalculator:
    def __init__(self, config: AddonConfig | None = None) -> None:
        self._config = config or AddonConfig()

    def calculate(self, record: Mapping[str, Any]) -> float:
        if record.get("type") != self._config.addon_type:
            return 0.0
        return float(record.get("monthly_cost", 0.0))

    def sum_addons(self, records: Iterable[Mapping[str, Any]]) -> float:
        total = 0.0
        for record in records:
            total += self.calculate(record)
        return total


def sum_addons(records: Iterable[Mapping[str, Any]], config: AddonConfig | None = None) -> float:
    calculator = AddonCalculator(config=config)
    return calculator.sum_addons(records)
