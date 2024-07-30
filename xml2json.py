import xmltodict
import json

# read the XML file
with open('SBML_origin_quarter.xml', 'r', encoding='utf-8') as xml_file:
    xml_content = xml_file.read()

# convert the XML content to a dictionary
xml_dict = xmltodict.parse(xml_content)

# convert the dictionary to a JSON string
json_data = json.dumps(xml_dict, indent=4)

# save the JSON string to a file
with open('SBML_origin_quarter.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("XML to JSON conversion completed.")