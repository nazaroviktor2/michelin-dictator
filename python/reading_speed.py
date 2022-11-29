def replace_all(text, lst):
    for i in lst:
        text = text.replace(i, '')
    return text


def speed(text, average_error, average_speed):
    arr = [i for i in '!@#$%^&()_-,./;:|\~`']
    number_of_words = len(replace_all(text, arr).split())
    result_speed = number_of_words//average_speed
    return [result_speed - error, result_speed + error]

print(speed('GYTFdhvegv ,kmlew fwe#l ,'))