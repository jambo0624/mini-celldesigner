import json

input_file_path = 'SBML_new_PPP_6.json'
output_file_path = 'sbml2escher_SBML_new_PPP_6.json'

# Load SBML JSON data
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save escher JSON data
def save_json_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Get metabolites for a reaction
def get_metabolite_for_reaction(reaction, specie2bigg):
    """
    :param reaction: reaction object
    :param specie2bigg: dict of species id to bigg_id
    :return: metabolites of the reaction, {'bigg_id': str, 'coefficient': int}[]
    """
    reaction_metabolites = []
    # get the list of reactants
    list_of_reactants = reaction.get('listOfReactants', {}).get('speciesReference')
    if isinstance(list_of_reactants, dict):
        list_of_reactants = [list_of_reactants]
    for reactant in list_of_reactants:
        metabolite_id = reactant['@species']
        metabolite_name = specie2bigg[metabolite_id]
        reaction_metabolites.append({
            'bigg_id': metabolite_name,
            'coefficient': -1
        })
    
    # get the list of products
    list_of_products = reaction.get('listOfProducts', {}).get('speciesReference')
    if isinstance(list_of_products, dict):
        list_of_products = [list_of_products]
    for product in list_of_products:
        metabolite_id = product['@species']
        metabolite_name = specie2bigg[metabolite_id]
        reaction_metabolites.append({
            'bigg_id': metabolite_name,
            'coefficient': 1
        })

    return reaction_metabolites

# Create the midmarker for the label of reaction, return the midmarker id
def mid_node(start, end, reaction_layout_id, reaction, nodes):
    """
    :param start: start node 
    :param end: end node
    :param reaction_layout_id: reaction layout id 
    :param reaction: reaction object
    :param nodes: nodes dict
    :return: midmarker id
    """
    mid_id = f"{reaction_layout_id}-mid"
    # make the midmarker
    mid_node = {
        'x': (float(start['@layout:x']) + float(end['@layout:x'])) / 2,
        'y': (float(start['@layout:y']) + float(end['@layout:y'])) / 2
    }
    # add the midmarker
    nodes[mid_id] = {
        'node_type': 'midmarker',
        'x': mid_node['x'],
        'y': mid_node['y'],
    }

    reaction['label_x'] = mid_node['x']
    reaction['label_y'] = mid_node['y']
    return mid_id


# check if a point is on a segment
def is_point_on_segment(px, py, x1, y1, x2, y2):
    """
    :param px: point x 
    :param py: point y
    :param x1: start node x
    :param y1: start node y
    :param x2: end node x
    :param y2: end node y
    :return: bool of whether the point is on the segment
    """
    
    # calculate the cross product to determine if the point is on the segment
    cross_product = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    # because of the floating point error, we use 1e-6 as the threshold
    if abs(cross_product) > 1e-6:
        return False

    # check if the point is within the x range, the range is extended by 1 to avoid the floating point error
    if px < min(x1, x2) - 1 or px > max(x1, x2) + 1:
        return False

    # check if the point is within the y range, the range is extended by 1 to avoid the floating point error
    if py < min(y1, y2) - 1 or py > max(y1, y2) + 1:
        return False

    return True


# delete the target segment and insert new node and segments
def update_segments_with_node(is_produce_node, segments, nodes, start_x, start_y, extra_node_id, node_in_reaction_curve,
                              seg_id_for_debug=None):
    """
    :param segments: all segments in the single reaction
    :param nodes: all nodes in the model
    :param start_x: current x position
    :param start_y: current y position
    :param extra_node_id: current node id, which is not the same as the start/end node id
    :param node_in_reaction_curve: start/end node id, for the not found situation
    :param seg_id_for_debug: current segment id, for the debug
    :return: None
    """
    segment_to_remove = None
    from_node_id = None
    to_node_id = None

    # find the segment containing start_x and start_y
    for seg_id, segment in segments.items():
        from_node = nodes[segment['from_node_id']]
        to_node = nodes[segment['to_node_id']]
        if is_point_on_segment(start_x, start_y, from_node['x'], from_node['y'], to_node['x'], to_node['y']):
            segment_to_remove = seg_id
            from_node_id = segment['from_node_id']
            to_node_id = segment['to_node_id']
            break

    # if no segment is found, create a new segment from the target(start/end) node to the current node
    if segment_to_remove is None:
        print("No segment found containing the point.", seg_id_for_debug)
        segments[extra_node_id] = {
            # the flux direction is from the reaction to the product node
            'from_node_id': node_in_reaction_curve,
            'to_node_id': extra_node_id,
            'b1': None,
            'b2': None,
        } if is_produce_node else {
            # reverse when the node is a substrate, cause the flux direction is from the substrate node to the reaction
            'from_node_id': extra_node_id,
            'to_node_id': node_in_reaction_curve,
            'b1': None,
            'b2': None,
        }
        return

    # delete the target segment
    del segments[segment_to_remove]

    # create two new segments
    new_segment_1_id = f"{extra_node_id}-left"
    new_segment_2_id = f"{extra_node_id}-right"
    segments[new_segment_1_id] = {
        'from_node_id': from_node_id,
        'to_node_id': extra_node_id,
        'b1': None,
        'b2': None,
    }

    segments[new_segment_2_id] = {
        'from_node_id': extra_node_id,
        'to_node_id': to_node_id,
        'b1': None,
        'b2': None,
    }


