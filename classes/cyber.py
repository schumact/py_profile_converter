# Standard Library
from random import randint

# Local Module Imports
from .country import full_form_country, full_form_state


class Cyber:
    def __init__(self, profile):
        self.email = profile.email
        self.same_as_ship = profile.same_as_ship
        self.phone = profile.phone
        self.defaults = dict({"name": profile.title, "favourite": False,
                              "one_checkout": profile.limit})

    def set_ship_dict(self, CommonFormat):
        shipping = CommonFormat.shipping
        ship_dict = {
            "first_name": shipping.first,
            "last_name": shipping.last,
            "addr1": shipping.address_one,
            "addr2": shipping.address_two,
            "zip": shipping.zipcode,
            "city": shipping.city,
            "country": full_form_country(shipping.country),
            "state": full_form_state(shipping.state),
            "same_as_del": self.same_as_ship
        }
        return ship_dict

    def set_billing_dict(self, CommonFormat):
        billing = CommonFormat.billing
        billing_dict = {
            "first_name": billing.first,
            "last_name": billing.last,
            "addr1": billing.address_one,
            "addr2": billing.address_two,
            "zip": billing.zipcode,
            "city": billing.city,
            "country": full_form_country(billing.country),
            "state": full_form_state(billing.state),
            "same_as_del": self.same_as_ship
        }
        return billing_dict

    def set_card_dict(self, Card):
        if len(Card.year) != 4:
            Card.year = f"20{Card.year}"

        card_dict = {
            "email": self.email,
            "phone": self.phone,
            "card": {
                "exp_month": str(Card.month),
                "exp_year": Card.year,
                "name": Card.name,
                "number": Card.number,
                "cvv": str(Card.cvv)
            }
        }
        return card_dict


def set_common_billing(billing_dict, Billing):
    billing = Billing()
    billing.first = billing_dict["first_name"]
    billing.last = billing_dict["last_name"]
    billing.address_one = billing_dict['addr1']
    billing.address_two = billing_dict['addr2']
    billing.zipcode = billing_dict['zip']
    billing.city = billing_dict['city']
    billing.country = billing_dict['country']
    billing.state = billing_dict['state']
    return billing


def set_common_shipping(shipping_dict, Shipping):
    shipping = Shipping()
    shipping.first = shipping_dict['first_name']
    shipping.last = shipping_dict['last_name']
    shipping.address_one = shipping_dict['addr1']
    shipping.address_two = shipping_dict['addr2']
    shipping.zipcode = shipping_dict['zip']
    shipping.city = shipping_dict['city']
    shipping.country = shipping_dict['country']
    shipping.state = shipping_dict['state']
    return shipping


def set_common_card(card_dict, Card):
    return Card(card_dict["name"], card_dict["number"], card_dict["exp_month"],
                card_dict["exp_year"], card_dict["cvv"])


def from_cyber(json_obj, CommonFormat):
    profiles = []
    for key, value in json_obj.items():
        template = CommonFormat()
        template.title = key
        template.billing = set_common_billing(value['billing'], template.billing)
        template.shipping = set_common_shipping(value['delivery'], template.shipping)
        template.card = set_common_card(value['payment']["card"], template.card)
        template.email = value["payment"]["email"]
        template.phone = value["payment"]["phone"]
        template.same_as_ship = value["billing"]["same_as_del"]
        template.limit = value["one_checkout"]
        profiles.append(template)
    return profiles


def to_cyber(common_profiles):
    new_profiles = {}
    for profile in common_profiles:
        cyber = Cyber(profile)
        new_profile = dict(cyber.defaults)
        new_profile.update({"delivery": cyber.set_ship_dict(profile)})
        new_profile.update({"billing": cyber.set_billing_dict(profile)})
        new_profile.update({"payment": cyber.set_card_dict(profile.card)})
        try:
            new_profiles[profile.title] = new_profile
        except KeyError as e:
            rand_num = randint(1, 100)
            print(f"Cannot use same name for cyber profile. Duplicate profile"
                  f" {profile.title} is now {profile.title}{rand_num}")
            new_profiles[profile.title + str(rand_num)] = new_profile
    return new_profiles
