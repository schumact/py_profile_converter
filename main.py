# Standard Library Imports
import json
import argparse
from sys import exit

# Local Module Imports
from classes.cyber import from_cyber, to_cyber
from classes.pd import from_pd, to_pd
from classes.phantom import from_phantom, to_phantom
from classes.anb import from_anb, to_anb
from classes.dashe import from_dashe, to_dashe
from classes.LatchKey import from_latch, to_latch


def arg_parser():
    parser = argparse.ArgumentParser(description="Py Profile Converter. Currently supports "
                                                 "anb, cyber, phantom, dashe, latch and pd")
    parser.add_argument('-f', '--former', required=True,
                        help="Name of bot where profiles are being converted from")
    parser.add_argument('-t', '--to', required=True,
                        help="Bot which will receive json files for importing")
    parser.add_argument('file_', help="Json file containing profiles for conversion")
    parser.add_argument('-n', '--new_file_name', required=True,
                        help="Name of file for profiles to be output to")
    return parser.parse_args()


FROM_BOTS = {
    "cyber": from_cyber,
    "phantom": from_phantom,
    "pd": from_pd,
    "anb": from_anb,
    "dashe": from_dashe,
    "latch": from_latch
}

TO_BOTS = {
    "cyber": to_cyber,
    "phantom": to_phantom,
    "pd": to_pd,
    "anb": to_anb,
    "dashe": to_dashe,
    "latch": to_latch
}


class Card:
    def __init__(self, name, number, month, year, cvv, **kwargs):
        self.name = name
        self.number = number
        self.month = month
        self.year = year
        self.cvv = cvv
        self.kwargs = kwargs


class Billing:
    def __init__(self, first=None, last=None, address_one=None, address_two=None,
                 zipcode=None, city=None, country=None, state=None, **kwargs):
        self.first = first
        self.last = last
        self.address_one = address_one
        self.address_two = address_two
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.state = state


class Shipping:
    def __init__(self, first=None, last=None, email=None, address_one=None, address_two=None,
                 zipcode=None, city=None, country=None, state=None, same_as_del=None, **kwargs):
        self.first = first
        self.last = last
        self.email = email
        self.address_one = address_one
        self.address_two = address_two
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.state = state
        self.same_as_del = same_as_del
        self.kwargs = kwargs


class CommonFormat:
    def __init__(self):
        self.shipping = Shipping
        self.billing = Billing
        self.card = Card
        self.title = None
        self.email = None
        self.phone = None
        self.limit = None
        self.same_as_ship = None


def read_from_json(json_file):
    parsed = None
    try:
        with open(json_file, 'r') as fi:
            parsed = json.load(fi)
    except FileNotFoundError as e:
        exit("Please supply profile json file that already exists.")
    except json.JSONDecodeError as e:
        exit("File does not contain valid Json. Exiting program")

    return parsed


def create_profiles_json_file(profiles):
    if not args.new_file_name.endswith('json'):
        exit(f"The file to be created, {args.new_file_name} ,"
             f" was not of .json file type ")
    with open(args.new_file_name, 'w') as fi:
        json.dump(profiles, fi)
        print(f'Success! Profiles have been created in {args.new_file_name}')


def pretty_print_json(json_obj):
    return json.dumps(json_obj, indent=4, sort_keys=True)


def generate_profiles(to_bot_func, old_profiles):
    if to_bot_func == to_anb:
        return to_bot(old_profiles, args.new_file_name)
    else:
        new_profiles = to_bot_func(old_profiles)
        return create_profiles_json_file(new_profiles)


def from_bot_to_common(from_bot_func):
    if from_bot_func == from_anb:
        return from_bot_func(args.file_, CommonFormat)
    else:
        return from_bot_func(read_from_json(args.file_), CommonFormat)


def convert(from_bot_func, to_bot_func):
    old_profiles = from_bot_to_common(from_bot_func)
    generate_profiles(to_bot_func, old_profiles)


if __name__ == '__main__':
    args = arg_parser()
    if args.former.lower() == args.to.lower():
        exit("-t and -f flags must be different. Cannot convert between the same bot")
    from_bot = None
    to_bot = None
    try:
        from_bot = FROM_BOTS[args.former.lower()]
        to_bot = TO_BOTS[args.to.lower()]
    except KeyError as e:
        exit("Either the -f or -t option was passed an invalid value. "
             "Current valid options for both fields are cyber, pd, phantom")
    convert(from_bot, to_bot)

