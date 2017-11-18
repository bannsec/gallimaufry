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
    
    if "\n{0:04x}".format(vendor_id) not in ids:
        return "Unknown..."

    # Need to find the product id that is part of this vendor
    products = ids.split("\n{0:04x}".format(vendor_id))[1]
    products = products.split("\n")[1:]

    for product in products:
        if not product.startswith("\t"):
            return "Unknown..."
        
        if product.startswith("\t{0:04x}".format(product_id)):
            return product.split("\t{0:04x}".format(product_id))[1].strip()
    
    raise Exception("How did I get here?!")

#
# Does it have the field?
# 

@enforce.runtime_validation
def has_device_descriptor(packet) -> bool:
    return any(True for layer in packet['_source']['layers'].values() if 'usb.bDescriptorType' in layer and int(layer['usb.bDescriptorType'],16) == 1 and 'usb.bmRequestType' not in layer)

@enforce.runtime_validation
def has_configuration_descriptor(packet) -> bool:
    return any(True for layer in packet['_source']['layers'].values() if 'usb.bDescriptorType' in layer and int(layer['usb.bDescriptorType'],16) == 2)

@enforce.runtime_validation
def has_string_descriptor(packet) -> bool:
    return any(True for layer in packet['_source']['layers'].values() if 'usb.bDescriptorType' in layer and int(layer['usb.bDescriptorType'],16) == 3 and 'usb.bString' in layer)

@enforce.runtime_validation
def has_endpoint_descriptor(packet) -> bool:
    return any(True for layer in packet['_source']['layers'].values() if 'usb.bDescriptorType' in layer and int(layer['usb.bDescriptorType'],16) == 4)

#
# Get the fields (assumes we know they exist)
#

@enforce.runtime_validation
def get_configuration_descriptor(packet):
    return next(layer for layer in packet['_source']['layers'].values() if 'usb.bDescriptorType' in layer and int(layer['usb.bDescriptorType'],16) == 2)
