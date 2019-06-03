import random
import string


class ProjectDestroyer:
    def __init__(self, profile):
        self.id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.defaults = dict({"jigAddress": False, "jigPhone": False, "title": profile.title,
                              "cashOnDelivery": False, "dotTrick": False, "email": profile.email,
                              "match": profile.same_as_ship, "limit": profile.limit,
                              "id": self.id})

    @staticmethod
    def set_ship_dict(CommonFormat):
        shipping = CommonFormat.shipping
        ship_dict = {
            "address1": shipping.address_one,
            "address2": shipping.address_two,
            "city": shipping.city,
            "country": shipping.country,
            "firstName": shipping.first,
            "lastName": shipping.last,
            "phone": CommonFormat.phone,
            "state": shipping.state,
            "zipcode": shipping.zipcode
        }
        return ship_dict

    @staticmethod
    def set_billing_dict(CommonFormat):
        billing = CommonFormat.billing
        billing_dict = {
            "address1": billing.address_one,
            "address2": billing.address_two,
            "city": billing.city,
            "country": billing.country,
            "firstName": billing.first,
            "lastName": billing.last,
            "phone": CommonFormat.phone,
            "state": billing.state,
            "zipcode": billing.zipcode
        }
        return billing_dict

    @staticmethod
    def set_card_dict(Card):
        if len(Card.year) == 4:
            Card.year = Card.year[-2:]

        card_dict = {
            "code": Card.cvv,
            "expire": f"{Card.month}/{Card.year}",
            "name": Card.name,
            "number": Card.number
        }
        return card_dict


def set_common_billing(billing_dict, Billing):
    billing = Billing()
    billing.first = billing_dict["firstName"]
    billing.last = billing_dict["lastName"]
    billing.address_one = billing_dict['address1']
    billing.address_two = billing_dict['address2']
    billing.zipcode = billing_dict['zipcode']
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
    shipping.zipcode = shipping_dict['zipcode']
    shipping.city = shipping_dict['city']
    shipping.country = shipping_dict['country']
    shipping.state = shipping_dict['state']
    return shipping


def set_common_card(card_dict, Card):
    expiration = card_dict["expire"].split('/')
    return Card(card_dict["name"], card_dict["number"], expiration[0],
                expiration[1], card_dict["code"])


def from_pd(json_list, CommonFormat):
    profiles = []
    for json_obj in json_list:
        template = CommonFormat()
        template.title = json_obj["title"]
        template.billing = set_common_billing(json_obj['billing'], template.billing)
        template.shipping = set_common_shipping(json_obj['shipping'], template.shipping)
        template.card = set_common_card(json_obj["card"], template.card)
        template.email = json_obj["email"]
        template.phone = json_obj["billing"]["phone"]
        template.same_as_ship = json_obj["match"]
        template.limit = json_obj["limit"]
        profiles.append(template)
    return profiles


def to_pd(common_profiles):
    new_profiles = []
    for profile in common_profiles:
        pd = ProjectDestroyer(profile)
        new_profile = dict(pd.defaults)
        new_profile.update({"shipping": pd.set_ship_dict(profile)})
        new_profile.update({"billing": pd.set_billing_dict(profile)})
        new_profile.update({"card": pd.set_card_dict(profile.card)})
        new_profiles.append(new_profile)
    return new_profiles



