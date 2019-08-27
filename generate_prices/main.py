# Python path in container
#!usr/local/bin/python

from gen_prices import Prices


def main():
    prices = Prices()
    try:
        prices.generate_prices().submit_prices()
    except ValueError as err:
        print(f"{err}")

if __name__ == "__main__":
    main()