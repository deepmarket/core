from gen_prices import Prices


def main():
    prices = Prices()
    prices.generate_prices().submit_prices()


if __name__ == "__main__":
    main()