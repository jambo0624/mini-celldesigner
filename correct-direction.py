import json

# Function to correct segments based on the specified logic
def correct_segments(reactions):
    for reaction in reactions.values():
        start_node_id = None
        for index, (segment_id, segment) in enumerate(reaction['segments'].items()):
            if index == 0:
                # First segment, save the from_node_id as start_node_id
                start_node_id = segment['from_node_id']
            elif index == 1:
                # Second segment, set to_node_id as the new start_node_id and swap
                segment['from_node_id'], segment['to_node_id'] = segment['to_node_id'], segment['from_node_id']
            else:
                # For subsequent segments, swap if from_node_id matches start_node_id
                if segment['from_node_id'] == start_node_id:
                    segment['from_node_id'], segment['to_node_id'] = segment['to_node_id'], segment['from_node_id']

# Load the JSON file
file_path = 'pathwayMap_sphingolipidMetabolism_rc_v2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Correct all reactions in the dataset
for entry in data:
    if 'reactions' in entry:
        correct_segments(entry['reactions'])

# Save the corrected data
corrected_file_path = 'pathwayMap_sphingolipidMetabolism_rc_v2_corrected.json'
with open(corrected_file_path, 'w') as corrected_file:
    json.dump(data, corrected_file, indent=2)

print(f"Corrected file saved to {corrected_file_path}")