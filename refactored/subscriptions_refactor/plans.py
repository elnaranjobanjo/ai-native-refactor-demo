"""Plan pricing calculations for subscriptions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class PlanPricingConfig:
    plan_type: str = "plan"
    default_overage_charge: float = 3.0


@dataclass(frozen=True)
class PlanCharge:
    seats: float
    price_per_seat: float
    active_users: float
    overage_charge: float

    @property
    def base_cost(self) -> float:
        return self.seats * self.price_per_seat

    @property
    def overage_cost(self) -> float:
        if self.active_users <= self.seats:
            return 0.0
        return (self.active_users - self.seats) * self.overage_charge

    @property
    def total(self) -> float:
        return self.base_cost + self.overage_cost


class PlanPricingEngine:
    def __init__(self, config: PlanPricingConfig | None = None) -> None:
        self._config = config or PlanPricingConfig()

    def _coerce_charge(self, record: Mapping[str, Any]) -> PlanCharge:
        return PlanCharge(
            seats=float(record["seats"]),
            price_per_seat=float(record["price_per_seat"]),
            active_users=float(record["active_users"]),
            overage_charge=float(record.get("overage_charge", self._config.default_overage_charge)),
        )

    def calculate(self, record: Mapping[str, Any]) -> float:
        if record.get("type") != self._config.plan_type:
            return 0.0
        charge = self._coerce_charge(record)
        return charge.total

    def sum_charges(self, records: Iterable[Mapping[str, Any]]) -> float:
        total = 0.0
        for record in records:
            total += self.calculate(record)
        return total


def sum_plan_charges(records: Iterable[Mapping[str, Any]], config: PlanPricingConfig | None = None) -> float:
    engine = PlanPricingEngine(config=config)
    return engine.sum_charges(records)
