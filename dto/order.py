from datetime import datetime
from typing import Optional


class Order:
    def __init__(
            self,
            filled: datetime,
            currency_from: str,
            currency_to: str,
            count: float,
            count_to: Optional[float] = None,
            unit_price: Optional[float] = None,
            exchange_name: Optional[str] = None
    ):
        """
        only one of count_to and unit_price could be filled in
        """

        self.filled = filled
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.count = count
        self.count_to = count_to
        self.unit_price = unit_price
        self.exchange_name = exchange_name

    def __repr__(self):
        string_builder = ""
        if self.exchange_name is not None:
            string_builder += f"{self.exchange_name}: "

        if self.unit_price is not None:
            string_builder += f"{self.currency_from} to {self.currency_to}; " \
                              f"{self.count} for {self.unit_price} at {self.filled}"
        else:
            string_builder += f"{self.currency_from} to {self.currency_to}; " \
                              f"{self.count_to} for {self.count} at {self.filled}"

        return string_builder
