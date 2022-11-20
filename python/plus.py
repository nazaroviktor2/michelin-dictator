"""File with funcion plus_to_stress."""


def plus_to_stress(string):
    """Function which turns letters with + to letters with stress.

    Args:
        string: str - string with pluses and letters.

    Returns:
        str - string with stresses without pluses.
    """
    # Á á Ó ó É é ý и́ ы́ э́ ю́ я́
    # а́ е́ и́ о́ у́ ы́ э́ ю́ я́
    letters = {'А': 'Á', 'О': 'Ó', 'Е': 'É', 'У': 'У́', 'И': 'И́', 'Ы': 'Ы́',
               'Э': 'Э́', 'Ю': 'Ю́', 'Я': 'Я́',
               'а': 'а́', 'е': 'е́', 'и': 'и́', 'о': 'о́', 'у': 'у́', 'ы': 'ы́',
               'э': 'э́', 'ю': 'ю́', 'я': 'я́',
               'A': 'Á', 'E': 'É', 'O': 'Ó', 'U': 'Ú', 'I': 'Í', 'Y': 'Ý',
               'a': 'á', 'e': 'é', 'o': 'ó', 'u': 'ú', 'i': 'í', 'y': 'ý'
               }
    while '+' in string:
        ind = string.index('+')
        if ind + 1 < len(string) and string[ind + 1] in letters:
            string = string.replace(string[ind] + string[ind + 1], letters[string[ind + 1]], 1)
        else:
            string = string.replace(string[ind], '', 1)
    return string
# print(plus_to_stress('+м+Yо+и+ктлоьдл+о+\n +Оьлуотлоку+'))
