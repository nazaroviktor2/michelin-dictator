def bold(string):
    cnt = 0
    for i in string:
        if cnt == 1 and i == '*':
            string = string.replace(i, '</b>', 1)
            cnt = 0
        elif i == '*':
            string = string.replace(i, '<b>', 1)
            cnt += 1
    return string


print(bold('CGHBJ*DNK B*HJB KJBKN* JKNJK'))