# Load your original JSON data
data = load_json_data(input_file_path)

# map basic information
model = data['sbml']['model']
map_name = model['@id']
map_id = model['@id']
map_description = ""

# define nodes and edges
nodes = {}
edges = {}

# create species2bigg, for the convenience of getting bigg_id
species = model['listOfSpecies']['species']
specie2bigg = {}
for sp in species:
    specie2bigg[sp['@id']] = sp['@name']

# define the list of layouts
list_of_layouts = model['layout:listOfLayouts']
# dict or list is better?
if isinstance(list_of_layouts, dict):
    list_of_layouts = [list_of_layouts]

layout_root = list_of_layouts[0]['layout:layout']
layout_width = float(layout_root['layout:dimensions']['@layout:width'])
layout_height = float(layout_root['layout:dimensions']['@layout:height'])

# create reactions, expect the label position and segments
reactions = model['listOfReactions']['reaction']
for reaction in reactions:
    reaction_id = reaction['@id']
    reaction_name = reaction['@name'] if '@name' in reaction else reaction_id
    reaction_reversible = reaction['@reversible'] == 'true'
    reaction_metabolites = get_metabolite_for_reaction(reaction, specie2bigg)
    edges[reaction_id] = {}
    edges[reaction_id]['name'] = reaction_name
    edges[reaction_id]['bigg_id'] = reaction_name
    edges[reaction_id]['reversibility'] = reaction_reversible
    edges[reaction_id]['metabolites'] = reaction_metabolites
    # set the default label position, outside the layout
    edges[reaction_id]['label_x'] = layout_width + 100
    edges[reaction_id]['label_y'] = layout_height + 100

# create nodes, expect the midmarker
list_of_species_glyphs = layout_root['layout:listOfSpeciesGlyphs']['layout:speciesGlyph']
for species_glyph in list_of_species_glyphs:
    layout_id = species_glyph['@layout:id']
    species_id = species_glyph['@layout:species']
    position = species_glyph['layout:boundingBox']['layout:position']
    width = species_glyph['layout:boundingBox']['layout:dimensions']['@layout:width']
    height = species_glyph['layout:boundingBox']['layout:dimensions']['@layout:height']
    name = specie2bigg[species_id]
    nodes[layout_id] = {
        'bigg_id': name,
        'name': name,
        'node_type': 'metabolite',
        'x': float(position['@layout:x']) + float(width) / 2,
        'y': float(position['@layout:y']) + float(height) / 2,
        'label_x': float(position['@layout:x']) + float(width) / 2,
        'label_y': float(position['@layout:y']) + float(height) / 2,
        'node_is_primary': False
    }

