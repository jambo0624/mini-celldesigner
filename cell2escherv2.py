import json
import uuid


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


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


def get_metabolite_name(metabolite_id, nodes, is_primary=False):
    for _, node in nodes.items():
        if node['name'] == metabolite_id:
            node['node_is_primary'] = is_primary
            return node['bigg_id']
    return ""


def add_segment(segments, from_node_id, to_node_id, pos1, pos2, offset_factor):
    x_direction = 1 if pos1[0] < pos2[0] else -1
    y_direction = 1 if pos1[1] < pos2[1] else -1
    b1_x = pos1[0] + x_direction * abs(pos1[0] - pos2[0]) * offset_factor
    b1_y = pos1[1] + y_direction * abs(pos1[1] - pos2[1]) * offset_factor
    b2_x = pos1[0] + x_direction * 2 * abs(pos1[0] - pos2[0]) * offset_factor
    b2_y = pos1[1] + y_direction * 2 * abs(pos1[1] - pos2[1]) * offset_factor
    segments[str(uuid.uuid4())] = {
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "b1": {"x": b1_x, "y": b1_y},
        "b2": {"x": b2_x, "y": b2_y}
    }


def add_segment_without_pos(segments, from_node_id, to_node_id):
    segments[str(uuid.uuid4())] = {
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "b1": None,
        "b2": None
    }


def add_midmarker(nodes, id, position):
    nodes[id] = {
        "node_type": "midmarker",
        "x": position[0],
        "y": position[1]
    }
    return id

def define_edge_label_position(edge, position):
    edge["label_x"] = position[0]
    edge["label_y"] = position[1]
