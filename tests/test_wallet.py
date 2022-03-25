from dto.wallet import CurrencyWallet, Wallet


def test_currency_wallet__case1():
    """buying 200 XRP for 20 CZK each, then selling 200 XRP for 22. Should be 400,- in profit."""

    currency_wallet = CurrencyWallet("XRP")
    currency_wallet.buy(200, 20)
    profit = currency_wallet.spend(200, 22)

    assert profit == 400


def test_currency_wallet__case2():
    """buying 200 XRP for 20 CZK each, then selling 200 XRP for 18. Should be -400,- in profit."""

    currency_wallet = CurrencyWallet("XRP")
    currency_wallet.buy(200, 20)
    profit = currency_wallet.spend(200, 18)

    assert profit == -400


def test_currency_wallet__case3():
    """buying 200 XRP for 20 CZK each, then selling 150 XRP for 22. Should be 300,- in profit."""

    currency_wallet = CurrencyWallet("XRP")
    currency_wallet.buy(200, 20)
    profit = currency_wallet.spend(150, 22)

    assert profit == 300


def test_wallet__czkt_case1():
    """
    Buying 200 XRP for 20 CZKT (hypothetical czech stablecoin simulating crypto asset). Selling 200 XRP for 22 CZKT.
    Should have in my wallet 0 XRP, 4400 CZKT and 400 CZK in profit
    """

    wallet = Wallet()
    wallet.buy("CZKT", 4000, 1)
    profit = wallet.convert(
        currency_from="CZKT",
        currency_to="XRP",
        count_from=4000,
        currency_from_current_price=1,
        currency_to_current_price=20
    )

    assert wallet.currencies["XRP"].count == 200
    assert wallet.currencies["CZKT"].count == 0
    assert profit == 0

    profit = wallet.convert(
        currency_from="XRP",
        currency_to="CZKT",
        count_from=200,
        currency_from_current_price=22,
        currency_to_current_price=1
    )

    assert wallet.currencies["XRP"].count == 0
    assert wallet.currencies["CZKT"].count == 4400
    assert profit == 400


def test_wallet__czkt_case2():
    """
    Buying 200 XRP for 20 CZKT (hypothetical czech stablecoin simulating crypto asset). Selling 150 XRP for 22 CZKT.
    Should have in my wallet 50 XRP, 3300 CZKT and 300 CZK in profit
    """

    wallet = Wallet()
    wallet.buy("CZKT", 4000, 1)
    profit = wallet.convert(
        currency_from="CZKT",
        currency_to="XRP",
        count_from=4000,
        currency_from_current_price=1,
        currency_to_current_price=20
    )

    assert wallet.currencies["XRP"].count == 200
    assert wallet.currencies["CZKT"].count == 0
    assert profit == 0

    profit = wallet.convert(
        currency_from="XRP",
        currency_to="CZKT",
        count_from=150,
        currency_from_current_price=22,
        currency_to_current_price=1
    )

    assert wallet.currencies["XRP"].count == 50
    assert wallet.currencies["CZKT"].count == 3300
    assert profit == 300


def test_wallet__xrp_eth():
    """
    Buying 12000 XRP (0.5 CZK) for 1.5 ETH (4000 CZK) - conversion ratio is 8000.
    Then price goes to 2 CZK for XRP and 2000 CZK for ETH - conversion ratio is 1000.
    Then selling everything to CZK.
    Should be 18000 CZK profit on XRP and 3000 loss on ETH
    """

    wallet = Wallet()
    wallet.buy("ETH", 3, 4000)
    profit = wallet.convert(
        currency_from="ETH",
        currency_to="XRP",
        count_from=1.5,
        currency_from_current_price=4000,
        currency_to_current_price=0.5
    )

    assert wallet.currencies["ETH"].count == 1.5
    assert wallet.currencies["XRP"].count == 12000
    assert profit == 0

    profit = wallet.convert(
        currency_from="ETH",
        currency_to="CZK",
        count_from=1.5,
        currency_from_current_price=2000,
        currency_to_current_price=1
    )

    assert wallet.currencies["ETH"].count == 0
    assert wallet.currencies["CZK"].count == 3000
    assert profit == -3000

    profit = wallet.convert(
        currency_from="XRP",
        currency_to="CZK",
        count_from=12000,
        currency_from_current_price=2,
        currency_to_current_price=1
    )

    assert wallet.currencies["XRP"].count == 0
    assert wallet.currencies["CZK"].count == 3000 + 24000
    assert profit == 18000
