import json
import re
from datetime import datetime

def infer_type(value):
    if isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float'
    elif isinstance(value, str):
        date_format = "%Y-%m-%d"
        try:
            if datetime.strptime(value, date_format):
                return 'date'
        except ValueError:
            pass

        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return 'email'

        return 'str'
    else:
        return type(value).__name__

def extract_structure(data):
    if isinstance(data, dict):
        return {key: extract_structure(value) for key, value in data.items()}
    elif isinstance(data, list):
        if data:
            return [extract_structure(data[0])]
        return []
    else:
        return infer_type(data)


def json_to_structure(json_file_path, output_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    structure = extract_structure(data)

    with open(output_file_path, 'w') as file:
        json.dump(structure, file, indent=4)


json_to_structure('SBML_new_PPP_6.json', 'path_to_output_json_file.json')