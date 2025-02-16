from DrugBankAnalyze.Prices import get_prices
from DrugBankAnalyze.Util import is_valid_drugbank_id

def test_get_prices():
    xml_file = "data/drugbank_partial.xml"
    df = get_prices(xml_file)

    assert all(is_valid_drugbank_id(id) for id in df["DrugBank ID"])
    assert all(price >= 0 for price in df["Average Price"])