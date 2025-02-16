# Task 1
import pandas as pd
import xml.etree.ElementTree as ET

def drug_summary(xml_file : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    data = {
        "DrugBank ID": [],
        "Name": [],
        "Type": [],
        "Description": [],
        "State": [],
        "Indication": [],
        "Mechanism of Action": [],
        "Food Interactions": [],
    }

    for drug in root.findall("db:drug", ns):
        data["DrugBank ID"].append(drug.find("db:drugbank-id", ns).text)
        data["Name"].append(drug.find("db:name", ns).text)
        data["Type"].append(drug.get("type"))
        data["Description"].append(drug.find("db:description", ns).text if drug.find("db:description", ns) is not None else None)
        data["State"].append(drug.find("db:state", ns).text)
        data["Indication"].append(drug.find("db:indication", ns).text if drug.find("db:indication", ns) is not None else None)
        data["Mechanism of Action"].append(drug.find("db:mechanism-of-action", ns).text if drug.find("db:mechanism-of-action", ns) is not None else None)
        data["Food Interactions"].append({food_interaction.text for food_interaction in drug.findall("db:food-interactions/db:food-interaction", ns)})

    return pd.DataFrame(data)
