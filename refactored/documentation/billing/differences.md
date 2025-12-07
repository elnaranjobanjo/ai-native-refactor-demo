# Parity Guarantees
- Processing order (pricing → discounts → shipping → tax → rounding) mirrors the legacy implementation.
- Default policies keep the same threshold (100), shipping fees (5/15), tax rate (22%), and type names (`product`, `service`, `discount`).
- Public `handle` still accepts iterables of dict-like line items and returns a rounded float.

# Improvements
- Responsibility separation means product/service pricing, discounts, shipping, and taxes can evolve independently.
- Dataclass configs expose official knobs for thresholds, fees, and tax rates instead of hidden constants.
- Deterministic injection points allow dependency overrides for testing or region-specific rules.
- Duplicate conditions and unused helpers were removed, reducing risk of divergent logic paths.

# Remaining Risks / Follow-ups
- Input validation remains minimal; malformed dicts will still raise `KeyError` similar to legacy behavior.
- No logging/telemetry is emitted when unsupported item types are ignored—could add structured warnings later.
