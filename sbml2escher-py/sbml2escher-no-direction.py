import json

input_file_path = 'SBML_origin.json'
output_file_path = 'sbml2escher_SBML_origin.json'

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_metabolite_for_reaction(reaction, specie2bigg):
    reaction_metabolites = []
    listOfReactants = reaction.get('listOfReactants', {}).get('speciesReference')
    if isinstance(listOfReactants, dict):
        listOfReactants = [listOfReactants]
    for reactant in listOfReactants:
        metabolite_id = reactant['@species']
        metabolite_name = specie2bigg[metabolite_id]
        reaction_metabolites.append({
            'bigg_id': metabolite_name,
            'coefficient': -1
        })
    listOfProducts = reaction.get('listOfProducts', {}).get('speciesReference')
    if isinstance(listOfProducts, dict):
        listOfProducts = [listOfProducts]
    for product in listOfProducts:
        metabolite_id = product['@species']
        metabolite_name = specie2bigg[metabolite_id]
        reaction_metabolites.append({
            'bigg_id': metabolite_name,
            'coefficient': 1
        })

    return reaction_metabolites

def mid_node(start, end, reaction_layout_id, reaction, nodes):
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
    # calculate the cross product to determine if the point is on the segment
    cross_product = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    if abs(cross_product) > 1e-6:
        return False

    # check if the point is within the x range
    if px < min(x1, x2) or px > max(x1, x2):
        return False

    # check if the point is within the y range
    if py < min(y1, y2) or py > max(y1, y2):
        return False

    return True

