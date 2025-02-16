# Task 2
import pandas as pd
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from DrugBankAnalyze.Util import cap_str

def get_synonyms(xml_file : str, drug_id : str) -> set[str]:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    synonyms = {}

    for drug in root.findall("db:drug", ns):
        if drug.find("db:drugbank-id", ns).text == drug_id:
            synonyms = {synonym.text for synonym in drug.findall("db:synonyms/db:synonym", ns)}
    
    return synonyms

def visualize_synonyms(xml_file : str, drug_id : str) -> pd.DataFrame:
    synonyms = get_synonyms(xml_file, drug_id)
    synonyms = {cap_str(synonym, 15) for synonym in synonyms}

    G = nx.Graph()
    G.add_node(drug_id)
    G.add_nodes_from(synonyms)
    G.add_edges_from([(drug_id, synonym) for synonym in synonyms])

    plt.figure(figsize=(7, 7))
    nx.draw(G, with_labels=True, node_size=1500, node_color='skyblue', font_size=10, font_weight='bold')
    plt.title(f"Synonyms for {drug_id}")
    plt.show()