import logging
logger = logging.getLogger("USB.Classes.HID")

import enforce

from ...Interface import Interface

@enforce.runtime_validation
class HID:

    def __init__(self, interface: Interface):
        """
        interface = pointer to interface class for this to parse
        """

        self.interface = interface

    def __repr__(self) -> str:
        return "<Handler HID>"

    ##############
    # Properties #
    ##############

    @property
    def interface(self) -> Interface:
        """The associated interface for this Handler."""
        return self.__interface

    @interface.setter
    def interface(self, interface: Interface) -> None:
        self.__interface = interface
