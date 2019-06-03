# Standard Library Imports
import re

card_types = {
    "visa": [
        [4]
    ],
    "discover": [
        [6011],
        [622126, 622925],
        [644, 649],
        [65]
    ],
    "amex": [
        [34],
        [37]
    ],
    "master": [
        [50, 55]
    ]
}


def get_card_type(number):
    if type(number) is not str:
        number = str(number)
    for key, value in card_types.items():
        for each_list in value:
            if len(each_list) > 1:
                for i in range(each_list[0], each_list[1]):
                    num = re.compile(f"{i}")
                    valid = num.match(number)
                    if valid:
                        return key

            else:
                num = re.compile(f"{each_list[0]}")
                valid = num.match(number)
                if valid:
                    return key
    return "Invalid"
