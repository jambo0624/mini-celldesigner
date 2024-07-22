import xmltodict
import json

# 读取 XML 文件
with open('SBML_origin_quarter_2.xml', 'r', encoding='utf-8') as xml_file:
    xml_content = xml_file.read()

# 将 XML 转换为字典
xml_dict = xmltodict.parse(xml_content)

# 将字典转换为 JSON 格式
json_data = json.dumps(xml_dict, indent=4)

# 将 JSON 数据写入文件
with open('SBML_origin_quarter_2.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("转换完成，SBML_origin_quarter_2.json 文件。")
