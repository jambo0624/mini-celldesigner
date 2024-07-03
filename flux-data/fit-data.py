import csv
import json

# 读取CSV数据
csv_file = 'test_TCA.csv'
csv_data = {}
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        csv_data[row['reaction']] = float(row['value'])

# 读取JSON数据
json_file = 'RECON1_FIT.json'
with open(json_file, mode='r') as file:
    json_data = json.load(file)

# 更新JSON数据
if len(json_data) >= 1 and 'reactions' in json_data[1]:
    reactions = json_data[1]['reactions']
    for reaction, details in reactions.items():
        bigg_id = details.get('bigg_id')
        if bigg_id in csv_data:
            # 添加data到reaction对象
            details['data'] = csv_data[bigg_id]
            # 添加data到segments对象
            if 'segments' in details:
                for segment in details['segments'].values():
                    segment['data'] = csv_data[bigg_id]

# 输出更新后的JSON数据
updated_json_file = 'updated_example.json'
with open(updated_json_file, mode='w') as file:
    json.dump(json_data, file, indent=4)

print("Updated JSON data has been written to", updated_json_file)
