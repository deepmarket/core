from datetime import datetime
from functools import wraps
from os import environ
from random import uniform

from requests import post

SLOTS: int = 4

if environ.get("API_PRICING_ENDPOINT"):
    api_endpoint: str = environ.get("API_PRICING_ENDPOINT")
else:
    api_endpoint: str = "http://pacific.cs.pdx.edu/api/v1/pricing"

class Prices(object):

    def __init__(self, _min: float=0.01, _max: float=0.0001):
        self._min_max_price: tuple = (_min, _max)
        
        self.date_today: datetime = datetime.today()

        self.cpu_prices: [float] = [0.0] * SLOTS
        self.gpu_prices: [float] = [0.0] * SLOTS
        self.memory_prices: [float] = [0.0] * SLOTS
        self.disk_prices: [float] = [0.0] * SLOTS

        self.prices_tuple: tuple = (self.cpu_prices, self.gpu_prices, self.memory_prices, self.disk_prices)

        self.prices_data = {
            "cpu": self.cpu_prices,
            "gpu": self.gpu_prices,
            "memory": self.memory_prices,
            "disk_space": self.disk_prices
        }

    def __repr__(self):
        pass
    
    def __str__(self):
        return f""" CPU: {self.cpu_prices}
                    GPU: {self.gpu_prices}
                    MEMORY: {self.memory_prices}
                    DISK: {self.disk_prices}
                """

    def _update_prices_dict(self):
        self.prices_data = {
            "cpu": self.cpu_prices,
            "gpu": self.gpu_prices,
            "memory": self.memory_prices,
            "disk_space": self.disk_prices
        }

    def generate_prices(self):
        self.cpu_prices = [uniform(*self._min_max_price) for _ in range(SLOTS)]
        self.gpu_prices = [uniform(*self._min_max_price) for _ in range(SLOTS)]
        self.memory_prices = [uniform(*self._min_max_price) for _ in range(SLOTS)]
        self.disk_prices = [uniform(*self._min_max_price) for _ in range(SLOTS)]
        
        # TODO: Can change to one liner but probably less trivial; note: have to update `update_prices_dict` tho :/
        # self.prices_tuple = tuple([[uniform(*self._min_max_price) for _ in range(SLOTS)] for _ in self.prices_tuple])
        
        # Update new prices
        self._update_prices_dict()

        # Allow chaining
        return self

    def submit_prices(self):
        for slot in range(SLOTS):
            
            price_data = {
                "time_slot": slot,
                "cpus": self.prices_data["cpu"][slot],
                "gpus": self.prices_data["gpu"][slot],
                "memory": self.prices_data["memory"][slot],
                "disk_space": self.prices_data["disk_space"][slot],
                "createdOn": self.date_today,
                "updatedOn": self.date_today,
            }

            print(price_data)
            res = post(api_endpoint, price_data)
            
            print()

            if res.status_code is not 200:
                raise ValueError(f"Could not post prices to {api_endpoint}\n{res}")

        # return res.response

        return self
    