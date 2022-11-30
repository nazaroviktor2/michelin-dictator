def from_json(file_name):
    import json
    import os
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            json_in = json.load(file)
            result = []
            if json_in:
                for i, j in json_in.items():
                    result.append([i]+[elem for elem in j.values()])
                return result
            return 'file is empty'
    return 'no such file'


# print(from_json('texts.json'))
