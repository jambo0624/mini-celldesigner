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

        # 主反应物和产物
        base_reactant_a_id = reaction['annotation']['celldesigner:extension']['celldesigner:baseReactants'][
            'celldesigner:baseReactant']["@alias"]
        base_reactant_s_id = reaction['annotation']['celldesigner:extension']['celldesigner:baseReactants'][
            'celldesigner:baseReactant']["@species"]
        base_reactant_name = ""
        for _, _sp in nodes.items():
            if _sp['name'] == base_reactant_s_id:
                base_reactant_name = _sp['bigg_id']
                _sp['node_is_primary'] = True
                break
        metabolites.append({
            "bigg_id": base_reactant_name,
            "coefficient": -1
        })

        base_product_a_id = reaction['annotation']['celldesigner:extension']['celldesigner:baseProducts'][
            'celldesigner:baseProduct']['@alias']
        base_product_s_id = reaction['annotation']['celldesigner:extension']['celldesigner:baseProducts'][
            'celldesigner:baseProduct']['@species']
        base_product_name = ""
        for _, _sp in nodes.items():
            if _sp['name'] == base_product_s_id:
                base_product_name = _sp['bigg_id']
                _sp['node_is_primary'] = True
                break
        metabolites.append({
            "bigg_id": base_product_name,
            "coefficient": 1
        })

        # 中点信息
        base_reactant_position = [nodes[base_reactant_a_id]['x'], nodes[base_reactant_a_id]['y']]
        base_product_position = [nodes[base_product_a_id]['x'], nodes[base_product_a_id]['y']]


        center_id = str(uuid.uuid4())
        center_position = [(base_reactant_position[0] + base_product_position[0]) / 2,
                           (base_reactant_position[1] + base_product_position[1]) / 2]


        edge["label_x"] = center_position[0]
        edge["label_y"] = center_position[1]

        nodes.setdefault(center_id, {
            "node_type": "midmarker",
            "x": center_position[0],
            "y": center_position[1]
        })

        vector_x = abs(base_product_position[0] - base_reactant_position[0])
        vector_y = abs(base_product_position[1] - base_reactant_position[1])
        offset_x = vector_x * 0.1
        offset_y = vector_y * 0.1

        segments = {}
        reactants = reaction.get('annotation', {}).get('celldesigner:extension', {}).get(
            'celldesigner:listOfReactantLinks', {}).get('celldesigner:reactantLink', None)
        products = reaction.get('annotation', {}).get('celldesigner:extension', {}).get(
            'celldesigner:listOfProductLinks', {}).get('celldesigner:productLink', None)

        if reactants is None and products is None:
            b1_x = base_reactant_position[0] + abs(base_reactant_position[0] - center_position[0]) / 3
            b1_y = base_reactant_position[1] + abs(base_reactant_position[1] - center_position[1]) / 3

            b2_x = base_reactant_position[0] + 2 * abs(
                base_reactant_position[0] - center_position[0]) / 3
            b2_y = base_reactant_position[1] + 2 * abs(
                base_reactant_position[1] - center_position[1]) / 3
            # 添加反应物到中点的连线
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": base_reactant_a_id,
                "to_node_id": center_id,
                "b1": {
                    "x": b1_x,
                    "y": b1_y
                },
                "b2": {
                    "x": b2_x,
                    "y": b2_y
                }
            })
            b3_x = base_product_position[0] + abs(base_product_position[0] - center_position[0]) / 3
            b3_y = base_product_position[1] + abs(base_product_position[1] - center_position[1]) / 3

            b4_x = base_product_position[0] + 2 * abs(
                base_product_position[0] - center_position[0]) / 3
            b4_y = base_product_position[1] + 2 * abs(
                base_product_position[1] - center_position[1]) / 3
            # 添加产物到中点的连线
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": center_id,
                "to_node_id": base_product_a_id,
                "b1": {
                    "x": b3_x,
                    "y": b3_y
                },
                "b2": {
                    "x": b4_x,
                    "y": b4_y
                }
            })




        if reactants is not None:
            left_id = str(uuid.uuid4())
            left_position = [
                center_position[0] - offset_x,
                center_position[1] - offset_y
            ]

            nodes.setdefault(
                left_id, {
                    "node_type": "midmarker",
                    "x": left_position[0],
                    "y": left_position[1],
                })
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": left_id,
                "to_node_id": center_id,
                "b1": None,
                "b2": None
            })

            b1_x = base_reactant_position[0] + abs(base_reactant_position[0] - left_position[0]) / 3
            b1_y = base_reactant_position[1] + abs(base_reactant_position[1] - left_position[1]) / 3
            b2_x = base_reactant_position[0] + 2 * abs(base_reactant_position[0] - left_position[0]) / 3
            b2_y = base_reactant_position[1] + 2 * abs(base_reactant_position[1] - left_position[1]) / 3
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": base_reactant_a_id,
                "to_node_id": left_id,
                "b1": {
                    "x": b1_x,
                    "y": b1_y
                },
                "b2": {
                    "x": b2_x,
                    "y": b2_y
                }
            })


            if isinstance(reactants, dict):  # 如果reactants是字典，将其转换为列表
                reactants = [reactants]

            for reactant in reactants:
                name = next(
                    (node['bigg_id'] for key, node in nodes.items() if node['name'] == reactant['@reactant']), "")
                metabolites.append({
                    "bigg_id": name,
                    "coefficient": -1
                })

                reaction_a_id = reactant['@alias']
                reaction_position = [nodes[reaction_a_id]['x'], nodes[reaction_a_id]['y']]
                x_greater = reaction_position[0] > left_position[0]
                y_greater = reaction_position[1] > left_position[1]
                b1_x = reaction_position[0] + abs(reaction_position[0] - left_position[0]) / 3 if x_greater else reaction_position[0] - abs(reaction_position[0] - left_position[0]) / 3
                b1_y = reaction_position[1] + abs(reaction_position[1] - left_position[1]) / 3 if y_greater else reaction_position[1] - abs(reaction_position[1] - left_position[1]) / 3

                b2_x = reaction_position[0] + 2 * abs(reaction_position[0] - left_position[0]) / 3 if x_greater else reaction_position[0] - 2 * abs(reaction_position[0] - left_position[0]) / 3
                b2_y = reaction_position[1] + 2 * abs(reaction_position[1] - left_position[1]) / 3 if y_greater else reaction_position[1] - 2 * abs(reaction_position[1] - left_position[1]) / 3

                segments.setdefault(str(uuid.uuid4()), {
                        "from_node_id": reaction_a_id,
                        "to_node_id": left_id,
                        "b1": {
                            "x": b1_x,
                            "y": b1_y
                        },
                        "b2": {
                            "x": b2_x,
                            "y": b2_y
                        }
                    })
        else:
            b1_x = base_reactant_position[0] + abs(base_reactant_position[0] - center_position[0]) / 3
            b1_y = base_reactant_position[1] + abs(base_reactant_position[1] - center_position[1]) / 3

            b2_x = base_reactant_position[0] + 2 * abs(
                base_reactant_position[0] - center_position[0]) / 3
            b2_y = base_reactant_position[1] + 2 * abs(
                base_reactant_position[1] - center_position[1]) / 3
            # 添加反应物到中点的连线
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": base_reactant_a_id,
                "to_node_id": center_id,
                "b1": {
                    "x": b1_x,
                    "y": b1_y
                },
                "b2": {
                    "x": b2_x,
                    "y": b2_y
                }
            })


        if products is not None:
            right_id = str(uuid.uuid4())
            right_position = [
                center_position[0] + offset_x,
                center_position[1] + offset_y
            ]

            nodes.setdefault(
                right_id, {
                    "node_type": "midmarker",
                    "x": right_position[0],
                    "y": right_position[1],
                }
            )
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": center_id,
                "to_node_id": right_id,
                "b1": None,
                "b2": None
            })

            b1_x = right_position[0] + abs(base_product_position[0] - right_position[0]) / 3
            b1_y = right_position[1] + abs(base_product_position[1] - right_position[1]) / 3
            b2_x = right_position[0] + 2 * abs(base_product_position[0] - right_position[0]) / 3
            b2_y = right_position[1] + 2 * abs(base_product_position[1] - right_position[1]) / 3
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": right_id,
                "to_node_id": base_product_a_id,
                "b1": {
                    "x": b1_x,
                    "y": b1_y
                },
                "b2": {
                    "x": b2_x,
                    "y": b2_y
                }
            })


            if isinstance(products, dict):  # 如果products是字典，将其转换为列表
                products = [products]

            for product in products:
                name = next((node['bigg_id'] for key, node in nodes.items() if node['name'] == product['@product']), "")
                metabolites.append({
                    "bigg_id": name,
                    "coefficient": 1
                })

                reaction_a_id = product['@alias']
                reaction_position = [nodes[reaction_a_id]['x'], nodes[reaction_a_id]['y']]

                x_greater = reaction_position[0] > right_position[0]
                y_greater = reaction_position[1] > right_position[1]

                b1_x = right_position[0] + abs(reaction_position[0] - right_position[0]) / 3 if x_greater else right_position[0] - abs(reaction_position[0] - right_position[0]) / 3
                b1_y = right_position[1] + abs(reaction_position[1] - right_position[1]) / 3 if y_greater else right_position[1] - abs(reaction_position[1] - right_position[1]) / 3

                b2_x = right_position[0] + 2 * abs(reaction_position[0] - right_position[0]) / 3 if x_greater else right_position[0] - 2 * abs(reaction_position[0] - right_position[0]) / 3
                b2_y = right_position[1] + 2 * abs(reaction_position[1] - right_position[1]) / 3 if y_greater else right_position[1] - 2 * abs(reaction_position[1] - right_position[1]) / 3

                segments.setdefault(str(uuid.uuid4()), {
                    "from_node_id": right_id,
                    "to_node_id": reaction_a_id,
                    "b1": {
                        "x": b1_x,
                        "y": b1_y
                    },
                    "b2": {
                        "x": b2_x,
                        "y": b2_y
                    }
                })
        else:
            b3_x = base_product_position[0] + abs(base_product_position[0] - center_position[0]) / 3
            b3_y = base_product_position[1] + abs(base_product_position[1] - center_position[1]) / 3

            b4_x = base_product_position[0] + 2 * abs(
                base_product_position[0] - center_position[0]) / 3
            b4_y = base_product_position[1] + 2 * abs(
                base_product_position[1] - center_position[1]) / 3
            # 添加产物到中点的连线
            segments.setdefault(str(uuid.uuid4()), {
                "from_node_id": center_id,
                "to_node_id": base_product_a_id,
                "b1": {
                    "x": b3_x,
                    "y": b3_y
                },
                "b2": {
                    "x": b4_x,
                    "y": b4_y
                }
            })

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
            # "x": width / 50,
            # "y": height / 50,
            # "width": width,
            # "height": height
            "x": -246,
            "y": -336.05,
            "width": 6622,
            "height": 3213.1
        }
    }
]

# Save the new JSON data
save_json_data(cytoscape_data, 'escher-v1.json')