# create the segments of edges
list_of_reaction_glyphs = layout_root['layout:listOfReactionGlyphs']['layout:reactionGlyph']
for reaction_glyph in list_of_reaction_glyphs:
    reaction = edges[reaction_glyph['@layout:reaction']]
    segments = {}
    reaction_seg_start_node_id = None
    reaction_seg_end_node_id = None
    reaction_layout_id = reaction_glyph['@layout:id']

    # add the segments of reaction
    list_of_reaction_segments = []
    if 'layout:curve' in reaction_glyph:
        layout_curve = reaction_glyph['layout:curve']
        if layout_curve is not None and 'layout:listOfCurveSegments' in layout_curve:
            list_of_reaction_curves = layout_curve['layout:listOfCurveSegments']
            if list_of_reaction_curves is not None and 'layout:curveSegment' in list_of_reaction_curves:
                list_of_reaction_segments = list_of_reaction_curves['layout:curveSegment']

    if isinstance(list_of_reaction_segments, dict):
        list_of_reaction_segments = [list_of_reaction_segments]
    # retrieve the line segments of reaction to create the segments of edges
    for index, reaction_segment in enumerate(list_of_reaction_segments):
        reaction_segment_id = f"{reaction_layout_id}-{index}"
        start = reaction_segment['layout:start']
        end = reaction_segment['layout:end']
        start_x = float(start['@layout:x'])
        start_y = float(start['@layout:y'])
        end_x = float(end['@layout:x'])
        end_y = float(end['@layout:y'])

        start_id = f"{reaction_segment_id}-start"
        end_id = f"{reaction_segment_id}-end"
        nodes[start_id] = {
            'node_type': 'multimarker',
            'x': start_x,
            'y': start_y,
        }
        nodes[end_id] = {
            'node_type': 'multimarker',
            'x': end_x,
            'y': end_y,
        }

        if index == 0:
            # sign the start node, for the connection of the metabolites
            reaction_seg_start_node_id = start_id
            # sign the end node, for the connection of the metabolites
            reaction_seg_end_node_id = end_id

            # create midmarker for the label of reaction
            mid_id = mid_node(start, end, reaction_layout_id, reaction, nodes)
            mid_left_seg_id = f"{reaction_segment_id}-mid-left"
            segments[mid_left_seg_id] = {
                'from_node_id': start_id,
                'to_node_id': mid_id,
                'b1': None,
                'b2': None,
            }
            mid_right_seg_id = f"{reaction_segment_id}-mid-right"
            segments[mid_right_seg_id] = {
                'from_node_id': mid_id,
                'to_node_id': end_id,
                'b1': None,
                'b2': None,
            }
        else:
            if index == len(list_of_reaction_segments) - 1:
                # sign the end node, for the connection of the metabolites
                reaction_seg_end_node_id = end_id
            segments[reaction_segment_id] = {
                'from_node_id': start_id,
                'to_node_id': end_id,
                'b1': None,
                'b2': None,
            }

    # create the segments of metabolites
    list_of_metabolite_curves = reaction_glyph['layout:listOfSpeciesReferenceGlyphs']['layout:speciesReferenceGlyph']
    for metabolite_curve in list_of_metabolite_curves:
        metabolite_curve_id =  f"{reaction_layout_id}-{metabolite_curve['@layout:id']}"
        role = metabolite_curve['@layout:role']
        mato_species_glyph = metabolite_curve['@layout:speciesGlyph']
        start_node_id = reaction_seg_start_node_id
        end_node_id = reaction_seg_end_node_id

        # get the list of curve segments in each metabolite
        list_of_metabolite_segments =  metabolite_curve['layout:curve']['layout:listOfCurveSegments']["layout:curveSegment"]
        if isinstance(list_of_metabolite_segments, dict):
            list_of_metabolite_segments = [list_of_metabolite_segments]

        length_of_metabolite_segments = len(list_of_metabolite_segments)
        for index, metabolite_segment in enumerate(list_of_metabolite_segments):
            start_x = float(metabolite_segment['layout:start']['@layout:x'])
            start_y = float(metabolite_segment['layout:start']['@layout:y'])
            end_x = float(metabolite_segment['layout:end']['@layout:x'])
            end_y = float(metabolite_segment['layout:end']['@layout:y'])
            start_seg_id_extra = None
            end_seg_id_extra = None
            metabolite_segment_id = f"{metabolite_curve_id}-{mato_species_glyph}"
            # sign the start adn the end node, for the connection of the metabolites
            current_metabolite_segment_id = f"{metabolite_segment_id}-{index}"
            next_metabolite_segment_id = f"{metabolite_segment_id}-{index + 1}"

            # mark the primary metabolites
            if role == 'substrate' or role == 'product':
                nodes[mato_species_glyph]['node_is_primary'] = True

            if role == 'substrate' or role == 'sidesubstrate':
                if index == 0:
                    # if the start node is not the same as the start node of the reaction, create a new node
                    if start_node_id and (start_x != nodes[start_node_id]['x'] or start_y != nodes[start_node_id]['y']):
                        # create a new node
                        start_seg_id_extra = f"{current_metabolite_segment_id}-extra"
                        # add the new node
                        nodes[start_seg_id_extra] = {
                            'node_type': 'multimarker',
                            'x': start_x,
                            'y': start_y,
                        }

                        # update the segments with the new node
                        update_segments_with_node(False, segments, nodes, start_x, start_y, start_seg_id_extra,
                                                  start_node_id, current_metabolite_segment_id)

                        # add the current segment from the next segment start node to the extra node, if this is the last segment then line from the mato_species_glyph to the extra node
                        segments[current_metabolite_segment_id] = {
                            'from_node_id': mato_species_glyph if length_of_metabolite_segments == 1 else next_metabolite_segment_id,
                            'to_node_id': start_seg_id_extra,
                            'b1': None,
                            'b2': None,
                        }
                    else:
                        # add the segment of the metabolite from the start node of the reaction to the metabolite
                        segments[current_metabolite_segment_id] = {
                            'from_node_id': mato_species_glyph if length_of_metabolite_segments == 1 else next_metabolite_segment_id,
                            'to_node_id': start_node_id,
                            'b1': None,
                            'b2': None,
                        }

                elif index == length_of_metabolite_segments - 1:
                    nodes[current_metabolite_segment_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    segments[current_metabolite_segment_id] = {
                        'from_node_id': mato_species_glyph,
                        'to_node_id': current_metabolite_segment_id,
                        'b1': None,
                        'b2': None,
                    }
                else:
                    nodes[current_metabolite_segment_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    segments[current_metabolite_segment_id] = {
                        'from_node_id': next_metabolite_segment_id,
                        'to_node_id': current_metabolite_segment_id,
                        'b1': None,
                        'b2': None,
                    }

            elif role == 'product' or role == 'sideproduct':
                if index == 0:
                    if end_node_id and (start_x != nodes[end_node_id]['x'] or start_y != nodes[end_node_id]['y']):
                        end_seg_id_extra = f"{current_metabolite_segment_id}-extra"
                        nodes[end_seg_id_extra] = {
                            'node_type': 'multimarker',
                            'x': start_x,
                            'y': start_y,
                        }

                        update_segments_with_node(True, segments, nodes, start_x, start_y, end_seg_id_extra,
                                                  end_node_id, current_metabolite_segment_id)

                        segments[current_metabolite_segment_id] = {
                            'from_node_id': end_seg_id_extra,
                            'to_node_id': mato_species_glyph if length_of_metabolite_segments == 1 else next_metabolite_segment_id,
                            'b1': None,
                            'b2': None,
                        }
                    else:
                        segments[current_metabolite_segment_id] = {
                            'from_node_id': end_node_id,
                            'to_node_id': mato_species_glyph if length_of_metabolite_segments == 1 else next_metabolite_segment_id,
                            'b1': None,
                            'b2': None,
                        }

                elif index == length_of_metabolite_segments - 1:
                    nodes[current_metabolite_segment_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    segments[current_metabolite_segment_id] = {
                        'from_node_id': current_metabolite_segment_id,
                        'to_node_id': mato_species_glyph,
                        'b1': None,
                        'b2': None,
                    }
                else:
                    nodes[current_metabolite_segment_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    segments[current_metabolite_segment_id] = {
                        'from_node_id': current_metabolite_segment_id,
                        'to_node_id': next_metabolite_segment_id,
                        'b1': None,
                        'b2': None,
                    }

            else:
                continue

    reaction['segments'] = segments
    edges[reaction_glyph['@layout:reaction']] = reaction

escher_maps = [{
    "map_name": map_name,
    "map_id": map_id,
    "map_description": map_description,
    "homepage": "https://escher.github.io",
    "schema": "https://escher.github.io/escher/jsonschema/1-0-0#"
},
    {
        "reactions": edges,
        "nodes": nodes,
        "text_labels": {},
        "canvas": {
            "x": -layout_width / 20,
            "y": -layout_height / 20,
            "width": layout_width * 1.1,
            "height": layout_height * 1.1
        }
    }
]

# Save the new JSON data
save_json_data(escher_maps, output_file_path)

print(f"convert success, and save to {output_file_path}")
