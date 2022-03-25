import csv

import iso8601

from api import CryptoAPI
from dto import Order
from .reader import Reader


class GateIOReader(Reader):
    PICKLE_FILENAME = "gate_io.pkl"
    EXCHANGE_NAME = "Gate.io"

    def __init__(self):
        self.api = CryptoAPI()

    def get_pickle_filename(self):
        return self.PICKLE_FILENAME

    def read_file(self, filename):
        fr = open(filename, "r")
        csvreader = csv.reader(fr, delimiter="\t", quotechar='"')
        header = next(csvreader)

        records = []
        for row in csvreader:
            dt_row = dict((x, y) for x, y in zip(header, row))

            if dt_row["Status"] != "Done":
                continue

            filled = iso8601.parse_date(dt_row["Time"])

            if dt_row["Type"] == "Buy":
                currency_to, currency_from = dt_row["Pairs"].split("/")
                count = float(dt_row["In Order"].split(" ")[0])
            if dt_row["Type"] == "Sell":
                currency_from, currency_to = dt_row["Pairs"].split("/")
                count = float(dt_row["Amount"].split(" ")[0])

            # price at order time, will be used to for taxing
            unit_price = self.api.get_currency_price_at(currency_from, filled)

            records.append(Order(
                filled=filled,
                currency_from=currency_from,
                currency_to=currency_to,
                count=count,
                unit_price=unit_price,
                exchange_name=self.EXCHANGE_NAME
            ))

        return records
