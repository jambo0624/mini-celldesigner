import csv
import json

# 读取CSV数据
csv_file = 'test_TCA.csv'
csv_data = {}
related_data = {}
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        csv_data[row['reaction']] = float(row['value'])

# 读取JSON数据
json_file = 'PPPmode.json'
with open(json_file, mode='r') as file:
    json_data = json.load(file)

# 更新JSON数据
reactions = json_data['reactions']
for details in reactions:
    bigg_id = details.get('id')
    if bigg_id in csv_data:
        related_data[bigg_id] = str(csv_data[bigg_id])
        # 添加data到reaction对象
        details['data'] = csv_data[bigg_id]

# 输出更新后的JSON数据
updated_json_file = 'model_with_data.json'
with open(updated_json_file, mode='w') as file:
    json.dump(json_data, file, indent=4)

related_data_file = 'related_data.json'
with open(related_data_file, mode='w') as file:
    json.dump([related_data], file, indent=4)

print("Updated JSON data has been written to", updated_json_file)
