from datetime import datetime

from src.calculations import calculate_margin_percent, convert_to_eur
from src.exchange_api import fetch_exchange_rates
from src.sheets import read_products, write_results


BASE_CURRENCY = "EUR"


def main():
    rows = read_products()

    if not rows:
        print("No products found in Google Sheet")
        return

    currencies = {
        row[2].upper()
        for row in rows
        if len(row) >= 3 and row[2].upper() != BASE_CURRENCY
    }

    rates = fetch_exchange_rates(
        base_currency=BASE_CURRENCY,
        target_currencies=sorted(currencies),
    )

    results = []

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for row in rows:
        if len(row) < 5:
            raise ValueError(
                f"Invalid product row: expected 5 columns, got {row}"
            )

        sku = row[0]
        product = row[1]
        currency = row[2].upper()

        try:
            purchase_price = float(row[3])
            selling_price_eur = float(row[4])
        except ValueError as exc:
            raise ValueError(
                f"Invalid numeric value for product {sku} ({product}): {row}"
            ) from exc

        cost_eur = convert_to_eur(
            purchase_price=purchase_price,
            currency=currency,
            rates=rates,
        )

        margin_percent = calculate_margin_percent(
            cost_eur=cost_eur,
            selling_price_eur=selling_price_eur,
        )

        if currency == BASE_CURRENCY:
            fx_rate = 1.0
        else:
            fx_rate = rates[currency]

        results.append(
            [
                fx_rate,
                cost_eur,
                margin_percent,
                updated_at,
            ]
        )

    response = write_results(results)

    updated_cells = response.get("updatedCells", 0)

    print(
        f"Successfully updated {len(results)} products "
        f"and {updated_cells} cells"
    )


if __name__ == "__main__":
    main()