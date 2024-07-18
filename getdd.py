import json


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



# Load your original JSON data
data = load_json_data('SBML_origin_quarter_3.json')


# Create nodes and edges
nodes = data[0]['nodes']
edges = data[0]['reactions']

cytoscape_data = [{
    "map_name": "RECON1.Glycolysis TCA PPP",
    "map_id": "3f685e1b934e33e5471b1a56540bbabe",
    "map_description": "\nLast Modified Tue Jun 18 2024 10:43:50 GMT+0100 (Irish Standard Time)",
    "homepage": "https://escher.github.io",
    "schema": "https://escher.github.io/escher/jsonschema/1-0-0#"
},
    {
        "reactions": edges,
        "nodes": nodes,
        "text_labels": {},
        "canvas": {
            "x": 4000,
            "y": 8000,
            "width": 40000,
            "height": 32000
        }
    }
]

# Save the new JSON data
save_json_data(cytoscape_data, 'escher-SBML_origin_quarter_3.json')
