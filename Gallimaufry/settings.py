
# Shared settings across multiple modules
# This is basically used like a super global across modules.


# Init the variables to share
def init():
    global usb_endpoint_designator
    usb_endpoint_designator = "usb.endpoint_number" # This may change based on wireshark version.

if 'usb_endpoint_designator' not in globals():
    init()
