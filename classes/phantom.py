# Local Module Imports
from .credit_card import get_card_type
from .country import abbreviate_country, abbreviate_state


class Phantom:
    def __init__(self, profile):
        profile.shipping.country = abbreviate_country(profile.shipping.country)

        self.defaults = dict({"Name": profile.title, "Phone": profile.phone,
                              "Same": profile.same_as_ship, "Email": profile.email,
                              "Country": profile.shipping.country})

    @staticmethod
    def set_ship_dict(CommonFormat):
        shipping = CommonFormat.shipping
        ship_dict = {
            "FirstName": shipping.first,
            "LastName": shipping.last,
            "Address": shipping.address_one,
            "Apt": shipping.address_two,
            "Zip": shipping.zipcode,
            "City": shipping.city,
            "State": abbreviate_state(shipping.state),
        }
        return ship_dict

    @staticmethod
    def set_billing_dict(CommonFormat):
        billing = CommonFormat.billing
        billing_dict = {
            "FirstName": billing.first,
            "LastName": billing.last,
            "Address": billing.address_one,
            "Apt": billing.address_two,
            "Zip": billing.zipcode,
            "City": billing.city,
            "State": abbreviate_state(billing.state),
        }
        return billing_dict

    @staticmethod
    def set_card_dict(Card):
        if len(Card.year) != 4:
            Card.year = f"20{Card.year}"

        card_dict = {
            "ExpMonth": str(Card.month),
            "ExpYear": Card.year,
            "CCNumber": Card.number,
            "CVV": str(Card.cvv),
            "CardType": get_card_type(Card.number)
        }
        return card_dict


def set_common_billing(billing_dict, Billing, **kwargs):
    billing = Billing()
    country = None
    if "country" in kwargs:
        country = kwargs["country"]
    billing.first = billing_dict["FirstName"]
    billing.last = billing_dict["LastName"]
    billing.address_one = billing_dict['Address']
    billing.address_two = billing_dict['Apt']
    billing.zipcode = billing_dict['Zip']
    billing.city = billing_dict['City']
    billing.country = country
    billing.state = billing_dict['State']
    return billing


def set_common_shipping(shipping_dict, Shipping, **kwargs):
    shipping = Shipping()
    country = None
    if "country" in kwargs:
        country = kwargs["country"]
    shipping.first = shipping_dict['FirstName']
    shipping.last = shipping_dict['LastName']
    shipping.address_one = shipping_dict['Address']
    shipping.address_two = shipping_dict['Apt']
    shipping.zipcode = shipping_dict['Zip']
    shipping.city = shipping_dict['City']
    shipping.country = country
    shipping.state = shipping_dict['State']
    return shipping


def set_common_card(profile, Card):
    return Card(f"{profile['Billing']['FirstName']} {profile['Billing']['LastName']}",
                profile["CCNumber"], profile["ExpMonth"], profile["ExpYear"], profile["CVV"],
                card_type=profile["CardType"])


def from_phantom(json_list, CommonFormat):
    profiles = []
    for json_obj in json_list:
        template = CommonFormat()
        template.title = json_obj["Name"]
        template.billing = set_common_billing(json_obj['Billing'], template.billing,
                                              country=json_obj["Country"])
        template.shipping = set_common_shipping(json_obj["Shipping"], template.shipping,
                                                country=json_obj["Country"])
        template.card = set_common_card(json_obj, template.card)
        template.email = json_obj["Email"]
        template.phone = json_obj["Phone"]
        template.same_as_ship = json_obj["Same"]
        template.limit = True  # oddly enough, no such value in the bot so will set to true
        profiles.append(template)
    return profiles


def to_phantom(common_profiles):
    new_profiles = []
    for profile in common_profiles:
        phantom = Phantom(profile)
        new_profile = dict(phantom.defaults)
        new_profile.update({"Shipping": phantom.set_ship_dict(profile)})
        new_profile.update({"Billing": phantom.set_billing_dict(profile)})
        new_profile.update(phantom.set_card_dict(profile.card))
        new_profiles.append(new_profile)
    return new_profiles
