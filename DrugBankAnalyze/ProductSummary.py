# Task 3
import pandas as pd
import xml.etree.ElementTree as ET

def product_summary(xml_file : str, drug_id : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    data = {
        "Drug Id": [],
        "Product name": [],
        "Labeller": [],
        "NDC": [],
        "Form": [],
        "Strength": [],
        "Route": [],
        "Country": [],
        "Source": [],
    }

    for drug in root.findall("db:drug", ns):
        if drug.find("db:drugbank-id", ns).text == drug_id:
            for product in drug.findall("db:products/db:product", ns):
                data["Drug Id"].append(drug_id)
                data["Product name"].append(product.find("db:name", ns).text)
                data["Labeller"].append(product.find("db:labeller", ns).text)
                data["NDC"].append(product.find("db:ndc-product-code", ns).text)
                data["Form"].append(product.find("db:dosage-form", ns).text)
                data["Strength"].append(product.find("db:strength", ns).text)
                data["Route"].append(product.find("db:route", ns).text)
                data["Country"].append(product.find("db:country", ns).text)
                data["Source"].append(product.find("db:source", ns).text)

    df = pd.DataFrame(data)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

