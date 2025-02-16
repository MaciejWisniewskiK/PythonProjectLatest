# Task 9
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from DrugBankAnalyze.Util import autopct_gen

def get_research_states(xml_file : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}
    
    data = {
        "id": [],
        "approved": [],
        "withdrawn": [],
        "experimental": [],
        "vet_approved": []
    }

    for drug in root.findall("db:drug", ns):
        data["id"].append(drug.find("db:drugbank-id", ns).text)
        data["approved"].append(False)
        data["withdrawn"].append(False)
        data["experimental"].append(False)
        data["vet_approved"].append(False)

        for group in drug.findall("db:groups/db:group", ns):
            if group.text == "approved":
                data["approved"][-1] = True
            elif group.text == "withdrawn":
                data["withdrawn"][-1] = True
            elif group.text == "experimental" or group.text == "investigational":
                data["experimental"][-1] = True
            elif group.text == "vet_approved":
                data["vet_approved"][-1] = True

    return pd.DataFrame(data)

def _dominating_state(row):
    if row["withdrawn"]:
        return "withdrawn"
    if row["vet_approved"]:
        return "vet_approved"
    if row["approved"]:
        return "approved"
    if row["experimental"]:
        return "experimental"
    return "unknown"

def research_state_pie_chart(xml_file : str) -> None:
    df = get_research_states(xml_file)
    df["state"] = df.apply(_dominating_state, axis=1)
    state_counts = df["state"].value_counts()

    plt.figure(figsize=(10, 10))
    plt.pie(state_counts, autopct=autopct_gen(3), labels=state_counts.index)
    plt.title("Drug research states")
    plt.show()