def create_edges(reactions, nodes):
    edges = {}
    for reaction in reactions:
        reaction_id = reaction['@id']
        metabolites = []
        edge = {
            'name': reaction['@name'] if '@name' in reaction else reaction_id,
            'bigg_id': reaction['@name'] if '@name' in reaction else reaction_id,
            "reversibility": False if '@reversible' in reaction and reaction['@reversible'] == 'false' else True,
            "metabolites": [],
            "label_x": 0,
            "label_y": 0,
        }

        # 添加 metabolites（反和产）
        base_reactant = reaction['annotation']['celldesigner:extension']['celldesigner:baseReactants'][
            'celldesigner:baseReactant']
        base_product = reaction['annotation']['celldesigner:extension']['celldesigner:baseProducts'][
            'celldesigner:baseProduct']
        metabolites.append({"bigg_id": get_metabolite_name(base_reactant["@species"], nodes, True), "coefficient": -1})
        metabolites.append({"bigg_id": get_metabolite_name(base_product["@species"], nodes, True), "coefficient": 1})

        # 中点信息，nodes 添加中点
        base_reactant_position = [nodes[base_reactant["@alias"]]['x'], nodes[base_reactant["@alias"]]['y']]
        base_product_position = [nodes[base_product["@alias"]]['x'], nodes[base_product["@alias"]]['y']]
        center_id = str(uuid.uuid4())
        center_position = [(nodes[base_reactant["@alias"]]['x'] + nodes[base_product["@alias"]]['x']) / 2,
                           (nodes[base_reactant["@alias"]]['y'] + nodes[base_product["@alias"]]['y']) / 2]

        offset_x = abs(base_product_position[0] - base_reactant_position[0]) * 0.1
        offset_y = abs(base_product_position[1] - base_reactant_position[1]) * 0.1

        define_edge_label_position(edge, center_position)
        add_midmarker(nodes, center_id, center_position)

        segments = {}
        reactants = reaction.get('annotation', {}).get('celldesigner:extension', {}).get(
            'celldesigner:listOfReactantLinks', {}).get('celldesigner:reactantLink', None)
        products = reaction.get('annotation', {}).get('celldesigner:extension', {}).get(
            'celldesigner:listOfProductLinks', {}).get('celldesigner:productLink', None)

        if reactants is None and products is None:
            add_segment(segments, base_reactant["@alias"], center_id, base_reactant_position, center_position, 1 / 3)
            add_segment(segments, center_id, base_product["@alias"], center_position, base_product_position, 1 / 3)

        if reactants is not None:
            left_id = str(uuid.uuid4())
            x_direction = 1 if base_reactant_position[0] > center_position[0] else -1
            y_direction = 1 if base_reactant_position[1] > center_position[1] else -1
            left_position = [
                center_position[0] + x_direction * offset_x,
                center_position[1] + y_direction * offset_y
            ]

            add_midmarker(nodes, left_id, left_position)
            add_segment_without_pos(segments, left_id, center_id)

            add_segment(segments, base_reactant["@alias"], left_id, base_reactant_position, left_position, 1 / 3)

            if isinstance(reactants, dict):  # 如果reactants是字典，将其转换为列表
                reactants = [reactants]

            for reactant in reactants:
                metabolites.append({
                    "bigg_id": get_metabolite_name(reactant['@reactant'], nodes, False),
                    "coefficient": -1
                })
                reaction_a_id = reactant['@alias']
                reaction_position = [nodes[reaction_a_id]['x'], nodes[reaction_a_id]['y']]
                add_segment(segments, reaction_a_id, left_id, reaction_position, left_position, 1 / 3)

        else:
            add_segment(segments, base_reactant["@alias"], center_id, base_reactant_position, center_position, 1 / 3)

        if products is not None:
            right_id = str(uuid.uuid4())
            x_direction = 1 if center_position[0] < base_product_position[0] else -1
            y_direction = 1 if center_position[1] < base_product_position[1] else -1
            right_position = [
                center_position[0] + x_direction * offset_x,
                center_position[1] + y_direction * offset_y
            ]

            add_midmarker(nodes, right_id, right_position)
            add_segment_without_pos(segments, center_id, right_id)
            add_segment(segments, right_id, base_product["@alias"], right_position, base_product_position, 1 / 3)

            if isinstance(products, dict):  # 如果products是字典，将其转换为列表
                products = [products]

            for product in products:
                metabolites.append({
                    "bigg_id": get_metabolite_name(product['@product'], nodes, False),
                    "coefficient": 1
                })

                reaction_a_id = product['@alias']
                reaction_position = [nodes[reaction_a_id]['x'], nodes[reaction_a_id]['y']]
                add_segment(segments, right_id, reaction_a_id, right_position, reaction_position, 1 / 3)

        else:
            add_segment(segments, center_id, base_product["@alias"], center_position, base_product_position, 1 / 3)

        edge["metabolites"] = metabolites
        edge["segments"] = segments
        edges.setdefault(reaction_id, edge)

    return edges


# Load your original JSON data
data = load_json_data('new_PPP.json')

map_name = data['sbml']['model']['@metaid']
map_id = data['sbml']['model']['@id']
map_description = ""
width = float(data['sbml']['model']['annotation']['celldesigner:extension']['celldesigner:modelDisplay']['@sizeX'])
height = float(data['sbml']['model']['annotation']['celldesigner:extension']['celldesigner:modelDisplay']['@sizeY'])

# Extract necessary components
species_aliases = data['sbml']['model']['annotation']['celldesigner:extension']['celldesigner:listOfSpeciesAliases'][
    'celldesigner:speciesAlias']
reactions = data['sbml']['model']['listOfReactions']['reaction']
species = data['sbml']['model']['listOfSpecies']['species']

# Extract positions
positions = extract_positions(species_aliases)

# Create nodes and edges
nodes = create_nodes(species_aliases, positions, species)
edges = create_edges(reactions, nodes)

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
            "x": -246,
            "y": -336.05,
            "width": width,
            "height": height
        }
    }
]

# Save the new JSON data
save_json_data(cytoscape_data, 'escher-v2.json')
