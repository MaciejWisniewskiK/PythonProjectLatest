from Parse import parse
from Generate import generate_new_drugs
import xml.etree.ElementTree as ET

og_xml = "data/drugbank_partial.xml"
out_xml = "data/drugbank_partial_and_generated.xml"
num_new_drugs = 200 #19900 explanation in demo_generated.ipynb

original_drugs, max_id, root = parse(og_xml)
new_drugs = generate_new_drugs(original_drugs, max_id + 1, max_id + num_new_drugs, out_xml)

