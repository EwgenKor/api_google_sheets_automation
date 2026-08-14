def convert_to_eur(
    purchase_price: float,
    currency: str,
    rates: dict[str, float],
) -> float:
    if purchase_price < 0:
        raise ValueError("Purchase price cannot be negative")

    currency = currency.upper()

    if currency == "EUR":
        return round(purchase_price, 2)

    if currency not in rates:
        raise ValueError(
            f"Exchange rate is missing for currency: {currency}"
        )

    rate = rates[currency]

    if rate <= 0:
        raise ValueError(
            f"Invalid exchange rate for currency {currency}: {rate}"
        )

    cost_eur = purchase_price / rate

    return round(cost_eur, 2)


def calculate_margin_percent(
    cost_eur: float,
    selling_price_eur: float,
) -> float:
    if cost_eur < 0:
        raise ValueError("Cost cannot be negative")

    if selling_price_eur <= 0:
        raise ValueError("Selling price must be greater than zero")

    margin_percent = (
        (selling_price_eur - cost_eur)
        / selling_price_eur
        * 100
    )

    return round(margin_percent, 2)