# delete the target segment and insert new node and segments
def update_segments_with_node(segments, nodes, start_x, start_y, new_node_id, for_not_found_node_id, tt=None):
    segment_to_remove = None
    from_node_id = None
    to_node_id = None

    # find the segment containing start_x and start_y
    for seg_id, segment in segments.items():
        from_node = nodes[segment['from_node_id']]
        to_node = nodes[segment['to_node_id']]
        # if tt == 're6450_5380--node_5387-sa18879-0':
        #     print(seg_id, segment['from_node_id'], from_node['x'], from_node['y'], segment['to_node_id'], to_node['x'], to_node['y'])
        if is_point_on_segment(start_x, start_y, from_node['x'], from_node['y'], to_node['x'], to_node['y']):
            segment_to_remove = seg_id
            from_node_id = segment['from_node_id']
            to_node_id = segment['to_node_id']
            break

    if segment_to_remove is None:
        # print("No segment found containing the point.", tt)
        segments[new_node_id] = {
            'from_node_id': for_not_found_node_id,
            'to_node_id': new_node_id,
            'b1': None,
            'b2': None,
        }
        return


    # delete the target segment
    del segments[segment_to_remove]

    # create two new segments
    new_segment_1_id = f"{new_node_id}-left"
    new_segment_2_id = f"{new_node_id}-right"
    segments[new_segment_1_id] = {
        'from_node_id': from_node_id,
        'to_node_id': new_node_id,
        'b1': None,
        'b2': None,
    }

    segments[new_segment_2_id] = {
        'from_node_id': new_node_id,
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


# define the list of layouts
listOfLayouts = model['layout:listOfLayouts']
# dict or list is better?
if isinstance(listOfLayouts, dict):
    listOfLayouts = [listOfLayouts]

layoutRoot = listOfLayouts[0]['layout:layout']
layout_width = float(layoutRoot['layout:dimensions']['@layout:width'])
layout_height = float(layoutRoot['layout:dimensions']['@layout:height'])

# create nodes, expect the midmarker
listOfSpeciesGlyphs = layoutRoot['layout:listOfSpeciesGlyphs']['layout:speciesGlyph']
for speciesGlyph in listOfSpeciesGlyphs:
    layoutId = speciesGlyph['@layout:id']
    speciesId = speciesGlyph['@layout:species']
    position = speciesGlyph['layout:boundingBox']['layout:position']
    width = speciesGlyph['layout:boundingBox']['layout:dimensions']['@layout:width']
    height = speciesGlyph['layout:boundingBox']['layout:dimensions']['@layout:height']
    name = specie2bigg[speciesId]
    nodes[layoutId] = {
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
listOfReactionGlyphs = layoutRoot['layout:listOfReactionGlyphs']['layout:reactionGlyph']
for reactionGlyph in listOfReactionGlyphs:
    reaction = edges[reactionGlyph['@layout:reaction']]
    segments = {}
    reaction_seg_start_node_id = None
    reaction_seg_end_node_id = None
    reaction_layout_id = reactionGlyph['@layout:id']

    # add the segments of reaction
    listOfReactionSegments = reactionGlyph['layout:curve']['layout:listOfCurveSegments']['layout:curveSegment']
    if isinstance(listOfReactionSegments, dict):
        listOfReactionSegments = [listOfReactionSegments]
    # retrieve the line segments of reaction to create the segments of edges
    for index, curveSegmentItem in enumerate(listOfReactionSegments):
        curveSegment = curveSegmentItem
        segmentId = f"{reaction_layout_id}-{index}"
        start = curveSegment['layout:start']
        end = curveSegment['layout:end']
        start_x = float(start['@layout:x'])
        start_y = float(start['@layout:y'])
        end_x = float(end['@layout:x'])
        end_y = float(end['@layout:y'])

        start_id = f"{segmentId}-start"
        end_id = f"{segmentId}-end"
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
        # sign the start node, for the connection of the metabolites
        reaction_seg_start_node_id = start_id
        # sign the end node, for the connection of the metabolites
        reaction_seg_end_node_id = end_id
        if index == 0:
            # create midmarker for the label of reaction
            mid_id = mid_node(start, end, reaction_layout_id, reaction, nodes)
            mid_left_seg_id = f"{segmentId}-mid-left"
            segments[mid_left_seg_id] = {
                'from_node_id': start_id,
                'to_node_id': mid_id,
                'b1': None,
                'b2': None,
            }
            mid_right_seg_id = f"{segmentId}-mid-right"
            segments[mid_right_seg_id] = {
                'from_node_id': mid_id,
                'to_node_id': end_id,
                'b1': None,
                'b2': None,
            }
        else:
            segments[segmentId] = {
                'from_node_id': start_id,
                'to_node_id': end_id,
                'b1': None,
                'b2': None,
            }

    # create the segments of metabolites
    listOfCurveSegments = reactionGlyph['layout:listOfSpeciesReferenceGlyphs']['layout:speciesReferenceGlyph']
    for curveSegment in listOfCurveSegments:
        segmentId = curveSegment['@layout:id']
        role = curveSegment['@layout:role']
        mato_speciesGlyph = curveSegment['@layout:speciesGlyph']
        start_node_id = reaction_seg_start_node_id
        end_node_id = reaction_seg_end_node_id

        # get the list of curve segments in each metabolite
        _listOfCurveSegments = curveSegment['layout:curve']['layout:listOfCurveSegments']["layout:curveSegment"]
        if isinstance(_listOfCurveSegments, dict):
            _listOfCurveSegments = [_listOfCurveSegments]

        lenOfCurveSegments = len(_listOfCurveSegments)
        for index, _curveSegment in enumerate(_listOfCurveSegments):
            start_x = float(_curveSegment['layout:start']['@layout:x'])
            start_y = float(_curveSegment['layout:start']['@layout:y'])
            end_x = float(_curveSegment['layout:end']['@layout:x'])
            end_y = float(_curveSegment['layout:end']['@layout:y'])
            start_seg_id_extra = None
            end_seg_id_extra = None
            seg_id = f"{segmentId}-{mato_speciesGlyph}-{index}"

            # mark the primary metabolites
            if role == 'substrate' or role == 'product':
                nodes[mato_speciesGlyph]['node_is_primary'] = True

            if role == 'substrate' or role == 'sidesubstrate':
                if index == 0:
                    if lenOfCurveSegments != 1:
                        nodes[seg_id] = {
                            'node_type': 'multimarker',
                            'x': end_x,
                            'y': end_y,
                        }
                    if start_x != nodes[start_node_id]['x'] or start_y != nodes[start_node_id]['y']:
                        start_seg_id_extra = f"{segmentId}-{mato_speciesGlyph}-{index}-extra"
                        nodes[start_seg_id_extra] = {
                            'node_type': 'multimarker',
                            'x': start_x,
                            'y': start_y,
                        }

                        tt = f"{reaction_layout_id}--{seg_id}"
                        update_segments_with_node(segments, nodes, start_x, start_y, start_seg_id_extra, start_node_id, tt)

                        segments[seg_id] = {
                            'from_node_id': start_seg_id_extra,
                            'to_node_id': mato_speciesGlyph if lenOfCurveSegments == 1 else seg_id,
                            'b1': None,
                            'b2': None,
                        }
                    else:
                        segments[seg_id] = {
                            'from_node_id': start_node_id,
                            'to_node_id': mato_speciesGlyph if lenOfCurveSegments == 1 else seg_id,
                            'b1': None,
                            'b2': None,
                        }
                elif index == lenOfCurveSegments - 1:
                    nodes[seg_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    segments[seg_id] = {
                        'from_node_id': seg_id,
                        'to_node_id': mato_speciesGlyph,
                        'b1': None,
                        'b2': None,
                    }
                else:
                    start_seg_id = f"{seg_id}-start"
                    nodes[start_seg_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    end_seg_id = f"{seg_id}-end"
                    nodes[end_seg_id] = {
                        'node_type': 'multimarker',
                        'x': end_x,
                        'y': end_y,
                    }
                    segments[seg_id] = {
                        'from_node_id': start_seg_id,
                        'to_node_id': end_seg_id,
                        'b1': None,
                        'b2': None,
                    }

            elif role == 'product' or role == 'sideproduct':
                if index == 0:
                    if lenOfCurveSegments != 1:
                        nodes[seg_id] = {
                            'node_type': 'multimarker',
                            'x': end_x,
                            'y': end_y,
                        }
                    if start_x != nodes[end_node_id]['x'] or start_y != nodes[end_node_id]['y']:
                        end_seg_id_extra = f"{segmentId}-{mato_speciesGlyph}-{index}-extra"
                        nodes[end_seg_id_extra] = {
                            'node_type': 'multimarker',
                            'x': start_x,
                            'y': start_y,
                        }

                        tt = f"{reaction_layout_id}--{seg_id}"
                        update_segments_with_node(segments, nodes, start_x, start_y, end_seg_id_extra, end_node_id, tt)

                        segments[seg_id] = {
                            'from_node_id': end_seg_id_extra,
                            'to_node_id': mato_speciesGlyph if lenOfCurveSegments == 1 else seg_id,
                            'b1': None,
                            'b2': None,
                        }
                    else:
                        segments[seg_id] = {
                            'from_node_id': end_node_id,
                            'to_node_id': mato_speciesGlyph if lenOfCurveSegments == 1 else seg_id,
                            'b1': None,
                            'b2': None,
                        }
                elif index == lenOfCurveSegments - 1:
                    nodes[seg_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    segments[seg_id] = {
                        'from_node_id': seg_id,
                        'to_node_id': mato_speciesGlyph,
                        'b1': None,
                        'b2': None,
                    }
                else:
                    start_seg_id = f"{seg_id}-start"
                    nodes[start_seg_id] = {
                        'node_type': 'multimarker',
                        'x': start_x,
                        'y': start_y,
                    }

                    end_seg_id = f"{seg_id}-end"
                    nodes[end_seg_id] = {
                        'node_type': 'multimarker',
                        'x': end_x,
                        'y': end_y,
                    }
                    segments[seg_id] = {
                        'from_node_id': start_seg_id,
                        'to_node_id': end_seg_id,
                        'b1': None,
                        'b2': None,
                    }

            else:
                continue

    reaction['segments'] = segments
    edges[reactionGlyph['@layout:reaction']] = reaction

cytoscape_data = [{
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
            "x": 0,
            "y": 0,
            "width": layout_width,
            "height": layout_height
        }
    }
]

# Save the new JSON data
save_json_data(cytoscape_data, output_file_path)

print(f"转换成功，结果已保存到 {output_file_path}")