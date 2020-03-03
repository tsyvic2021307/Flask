import scraper


def test_stripMoney():
    assert scraper.stripMoney("$3") == 3

def test_priceProcess():
    mini, maxi, ave = scraper.priceProcess([{'title': 'Example Title', 'price': '$1.50', 'url': 'https://www.trademe.co.nz/computers'}, {'title': 'Example Title2', 'price': '$3', 'url': 'https://www.trademe.co.nz/computers'}])
    assert mini == 1.5
    assert maxi == 3
    assert ave == 2.25