# Tasks 7, 8
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from DrugBankAnalyze.Util import autopct_gen

def get_targets(xml_file : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}
    
    data = {
        "DrugBank ID": [],
        "Source": [],
        "External ID": [],
        "Name": [],
        "Gene Name": [],
        "GenAtlas ID": [],
        "Chromosome": [],
        "Cell Location": [],
    }

    for drug in root.findall("db:drug", ns):
        for target in drug.findall("db:targets/db:target", ns):
            polypeptide = target.find("db:polypeptide", ns)
            if polypeptide is None:
                continue

            data["DrugBank ID"].append(target.find("db:id", ns).text)
            data["Source"].append(polypeptide.get("source"))
            data["External ID"].append(polypeptide.get("id"))
            data["Name"].append(polypeptide.find("db:name", ns).text)
            data["Gene Name"].append(polypeptide.find("db:gene-name", ns).text)
            data["Chromosome"].append(polypeptide.find("db:chromosome-location", ns).text)
            data["Cell Location"].append(polypeptide.find("db:cellular-location", ns).text)
            
            for ext_id in polypeptide.findall("db:external-identifiers/db:external-identifier", ns):
                if ext_id.find("db:resource", ns).text == "GenAtlas":
                    data["GenAtlas ID"].append(ext_id.find("db:identifier", ns).text)
                    break
            if (len(data["GenAtlas ID"]) < len(data["DrugBank ID"])):
                data["GenAtlas ID"].append(None)

    df = pd.DataFrame(data)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

def target_cell_location_pie_chart(targets : pd.DataFrame) -> None:
    cell_location_counts = targets["Cell Location"].value_counts()
    plt.figure(figsize=(10, 10))
    plt.pie(cell_location_counts, autopct=autopct_gen(), labels=cell_location_counts.index)
    plt.title("Cell Locations")
    plt.show()