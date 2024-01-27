def get_upper_first_three_letters(string):
    if len(string) >= 3:
        return string[:3].upper()
    else:
        return string.ljust(3, "0").upper()
