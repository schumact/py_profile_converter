# Standard Library Imports
import json
import argparse

# Local Module Imports
from classes.cyber import from_cyber, to_cyber
from classes.pd import from_pd, to_pd
from classes.phantom import from_phantom, to_phantom


def arg_parser():
    parser = argparse.ArgumentParser(description="EasyConverto Py")
    parser.add_argument('-f', '--former', required=True,
                        help="Json file containing profiles from old bot")
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
}

TO_BOTS = {
    "cyber": to_cyber,
    "phantom": to_phantom,
    "pd": to_pd,
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
                 zipcode=None, city=None, country=None, state=None):
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
                 zipcode=None, city=None, country=None, state=None, same_as_del=None):
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


class CommonFormat:
    def __init__(self):
        self.shipping = Shipping
        self.billing = Billing
        self.card = Card
        self.title = None


def read_from(file):
    parsed = None
    with open(file, 'r') as fi:
        try:
            parsed = json.load(fi)
        except json.JSONDecodeError as e:
            print(e)
    return parsed


def create_profiles_json_file(profiles):
    with open(args.new_file_name, 'w') as fi:
        json.dump(profiles, fi)
        print(f'Success! Profiles have been created in {args.new_file_name}')


def pretty_print_json(json_obj):
    return json.dumps(json_obj, indent=4, sort_keys=True)


if __name__ == '__main__':
    args = arg_parser()
    from_bot = FROM_BOTS[args.former]
    to_bot = TO_BOTS[args.to]
    old_profiles = from_bot(read_from(args.file_), CommonFormat)
    new_profiles = to_bot(old_profiles)
    create_profiles_json_file(new_profiles)
    print('Done')
