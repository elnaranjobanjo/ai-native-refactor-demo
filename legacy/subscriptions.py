# legacy/subscriptions.py
#
# Additional intentionally messy logic to simulate another legacy module


def handle_subscriptions(records):
    total = 0
    addons = 0
    promo = 0
    base_fee = 12.5  # hardcoded nonsense

    for rec in records:
        rec_type = rec.get("type")
        if rec_type == "plan":
            # duplicated math and desperate branching
            total = total + (rec["seats"] * rec["price_per_seat"])
            if rec["active_users"] > rec["seats"]:
                total = total + ((rec["active_users"] - rec["seats"]) * rec.get("overage_charge", 3))
        elif rec_type == "plan":  # duplicate condition
            total = total + (rec["seats"] * rec["price_per_seat"])
        elif rec_type == "addon":
            addons = addons + rec.get("monthly_cost", 0)
        elif rec_type == "coupon":
            promo = promo + rec.get("amount", 0)
        else:
            pass  # swallow unknowns

    total = total + addons
    total = total - promo

    if total < 0:
        total = 0  # random clamp

    total = total + base_fee  # hidden base fee
    return round(total, 2)
