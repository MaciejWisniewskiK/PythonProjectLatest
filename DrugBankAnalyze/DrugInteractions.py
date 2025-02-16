# Task 10
import pandas as pd
import xml.etree.ElementTree as ET

def get_drug_interactions(xml_file : str, drug_id : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    data = {
        "id": [],
        "name": [],
        "description": [],
    }

    for drug in root.findall("db:drug", ns):
        if drug.find("db:drugbank-id", ns).text != drug_id:
            continue
        for interaction in drug.findall("db:drug-interactions/db:drug-interaction", ns):
            data["id"].append(interaction.find("db:drugbank-id", ns).text)
            data["name"].append(interaction.find("db:name", ns).text)
            data["description"].append(interaction.find("db:description", ns).text)
    
    return pd.DataFrame(data)

