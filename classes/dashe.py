# Standard Library
from random import randint

# Local Module Imports
from .country import full_form_country, full_form_state


class Dashe:
    def __init__(self, profile):
        self.email = profile.email
        self.same_as_ship = profile.same_as_ship
        self.phone = profile.phone
        self.defaults = dict({"email": self.email, "profileName": profile.title,
                              "billingMatch": self.same_as_ship})

    def set_ship_dict(self, CommonFormat):
        shipping = CommonFormat.shipping
        ship_dict = {
            "firstName": shipping.first,
            "lastName": shipping.last,
            "address": shipping.address_one,
            "apt": shipping.address_two,
            "zipCode": shipping.zipcode,
            "city": shipping.city,
            "phoneNumber": self.phone,
            "country": full_form_country(shipping.country),
            "state": full_form_state(shipping.state),
        }
        return ship_dict

    def set_billing_dict(self, CommonFormat):
        billing = CommonFormat.billing
        billing_dict = {
            "firstName": billing.first,
            "lastName": billing.last,
            "address": billing.address_one,
            "apt": billing.address_two,
            "zipCode": billing.zipcode,
            "city": billing.city,
            "phoneNumber": self.phone,
            "country": full_form_country(billing.country),
            "state": full_form_state(billing.state),
        }
        return billing_dict

    def set_card_dict(self, Card):
        if len(Card.year) != 4:
            Card.year = f"20{Card.year}"

        card_dict = {
            "card": {
                "month": str(Card.month),
                "year": Card.year,
                "holder": Card.name,
                "number": Card.number,
                "cvv": str(Card.cvv)
            }
        }
        return card_dict


def set_common_billing(billing_dict, Billing):
    billing = Billing()
    billing.first = billing_dict["firstName"]
    billing.last = billing_dict["lastName"]
    billing.address_one = billing_dict['address']
    billing.address_two = billing_dict['apt']
    billing.zipcode = billing_dict['zipCode']
    billing.city = billing_dict['city']
    billing.country = billing_dict['country']
    billing.state = billing_dict['state']
    return billing


def set_common_shipping(shipping_dict, Shipping):
    shipping = Shipping()
    shipping.first = shipping_dict['firstName']
    shipping.last = shipping_dict['lastName']
    shipping.address_one = shipping_dict['address']
    shipping.address_two = shipping_dict['apt']
    shipping.zipcode = shipping_dict['zipCode']
    shipping.city = shipping_dict['city']
    shipping.country = shipping_dict['country']
    shipping.state = shipping_dict['state']
    return shipping


def set_common_card(card_dict, Card):
    return Card(card_dict["holder"], card_dict["number"],
                card_dict["month"], card_dict["year"], card_dict["cvv"])


def from_dashe(json_obj, CommonFormat):
    profiles = []
    for key, value in json_obj.items():
        template = CommonFormat()
        template.title = key
        template.billing = set_common_billing(value['billing'], template.billing)
        template.shipping = set_common_shipping(value['shipping'], template.shipping)
        template.card = set_common_card(value["card"], template)
        template.email = value["email"]
        template.phone = value["shipping"]["phoneNumber"]
        template.same_as_ship = value["billingMatch"]
        profiles.append(template)
    return profiles


def to_dashe(common_profiles):
    new_profiles = {}
    for profile in common_profiles:
        dashe = Dashe(profile)
        new_profile = dict(dashe.defaults)
        new_profile.update({"delivery": dashe.set_ship_dict(profile)})
        new_profile.update({"billing": dashe.set_billing_dict(profile)})
        new_profile.update({"payment": dashe.set_card_dict(profile.card)})
        try:
            new_profiles[profile.title] = new_profile
        except KeyError as e:
            rand_num = randint(1, 100)
            print(f"Cannot use same name for dashe profile. Duplicate profile"
                  f" {profile.title} is now {profile.title}{rand_num}")
            new_profiles[profile.title + str(rand_num)] = new_profile
    return new_profiles
