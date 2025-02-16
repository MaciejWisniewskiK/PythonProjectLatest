from DrugBankAnalyze.DrugSummary import drug_summary
import pandas as pd
import pytest
from DrugBankAnalyze.Util import is_valid_drugbank_id

def test_drug_summary():
    xml_file = "data/drugbank_partial.xml"
    df = drug_summary(xml_file)

    assert df["DrugBank ID"].is_unique
    assert all(is_valid_drugbank_id(id) for id in df["DrugBank ID"])
    assert all(state in {"liquid", "solid", "gas"} for state in df["State"].unique())


