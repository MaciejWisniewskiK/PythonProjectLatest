import random
import copy
import xml.etree.ElementTree as ET

def generate_new_drugs(original_drugs : list[ET.Element], first_id : int, last_id : int, out_xml : str) -> None:
    """
        Generate new drugs with incrementing IDs and values randomly chosen from original ones.
    """
    ns = {'db': 'http://www.drugbank.ca'}

    with open(out_xml, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(b'<drugbank xmlns="http://www.drugbank.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.drugbank.ca http://www.drugbank.ca/docs/drugbank.xsd" version="5.1" exported-on="2024-03-14">\n')

        for drug in original_drugs:
            f.write(ET.tostring(drug, encoding="utf-8"))
            f.write(b'\n')
         
        for i in range(first_id, last_id + 1):
            new_id = f"DB{i:05d}"
            new_drug = copy.deepcopy(random.choice(original_drugs))
            new_drug.find("db:drugbank-id", ns).text = new_id

            f.write(ET.tostring(new_drug, encoding="utf-8"))
            f.write(b'\n')

            if i % 100 == 0:
                f.flush()
                
        f.write(b'</drugbank>')