import xml.etree.ElementTree as ET
import copy

def parse(xml_file : str) -> tuple[list[ET.Element], int, ET.Element]:
    """
    Parse the xml file and return the list of drugs, the largest drug id (numeric), and the root element of the xml tree.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'db': 'http://www.drugbank.ca'}

    drugs = []
    max_id = 0

    for drug in root.findall("db:drug", ns):
        drug_id = drug.find("db:drugbank-id", ns).text
        numeric_id = int(drug_id[2:])
        max_id = max(max_id, numeric_id)

        drugs.append(copy.deepcopy(drug))
    
    return drugs, max_id, root

