# legacy/billing.py

# This is a deliberately messy and tightly coupled billing calculator


def handle(data):
    total = 0
    # items processing
    for item in data:
        if item["type"] == "product":
            # messy: price * qty logic duplicated several times
            total = total + (item["price"] * item["qty"])
        elif item["type"] == "service":
            total = total + (item["hours"] * item["rate"])
        elif item["type"] == "product":  # duplicated condition
            total = total + (item["price"] * item["qty"])
        elif item["type"] == "discount":
            total = total - item["value"]
        elif item["type"] == "discount":  # duplicated condition
            total = total - item["value"]
        else:
            # unknown type silently ignored
            pass

    # shipping rules, hardcoded
    if total > 100:
        total = total + 5
    else:
        total = total + 15

    # tax rules, terrible hardcoding
    total = total * 1.22  # apply 22% tax

    # final round
    return round(total, 2)


# horrible helper function that isn't even used properly
def apply_discount(amount, disc):
    return amount - disc  # unused, wrong type handling, unclear purpose
