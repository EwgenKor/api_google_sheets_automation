import requests


BASE_URL = "https://api.frankfurter.dev/v2/rates"


def fetch_exchange_rates(
    base_currency: str = "EUR",
    target_currencies: list[str] | None = None,
) -> dict[str, float]:
    params = {
        "base": base_currency,
    }

    if target_currencies:
        params["quotes"] = ",".join(target_currencies)

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Unexpected API response: expected a list")

    rates = {}

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Unexpected API response item")

        quote = item.get("quote")
        rate = item.get("rate")

        if not quote or not isinstance(rate, (int, float)):
            raise ValueError(
                f"Invalid exchange rate item: {item}"
            )

        rates[quote] = float(rate)

    return rates


if __name__ == "__main__":
    rates = fetch_exchange_rates(
        base_currency="EUR",
        target_currencies=["USD", "GBP"],
    )

    print(rates)