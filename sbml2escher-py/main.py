import xmltodict
import json

read_file_path = 'SBML_origin.xml'
write_file_path = 'SBML_origin.json'

# Read the XML file
with open(read_file_path, 'r', encoding='utf-8') as xml_file:
    xml_content = xml_file.read()

# Convert XML to dictionary
xml_dict = xmltodict.parse(xml_content)

# Convert the dictionary to JSON format
json_data = json.dumps(xml_dict, indent=4)

# Write the JSON data to a file
with open(write_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print(f"Conversion completed and saved as {write_file_path} file.")
