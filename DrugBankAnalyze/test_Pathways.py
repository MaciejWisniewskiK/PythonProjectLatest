from DrugBankAnalyze.Pathways import get_pathways
from DrugBankAnalyze.Util import is_valid_drugbank_id
import pandas as pd

def test_get_pathways():
    xml_file = "data/drugbank_partial.xml"
    df = get_pathways(xml_file)

    for pathway, row in df.iterrows():
        drugs = row["drugs"]
        assert all(is_valid_drugbank_id(id) for id in list(drugs))
    
