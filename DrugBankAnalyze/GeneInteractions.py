# Task 11
import pandas as pd
import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def get_gene_drug_interactions(xml_file : str, gene_name : str) -> pd.DataFrame:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    data = {
        "drug_id": [],
        "drug_name": [],
        "products": [],
    }

    for drug in root.findall("db:drug", ns):
        for target in drug.findall("db:targets/db:target", ns):
            polypeptide = target.find("db:polypeptide", ns)
            if polypeptide is None:
                continue
            if polypeptide.find("db:gene-name", ns).text != gene_name:
                continue

            data["drug_id"].append(drug.find("db:drugbank-id", ns).text)
            data["drug_name"].append(drug.find("db:name", ns).text)
            
            products = set()
            for product in drug.findall("db:products/db:product", ns):
                products.add(product.find("db:name", ns).text)
            
            data["products"].append(products)
                    
    return pd.DataFrame(data)

def gene_drug_interaction_graph(xml_file : str, gene_name : str) -> None:
    df = get_gene_drug_interactions(xml_file, gene_name)
    
    G = nx.Graph()
    G.add_node(gene_name, label=gene_name, node_type="gene")

    for drug_id, drug_name, products in zip(df["drug_id"], df["drug_name"], df["products"]):
        G.add_node(drug_id, label=drug_name, node_type="drug")
        G.add_edge(gene_name, drug_id)

        for product in products:
            G.add_node(product, label=product, node_type="product")
            G.add_edge(drug_id, product)
    
    pos = {}

    gene_node = [node for node in G.nodes if G.nodes[node]["node_type"] == "gene"][0]
    drug_nodes = [node for node in G.nodes if G.nodes[node]["node_type"] == "drug"]
    product_nodes = [node for node in G.nodes if G.nodes[node]["node_type"] == "product"]

    pos[gene_node] = (0, 0.5)

    y_positions = np.linspace(0, 1, len(drug_nodes))
    for i, node in enumerate(drug_nodes):
        pos[node] = (0.5, y_positions[i])
    
    y_positions = np.linspace(0, 1, len(product_nodes) + len(drug_nodes))
    for i, node in enumerate(product_nodes):
        parent_node_nr = drug_nodes.index([n for n in G.neighbors(node)][0])
        pos[node] = (1, y_positions[i + parent_node_nr])
        

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10)
    plt.title(f"Gene {gene_name} - Drug Interactions")
    plt.show()
