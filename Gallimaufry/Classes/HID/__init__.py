import logging
logger = logging.getLogger("USB.Classes.HID")

import enforce

SC_NONE = 0
SC_BOOT = 1

PROTO_NONE     = 0
PROTO_KEYBOARD = 1
PROTO_MOUSE    = 2

subclass_str = {
        SC_NONE: 'No Subclass',
        SC_BOOT: 'Boot Interface Subclass',
    }

protocol_str = {
        PROTO_NONE     : 'None',
        PROTO_KEYBOARD : 'Keyboard',
        PROTO_MOUSE    : 'Mouse',
    }

@enforce.runtime_validation
class HID:

    def __init__(self, interface):
        """
        interface = pointer to interface class for this to parse
        """

        self.interface = interface

        self._parse_interface()

        self._parse_endpoints()

    def _parse_endpoints(self):
        """Attempt to parse any information out of the endpoints."""
        
        # TODO: Actually use the HID descriptors...
        # Using subclass and proto for now

        # Loop through each endpoint
        for endpoint in self.interface.endpoints:
            if self.interface.bInterfaceProtocol == PROTO_KEYBOARD:
                endpoint.keyboard = Keyboard(endpoint.pcap)
            # TODO: mouse
        

    def _parse_interface(self):
        """Initial parsing of what type of interface this is."""

        # Just warn for now
        if self.interface.bInterfaceClass != 0x3:
            logger.warn("Interface class is not 3... This is likely the wrong handler!")

        # Update the subclass and protocol
        self.interface.subclass_str = subclass_str[self.interface.bInterfaceSubClass]
        self.interface.protocol_str = protocol_str[self.interface.bInterfaceProtocol]


    def __repr__(self) -> str:
        return "<Handler HID>"

    ##############
    # Properties #
    ##############

    @property
    def interface(self):
        """The associated interface for this Handler."""
        return self.__interface

    @interface.setter
    def interface(self, interface) -> None:
        self.__interface = interface

from .Keyboard import Keyboard
