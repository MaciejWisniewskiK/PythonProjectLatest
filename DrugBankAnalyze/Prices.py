# Task 12
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Used once to hand-pick the single-serving units
def _get_all_price_units(xml_file : str) -> set[str]:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    price_units = set()

    for drug in root.findall("db:drug", ns):
        for price in drug.findall("db:prices/db:price", ns):
            price_units.add(price.find("db:unit", ns).text)

    return price_units

# Hand picked from the output of _get_all_price_units
single_serving_units = {
    "ampule",
    "capsule",
    "dose",
    "each",
    "implant",
    "softgel capsule",
    "syringe",
    "tablet",
    "vial",
}

def get_prices(xml_file : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    data = {
        "DrugBank ID": [],
        "Name": [],
        "State": [],
        "Average price per serving": [],
    }

    for drug in root.findall("db:drug", ns):
        data["DrugBank ID"].append(drug.find("db:drugbank-id", ns).text)
        data["Name"].append(drug.find("db:name", ns).text)
        data["State"].append(drug.find("db:state", ns).text)

        prices_per_serving = []
        for price in drug.findall("db:prices/db:price", ns):
            unit = price.find("db:unit", ns).text

            cost_obj = price.find("db:cost", ns)
            cost = float(cost_obj.text)
            currency = cost_obj.get("currency")

            if unit in single_serving_units and currency == "USD":
                prices_per_serving.append(cost)       

        avg_price_per_serving = np.mean(prices_per_serving) if len(prices_per_serving) > 0 else None
        data["Average price per serving"].append(avg_price_per_serving)

    df = pd.DataFrame(data)
    df = df[df["Average price per serving"].notnull()]

    return df

def plot_prices(xml_file : str) -> None:
    df = get_prices(xml_file)

    plt.figure(figsize=(12, 6))
    sns.boxplot(x="State", y="Average price per serving", data=df)
    plt.yscale("log")
    plt.xlabel("State")
    plt.ylabel("Average Price per Serving (USD)")
    plt.title("Comparison of Drug Prices by State")
    plt.show()