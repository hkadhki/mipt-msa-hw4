from currency_converter import CurrencyConverter

# Список валют для конвертации
CURRENCIES = ["RUB", "EUR", "GBP", "CNY"]


def main():
    try:
        amount = float(input("Введите значение в USD:\n"))
    except ValueError:
        print("Некорректный ввод. Введите число.")
        return

    for currency in CURRENCIES:
        try:
            result = CurrencyConverter.convert(amount, currency)
            print(f"{amount} USD to {currency}: {result:.2f}")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()