def from_csv(file_name):
    import csv
    import os
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            csv_in = csv.reader(file)
            if csv_in:
                return [i for i in csv_in]
            return 'file is empty'
    return 'no such file'


#print(from_csv('texts.csv'))
