import datetime


def replace_all(text, lst):
    for i in lst:
        text = text.replace(i, '')
    return text


def reading_speed(text, average_error, average_speed):
    arr = [i for i in '!@#$%^&()_-,./;:|\~`']
    number_of_words = len(replace_all(text, arr).split())
    result_speed = number_of_words//average_speed
    return datetime.timedelta(seconds=result_speed - average_error), datetime.timedelta(seconds=result_speed + average_error)

# print(speed('GYTFdhvegv ,kmlew fwe#l ,'))
