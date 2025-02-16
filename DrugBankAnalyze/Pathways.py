# Tasks 4,5,6
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from DrugBankAnalyze.Util import cap_str

#def get_pathways(xml_file : str) -> pd.DataFrame:
#    tree = ET.parse(xml_file)
#    root = tree.getroot()
#    ns = {'db': 'http://www.drugbank.ca'}
#
#    data = dict()
#
#    for drug in root.findall("db:drug", ns):
#        drug_id = drug.find("db:drugbank-id", ns).text
#
#        for pathway in drug.findall("db:pathways/db:pathway", ns):
#            smpdb_id = pathway.find("db:smpdb-id", ns).text
#            drugs = {id.text for id in pathway.findall("db:drugs/db:drug/db:drugbank-id", ns)}
#            drugs.add(drug_id)
#
#            if smpdb_id not in data:
#                data[smpdb_id] = {
#                    "name": pathway.find("db:name", ns).text, 
#                    "category": pathway.find("db:category", ns).text, 
#                    "drugs": drugs
#                }
#            else:
#                data[smpdb_id]["drugs"].update(drugs)
#
#    return pd.DataFrame(data).T

def get_pathways(xml_file : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    data = dict()

    for drug in root.findall("db:drug", ns):
        for target in drug.findall("db:targets/db:target", ns):
            for go_c in target.findall("db:polypeptide/db:go-classifiers/db:go-classifier", ns):
                desc = go_c.find("db:description", ns).text
                if desc.endswith("pathway"):
                    if desc not in data:
                        data[desc] = {"drugs" : {drug.find("db:drugbank-id", ns).text}}
                    else:
                        data[desc]["drugs"].add(drug.find("db:drugbank-id", ns).text)

    return pd.DataFrame(data).T

def _get_drug_set(xml_file : str) -> set[str]:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    return {drug.find("db:drugbank-id", ns).text for drug in root.findall("db:drug", ns)}


def visualise_drug_pathway_interactions(xml_file : str):
    pathways = get_pathways(xml_file)

    pathway_set = set(pathways.index)
    drug_set = _get_drug_set(xml_file)

    drug_pathway_df = pd.DataFrame(0, index=list(drug_set), columns=list(pathway_set))
    for p in pathways.index:
        for d in pathways.loc[p, "drugs"]:
            drug_pathway_df.loc[d, p] = 1

    short_labels = {col : cap_str(col, 15) for col in drug_pathway_df.columns}
    drug_pathway_df = drug_pathway_df.rename(columns=short_labels).sort_index()
    
    plt.figure(figsize=(20, 20))
    hm = sns.heatmap(drug_pathway_df,
                    cmap="YlGnBu",
                    cbar=False,
                    linewidths=0.5,
                    linecolor='gray',
                    square=True)

    hm.set_xticklabels(hm.get_xticklabels(), rotation=45, ha="right", fontsize=8)

    hm.set_yticks(np.arange(drug_pathway_df.shape[0]) + 0.5)
    hm.set_yticklabels(drug_pathway_df.index, rotation=0, fontsize=8)

    plt.xlabel("Pathways")
    plt.ylabel("Drug IDs")
    plt.title("Drug-Pathway Interactions")

    plt.tight_layout()
    plt.show()

def number_of_pathways_histogram(xml_file : str):
    pathways = get_pathways(xml_file)
    drugs = sorted(list(_get_drug_set(xml_file)))
    
    df = pd.DataFrame(0, index=drugs, columns=["Number of Pathways"])

    for p in pathways.index:
        for d in pathways.loc[p, "drugs"]:
            df.loc[d, "Number of Pathways"] += 1
    
    plt.figure(figsize=(20,10))
    plt.bar(df.index, df["Number of Pathways"])

    plt.xlabel("Drug ID")
    plt.ylabel("Number of Pathways")
    plt.title("Number of Pathways Each Drug Interacts With")

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()