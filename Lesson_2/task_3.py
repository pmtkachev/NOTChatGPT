"""
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
"""

import yaml

dict_to_yaml = {
    'items': ['ONE', 'two', 'OnE'],
    'number': 4,
    'ya_dict': {
        'one': f'{10}\u20ac',
        'two': f'{100}\u20ac'
    }
}

with open('data.yaml', 'w') as file:
    yaml.dump(dict_to_yaml, file, default_flow_style=False, allow_unicode=True)

with open('data.yaml') as file:
    load_yaml = yaml.load(file, Loader=yaml.FullLoader)
    print(dict_to_yaml == load_yaml)
