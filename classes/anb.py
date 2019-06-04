# Standard Library Imports
import csv
from sys import exit

# Local Module Imports
from .credit_card import get_card_type
from .country import abbreviate_country, abbreviate_state

FIELDS = ["ShippingAsBilling", "FirstNameBilling", "LastNameBilling", "address1Billing",
          "address2Billing", "cityBilling", "stateBilling", "zipCodeBilling",
          "countryBilling", "phoneBilling", "houseNbBilling", "FirstNameShipping",
          "LastNameShipping", "address1Shipping", "address2Shipping", "cityShipping",
          "stateShipping", "zipCodeShipping", "countryShipping", "phoneShipping",
          "houseNbShipping", "friendlyName", "NameOnCard", "DOB", "cardType", "CardNumber",
          "CardExpirationMonth", "CardExpirationYear", "CardSecurityCode", "billingEmail",
          "paypalEmail", "paypalPassword", "CheckoutDelaySeconds", "CheckoutOncePerWebsite"]


def verify_billing(Card):
    if len(Card.year) != 4:
        Card.year = f"20{Card.year}"
    paypal_pass = ""
    paypal_email = ""
    try:
        paypal_pass = Card.kwargs["paypalPassword"]
    except KeyError as e:
        pass
    try:
        paypal_email = Card.kwargs["paypalEmail"]
    except KeyError as e:
        pass

    return Card.year, paypal_pass, paypal_email


def set_common_billing(billing_dict, Billing, **kwargs):
    billing = Billing(houseNbBilling=billing_dict["houseNbBilling"])
    billing.first = billing_dict["FirstNameBilling"]
    billing.last = billing_dict["LastNameBilling"]
    billing.address_one = billing_dict["address1Billing"]
    billing.address_two = billing_dict["address2Billing"]
    billing.zipcode = billing_dict["zipCodeBilling"]
    billing.city = billing_dict["cityBilling"]
    billing.country = billing_dict["countryBilling"]
    billing.state = billing_dict["stateBilling"]
    return billing


def set_common_shipping(shipping_dict, Shipping, **kwargs):
    shipping = Shipping(houseNbShipping=shipping_dict["houseNbShipping"])
    shipping.first = shipping_dict["FirstNameShipping"]
    shipping.last = shipping_dict["LastNameShipping"]
    shipping.address_one = shipping_dict["address1Shipping"]
    shipping.address_two = shipping_dict["address2Shipping"]
    shipping.zipcode = shipping_dict["zipCodeShipping"]
    shipping.city = shipping_dict["cityShipping"]
    shipping.country = shipping_dict["countryShipping"]
    shipping.state = shipping_dict["stateShipping"]
    return shipping


def set_common_card(profile, Card):
    return Card(profile["NameOnCard"], profile["CardNumber"], profile["CardExpirationMonth"],
                profile["CardExpirationYear"], profile["CardSecurityCode"], card_type=profile["cardType"],
                paypalEmail=profile["paypalEmail"], paypalPassword=profile["paypalPassword"])


def from_anb(csv_file, CommonFormat):
    profile_list = []
    with open(csv_file, newline="") as fi:
        profiles = csv.DictReader(fi, fieldnames=FIELDS)
        for index, row in enumerate(profiles):
            template = CommonFormat()
            if index > 0:
                template.title = row["friendlyName"]
                template.billing = set_common_billing(row, template.billing)
                template.shipping = set_common_shipping(row, template.shipping)
                template.card = set_common_card(row, template.card)
                template.email = row["billingEmail"]
                template.phone = row["phoneBilling"]
                template.limit = row["CheckoutOncePerWebsite"]
                template.same_as_ship = row["ShippingAsBilling"]
                profile_list.append(template)

        return profile_list


def construct_csv_row(profile):
    shipping = profile.shipping
    billing = profile.billing
    card = profile.card
    card.year, paypal_pass, paypal_email = verify_billing(card)
    return {"ShippingAsBilling": profile.same_as_ship, "FirstNameBilling": billing.first,
            "LastNameBilling": billing.last, "address1Billing": billing.address_one,
            "address2Billing": billing.address_two, "cityBilling": billing.city,
            "stateBilling": abbreviate_state(billing.state), "zipCodeBilling": billing.zipcode,
            "countryBilling": abbreviate_country(billing.country), "phoneBilling": profile.phone,
            "houseNbBilling": "", "FirstNameShipping": shipping.first,
            "LastNameShipping": shipping.last, "address1Shipping": shipping.address_one,
            "address2Shipping": shipping.address_two, "cityShipping": shipping.city,
            "stateShipping": abbreviate_state(shipping.state), "zipCodeShipping": shipping.zipcode,
            "countryShipping": abbreviate_country(shipping.country), "phoneShipping": profile.phone,
            "houseNbShipping": "", "friendlyName": profile.title, "NameOnCard": card.name,
            "DOB": "2/14/1990", "cardType": get_card_type(card.number), "CardNumber": card.number,
            "CardExpirationMonth": card.month, "CardExpirationYear": card.year,
            "CardSecurityCode": card.cvv, "billingEmail": profile.email,
            "paypalEmail": paypal_email, "paypalPassword": paypal_pass, "CheckoutDelaySeconds": "0",
            "CheckoutOncePerWebsite": profile.limit}


def to_anb(common_profiles, new_csv):
    if not new_csv.endswith('.csv'):
        exit(f"The file to be created, {new_csv} , was not of .csv file type")
    with open(new_csv, 'w', newline='') as fi:
        #  create csv.dictwriter instance without quoting set to quote all so fieldnames
        # can be written (writeheader()) without quotes, as anb accepts them
        dummy_writer = csv.DictWriter(fi, fieldnames=FIELDS, restval='')
        dummy_writer.writeheader()
        writer = csv.DictWriter(fi, fieldnames=FIELDS, restval='', quoting=csv.QUOTE_ALL)
        for profile in common_profiles:
            writer.writerow(construct_csv_row(profile))
    print(f'Success! Profiles output to {new_csv}')
