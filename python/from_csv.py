def from_csv(file_name, separator):
    import csv
    import os
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            csv_in = csv.reader(file)
            file_content = ''
            for i in csv_in:
                file_content += ''.join(i)
            if file_content:
                return file_content.split(separator)
            return None
    return 'no such file'


print(from_csv('texts.csv', '   '))
