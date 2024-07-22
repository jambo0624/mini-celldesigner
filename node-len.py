import json


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_positions(species_aliases):
    positions = {}
    for aliases in species_aliases:
        aliases_id = aliases['@id']
        bounds = aliases['celldesigner:bounds']
        positions[aliases_id] = {
            'x': float(bounds['@x']),
            'y': float(bounds['@y'])
        }
    return positions


def create_nodes(species_aliases, positions, species):
    nodes = {}
    for aliases in species_aliases:
        aliases_id = aliases['@id']
        species_id = aliases['@species']

        bigg_id = next((_sp['@name'] for _sp in species if _sp['@id'] == species_id), "")

        if aliases_id in positions:
            node = {
                'bigg_id': bigg_id,
                'name': species_id,
                "node_type": "metabolite",
                "x": positions[aliases_id]["x"],
                "y": positions[aliases_id]["y"],
                "label_x": positions[aliases_id]["x"],
                "label_y": positions[aliases_id]["y"],
                "node_is_primary": False,
            }

            nodes.setdefault(aliases_id, node)
    return nodes




# Load your original JSON data
data = load_json_data('SBML_origin_quarter.json')


# Extract necessary components
species_aliases = data['sbml']['model']['layout:listOfLayouts']['layout:layout']['layout:listOfSpeciesGlyphs']['layout:speciesGlyph']
reactions = data['sbml']['model']['listOfReactions']['reaction']
species = data['sbml']['model']['listOfSpecies']['species']

print(len(species), 'species')
print(len(reactions), 'reactions')
print(len(species_aliases), 'species_aliases')
# Extract positions
# positions = extract_positions(species_aliases)

# Create nodes and edges
# nodes = create_nodes(species_aliases, positions, species)


# Save the new JSON data
