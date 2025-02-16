from DrugBankAnalyze.ProductSummary import product_summary

def test_product_summary():
    xml_file = "data/drugbank_partial.xml"
    drug_id = "DB00001"
    df = product_summary(xml_file, drug_id)

    assert df.shape[0] == 4