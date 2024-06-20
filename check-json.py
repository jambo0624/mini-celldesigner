import json

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)



origin = load_json_data('Recon1 Glycolysis TCA PPP.json')
escher = load_json_data('escher-v1.json')

if len(origin[1]['nodes']) == len(escher[1]['nodes']):
    print(len(origin[1]['nodes']), len(escher[1]['nodes']))
    print("nodes is the same.")
else:
    print(len(origin[1]['nodes']), len(escher[1]['nodes']))
    print("nodes is different.")

if len(origin[1]['reactions']) == len(escher[1]['reactions']):
    print(len(origin[1]['reactions']), len(escher[1]['reactions']))
    print("reactions is the same.")
else:
    print(len(origin[1]['reactions']), len(escher[1]['reactions']))
    print("reactions is different.")