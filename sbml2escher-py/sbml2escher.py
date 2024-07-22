import json

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


# Load your original JSON data
data = load_json_data('SBML_new_PPP_6.json')

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
    reaction_seg_start_node = None
    reaction_seg_end_node = None
    listOfReactionSegments = reactionGlyph['layout:curve']['layout:listOfCurveSegments']['layout:curveSegment']
    reaction_layout_id = reactionGlyph['@layout:id']
    if isinstance(listOfReactionSegments, dict):
        listOfReactionSegments = [listOfReactionSegments]
    # add the segments of reaction
    for index, curveSegmentItem in enumerate(listOfReactionSegments):
        if len(listOfReactionSegments) == 1:
            curveSegment = curveSegmentItem
            segmentId = f"{reaction_layout_id}-{index}"
            start = curveSegment['layout:start']
            end = curveSegment['layout:end']

            mid_id = mid_node(start, end, reaction_layout_id, reaction, nodes)
            reaction_seg_start_node = mid_id
            reaction_seg_end_node = mid_id
        else:
            curveSegment = curveSegmentItem
            segmentId = f"{reaction_layout_id}-{index}"

            start = curveSegment['layout:start']
            end = curveSegment['layout:end']
            start_id = f"{reaction_layout_id}-{index}-start"
            end_id = f"{reaction_layout_id}-{index}-end"
            nodes[start_id] = {
                'node_type': 'multimarker',
                'x': float(start['@layout:x']),
                'y': float(start['@layout:y']),
            }
            nodes[end_id] = {
                'node_type': 'multimarker',
                'x': float(end['@layout:x']),
                'y': float(end['@layout:y']),
            }
            segments[segmentId] = {
                'from_node_id': start_id,
                'to_node_id': end_id,
                'b1': None,
                'b2': None,
            }

            if index == 0:
                mid_node(start, end, reaction_layout_id, reaction, nodes)
                # sign the start node, for the connection of the metabolites
                reaction_seg_start_node = start_id

            if index == len(listOfReactionSegments) - 1:
                # sign the end node, for the connection of the metabolites
                reaction_seg_end_node = end_id

    listOfCurveSegments = reactionGlyph['layout:listOfSpeciesReferenceGlyphs']['layout:speciesReferenceGlyph']

    for curveSegment in listOfCurveSegments:
        segmentId = curveSegment['@layout:id']
        role = curveSegment['@layout:role']
        mato_speciesGlyph = curveSegment['@layout:speciesGlyph']
        start_node = reaction_seg_start_node
        end_node = reaction_seg_end_node

        _listOfCurveSegments = curveSegment['layout:curve']['layout:listOfCurveSegments']["layout:curveSegment"]
        if isinstance(_listOfCurveSegments, dict):
            _listOfCurveSegments = [_listOfCurveSegments]

        lenOfCurveSegments = len(_listOfCurveSegments)
        for index, _curveSegment in enumerate(_listOfCurveSegments):
            start_x = float(_curveSegment['layout:start']['@layout:x'])
            start_y = float(_curveSegment['layout:start']['@layout:y'])
            end_x = float(_curveSegment['layout:end']['@layout:x'])
            end_y = float(_curveSegment['layout:end']['@layout:y'])

            if role == 'substrate' or role == 'sidesubstrate':
                # mark the primary metabolites
                if role == 'substrate':
                    nodes[mato_speciesGlyph]['is_primary'] = True

                seg_id =  f"{segmentId}-{mato_speciesGlyph}-{index}"
                if index == 0 and lenOfCurveSegments == 1:
                    segments[seg_id] = {
                        'from_node_id': mato_speciesGlyph,
                        'to_node_id': start_node,
                        'b1': None,
                        'b2': None,
                    }
                elif index == 0:
                    nodes[seg_id] = {
                        'node_type': 'multimarker',
                        'x': end_x,
                        'y': end_y,
                    }

                    segments[seg_id] = {
                        'from_node_id': seg_id,
                        'to_node_id': start_node,
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
                # mark the primary metabolites
                if role == 'product':
                    nodes[mato_speciesGlyph]['is_primary'] = True

                seg_id =  f"{segmentId}{mato_speciesGlyph}{index}"
                if index == lenOfCurveSegments - 1 and lenOfCurveSegments == 1:
                    segments[seg_id] = {
                        'from_node_id': end_node,
                        'to_node_id': mato_speciesGlyph,
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
                        'to_node_id': start_node,
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
                        'from_node_id': end_seg_id,
                        'to_node_id': start_seg_id,
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
save_json_data(cytoscape_data, 'sbml2escher.json')
