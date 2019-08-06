# Standard Library
from random import randint

# Local Module Imports
from .country import abbreviate_country, abbreviate_state


class Latch:
    def __init__(self, profile):
        self.defaults = dict({"name": profile.title, "checkoutOnce": bool(profile.limit),
                              "email": profile.email, "phone": profile.phone})

    def set_ship_dict(self, CommonFormat):
        shipping = CommonFormat.shipping
        ship_dict = {
            "firstName": shipping.first,
            "lastName": shipping.last,
            "address1": shipping.address_one,
            "addrress2": shipping.address_two,
            "zip": shipping.zipcode,
            "city": shipping.city,
            "country": abbreviate_country(shipping.country),
            "state": abbreviate_state(shipping.state),
        }
        return ship_dict

    def set_billing_dict(self, CommonFormat):
        billing = CommonFormat.billing
        billing_dict = {
            "firstName": billing.first,
            "lastName": billing.last,
            "address1": billing.address_one,
            "address2": billing.address_two,
            "zip": billing.zipcode,
            "city": billing.city,
            "country": abbreviate_country(billing.country),
            "state": abbreviate_state(billing.state),
        }
        return billing_dict

    def set_card_dict(self, Card):
        if len(Card.year) != 4:
            Card.year = f"20{Card.year}"

        card_dict = {
            "cardMonth": str(Card.month),
            "cardYear": Card.year,
            "cardName": Card.name,
            "cardNumber": Card.number,
            "cardCVV": str(Card.cvv)
        }
        return card_dict


def set_common_billing(billing_dict, Billing):
    billing = Billing()
    billing.first = billing_dict["firstName"]
    billing.last = billing_dict["lastName"]
    billing.address_one = billing_dict['address1']
    billing.address_two = billing_dict['address2']
    billing.zipcode = billing_dict['zip']
    billing.city = billing_dict['city']
    billing.country = billing_dict['country']
    billing.state = billing_dict['state']
    return billing


def set_common_shipping(shipping_dict, Shipping):
    shipping = Shipping()
    shipping.first = shipping_dict['firstName']
    shipping.last = shipping_dict['lastName']
    shipping.address_one = shipping_dict['address1']
    shipping.address_two = shipping_dict['address2']
    shipping.zipcode = shipping_dict['zip']
    shipping.city = shipping_dict['city']
    shipping.country = shipping_dict['country']
    shipping.state = shipping_dict['state']
    return shipping


def set_common_card(card_dict, Card, *args):
    if card_dict:
        return Card(card_dict["name"], card_dict["number"], card_dict["exp_month"],
                    card_dict["exp_year"], card_dict["cvv"])
    else:
        return Card(args[0], args[1], args[2], args[3], args[4])


def from_latch(json_obj, CommonFormat):
    profiles = []
    for key, value in json_obj.items():
        template = CommonFormat()
        template.title = key
        template.billing = set_common_billing(value['billing'], template.billing)
        template.shipping = set_common_shipping(value['shipping'], template.shipping)
        template.card = set_common_card(None, template.card, value['cardName'], value['cardNumber'],
                                        value['cardMonth'], value['cardYear'], value['cardCVV'])
        template.email = value["email"]
        template.phone = value["phone"]
        template.same_as_ship = True  # setting true as default
        template.limit = value["checkoutOnce"]
        profiles.append(template)
    return profiles


def to_latch(common_profiles):
    new_profiles = {}
    for profile in common_profiles:
        latch = Latch(profile)
        new_profile = dict(latch.defaults)
        new_profile.update({"shipping": latch.set_ship_dict(profile)})
        new_profile.update({"billing": latch.set_billing_dict(profile)})
        new_profile.update(latch.set_card_dict(profile.card))
        try:
            new_profiles[profile.title] = new_profile
        except KeyError as e:
            rand_num = randint(1, 100)
            print(f"Cannot use same name for latch profile. Duplicate profile"
                  f" {profile.title} is now {profile.title}{rand_num}")
            new_profiles[profile.title + str(rand_num)] = new_profile
    return new_profiles
