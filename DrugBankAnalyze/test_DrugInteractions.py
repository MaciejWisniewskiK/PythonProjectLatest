from DrugBankAnalyze.DrugInteractions import get_drug_interactions
import pandas as pd
import pytest
from DrugBankAnalyze.Util import is_valid_drugbank_id

def test_get_drug_interactions():
    xml_file = "data/drugbank_partial.xml"
    drug_id = "DB00001"
    df = get_drug_interactions(xml_file, drug_id)

    assert all(is_valid_drugbank_id(id) for id in df["id"])
    assert df["id"].is_unique
    assert drug_id not in df["id"]