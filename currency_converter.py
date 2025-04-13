from datetime import datetime, timedelta
import requests
import logging

EXCHANGE_API_ENDPOINT = "https://api.exchangerate-api.com/v4/latest/USD"


class CurrencyConverter:
    _cached_rates = None
    _logger_instance = None
    _last_update_time = None
    _CACHE_EXPIRY = timedelta(hours=1)

    @classmethod
    def _init_logging(cls):
        if cls._logger_instance is None:
            cls._logger_instance = logging.getLogger("ExchangeRateLogger")
            cls._logger_instance.setLevel(logging.INFO)

            if not cls._logger_instance.handlers:
                console_handler = logging.StreamHandler()
                log_format = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                console_handler.setFormatter(log_format)
                cls._logger_instance.addHandler(console_handler)

    @classmethod
    def _refresh_rates_if_needed(cls):
        if (
                cls._cached_rates is None
                or cls._last_update_time is None
                or (datetime.now() - cls._last_update_time) > cls._CACHE_EXPIRY
        ):
            cls._init_logging()
            cls._logger_instance.info("Updating currency rates from external API")

            try:
                api_response = requests.get(EXCHANGE_API_ENDPOINT)
                api_response.raise_for_status()

                rate_data = api_response.json()
                cls._cached_rates = rate_data.get("rates", {})
                cls._last_update_time = datetime.now()

                cls._logger_instance.info("Successfully updated exchange rates")
            except requests.RequestException as api_error:
                cls._logger_instance.error(f"API request failed: {api_error}")
                raise ConnectionError("Could not fetch exchange rates") from api_error

    @classmethod
    def convert(cls, value_usd: float, target_currency_code: str) -> float:
        cls._init_logging()
        cls._refresh_rates_if_needed()

        currency_code = target_currency_code.upper()
        conversion_rate = cls._cached_rates.get(currency_code)

        if conversion_rate is None:
            cls._logger_instance.error(f"No exchange rate found for {currency_code}")
            raise ValueError(f"Unsupported currency: {currency_code}")

        cls._logger_instance.info(
            f"Converting {value_usd} USD to {currency_code} (Rate: {conversion_rate})"
        )
        return value_usd * conversion_rate