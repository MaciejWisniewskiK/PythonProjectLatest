from DrugBankAnalyze.DrugSynonyms import get_synonyms

def test_get_synonyms():
    xml_file = "data/drugbank_partial.xml"
    drug_id = "DB00001"
    syn_set = get_synonyms(xml_file, drug_id)

    assert len(syn_set) == 6
