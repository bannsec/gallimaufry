import enforce
import os
import re

here = os.path.dirname(os.path.realpath(__file__))

def read_usb_ids():
    with open(os.path.join(here,"usb.ids"),"rb") as f:
        ids = f.read().decode('cp1252')
    return ids

@enforce.runtime_validation
def resolve_vendor_id(vendor_id: int) -> str:
    ids = read_usb_ids()

    vendors = re.findall("\n{0:04x} +(.*)?\n".format(vendor_id),ids)

    if len(vendors) > 1:
        print("Matched on multiple vendors?? Please report this (https://github.com/Owlz/usb_pcap). Sticking with the first vendor.")
        vendors = [vendors[0]]

    if len(vendors) == 0:
        return "Unknown..."

    return vendors[0]

@enforce.runtime_validation
def resolve_product_id(vendor_id: int, product_id: int) -> str:
    ids = read_usb_ids()

    # Need to find the product id that is part of this vendor
    products = ids.split("\n{0:04x}".format(vendor_id))[1]
    products = products.split("\n")[1:]

    for product in products:
        if not product.startswith("\t"):
            return "Unknown..."
        
        if product.startswith("\t{0:04x}".format(product_id)):
            return product.split("\t{0:04x}".format(product_id))[1].strip()
    
    raise Exception("How did I get here?!")
