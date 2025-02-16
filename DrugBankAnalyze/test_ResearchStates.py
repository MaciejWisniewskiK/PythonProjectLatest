from DrugBankAnalyze.ResearchStates import get_research_states
from DrugBankAnalyze.Util import is_valid_drugbank_id

def test_get_research_states():
    xml_file = "data/drugbank_partial.xml"
    df = get_research_states(xml_file)

    assert all(is_valid_drugbank_id(id) for id in df["id"])
    
    for key in ["approved", "withdrawn", "experimental", "vet_approved"]:
        assert all(value in {0, 1} for value in df[key])