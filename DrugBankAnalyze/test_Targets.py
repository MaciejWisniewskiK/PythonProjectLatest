from DrugBankAnalyze.Targets import get_targets

def test_get_targets():
    xml_file = "data/drugbank_partial.xml"
    df = get_targets(xml_file)

    assert df["DrugBank ID"].is_unique