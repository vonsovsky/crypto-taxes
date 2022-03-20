## Calculate cryptocurrency taxes

Goes through all transactions made in a given year on centralized exchanges and calculates taxable profit.

  * It is using weighted price averaging of given coins (alternatives are LIFO and FIFO)
  * Reference fiat currency is CZK (Česká koruna)
  * Only selling back to fiat and exchanging cryptocurrency for cryptocurrency is taxable in Czech republic,
    so HODL for life!

### Steps

  * Gathers all transactions from all centralized exchanges I used
  * Sorts them by date, filters out those outside of a given year 
  * Applies one by one, to keep counts and average prices of given coins
  * Sums up profits from exchanges

### TODO

  * Make adapters for more exchanges (at least those I used, obviously, to finish my task)
  * Resolve problem with selling some crypto money in the following year from buy
  * Attribute exchange fees (if not accounted in order history)
  * More precise API with prices (using CoinGecko now, which has resolution of a few hours)
  * Send a letter to the tax office using a lot of colors, clowns, unicorns and statement of how much I hate them
