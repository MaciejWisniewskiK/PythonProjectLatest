from DrugBankAnalyze.GeneInteractions import get_gene_drug_interactions
from DrugBankAnalyze.Util import is_valid_drugbank_id

def test_get_gene_drug_interactions():
    xml_file = "data/drugbank_partial.xml"
    gene_name = "F2"
    df = get_gene_drug_interactions(xml_file, gene_name)

    assert all(is_valid_drugbank_id(id) for id in df["drug_id"])