import csv


def from_csv(file, separator):
    file_content = ''
    print(separator, type(separator))
    for i,chunk in enumerate(file.chunks()):
        print(i,chunk.decode())
    reader = csv.reader([chunk.decode() for chunk in file.chunks()], dialect=csv.excel_tab, delimiter="\t")
    # print(reader)
    # for i in reader:
    #     print(i)
    #     file_content += ''.join(i)
    # if file_content:
    #     return file_content.split(separator)
    # return None

