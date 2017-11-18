import enforce
import typing
from .HID import HID
from .Endpoint import Endpoint
from .Classes import get_class_handler

@enforce.runtime_validation
class Interface:
    """Describes a USB Interface.

    Args:
        interface_descriptor_packet (dict): json of the interface descriptor packet that defines this interface.
        pcap (list): list of pcap packets from capture.

    Note:
        This is generally created automatically from the
        Gallimaufry.Configuration.Configuration class.
    """

    def __init__(self,interface_descriptor_packet, pcap):
        # Store the pcap
        self.pcap = pcap

        # These will be filled in by the handler
        self.subclass_str = None
        self.protocol_str = None

        # Assume no HID
        self.hid = None

        # No known endpoints to start with
        self.endpoints = []

        self._parse_interface_descriptor_packet(interface_descriptor_packet)

    def _parse_interface_descriptor_packet(self, interface_descriptor_packet):
        self.bInterfaceNumber = int(interface_descriptor_packet['usb.bInterfaceNumber'])
        self.bAlternateSetting = int(interface_descriptor_packet['usb.bAlternateSetting'])
        self.bNumEndpoints = int(interface_descriptor_packet['usb.bNumEndpoints'])
        self.bInterfaceClass = int(interface_descriptor_packet['usb.bInterfaceClass'])
        self.bInterfaceSubClass = int(interface_descriptor_packet['usb.bInterfaceSubClass'],0)
        self.bInterfaceProtocol = int(interface_descriptor_packet['usb.bInterfaceProtocol'],16)
        self.iInterface = int(interface_descriptor_packet['usb.iInterface'])

    def _parse_hid_descriptor_packet(self, hid_descriptor_packet):
        self.hid = HID(hid_descriptor_packet)

    def _parse_endpoint_descriptor_packet(self, endpoint_descriptor_packet):
        # This is called from the Configuration Descriptor parsing
        self.endpoints.append(Endpoint(endpoint_descriptor_packet, pcap=self.pcap, interface=self))

    def __repr__(self) -> str:
        return "<Interface {1} bInterfaceNumber={0}>".format(self.bInterfaceNumber, self.class_str)

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """str: Textual summary of this interface."""
        summary = "Interface {0}\n".format(self.bInterfaceNumber)
        summary += "-"*(len(summary)-1) + "\n"

        summary += "Class: {0}\n".format(self.class_str)

        if self.subclass_str != None:
            summary += "SubClass: {0}\n".format(self.subclass_str)

        if self.protocol_str != None:
            summary += "Protocol: {0}\n".format(self.protocol_str)

        summary += "\n"
        summary += "Endpoints\n"
        summary += "---------\n"

        # Loop through Endpoints
        for endpoint in self.endpoints:
            summary += "\n"
            for line in endpoint.summary.split("\n"):
                summary +=  " "*4 + line + "\n"

        return summary.strip()

    @property
    def protocol_str(self) -> typing.Union[str, type(None)]:
        """str: String representation of interface's USB protocol."""
        return self.__protocol_str

    @protocol_str.setter
    def protocol_str(self, protocol_str: typing.Union[str, type(None)]) -> None:
        self.__protocol_str = protocol_str

    @property
    def subclass_str(self) -> typing.Union[str, type(None)]:
        """str: String representation of the interface's USB subclass."""
        return self.__subclass_str

    @subclass_str.setter
    def subclass_str(self, subclass_str: typing.Union[str, type(None)]) -> None:
        self.__subclass_str = subclass_str

    @property
    def handler(self):
        """Returns the handler, if known, for this interface."""

        # First request? Resolve it
        if not hasattr(self, "_Interface__handler"):
            self.__handler = get_class_handler(self.bInterfaceClass)

            # If we found one
            if self.__handler != None:
                self.__handler = self.__handler(self)

        return self.__handler

    @property
    def endpoints(self) -> typing.List[Endpoint]:
        """list: List of Endpoints for this Interface."""
        return self.__endpoints

    @endpoints.setter
    def endpoints(self, endpoints: typing.List[Endpoint]) -> None:
        self.__endpoints = endpoints

    @property
    def hid(self) -> typing.Union[type(None), HID]:
        """Gallimaufry.HID.HID: Returns the HID object for this Interface, if one exists, otherwise None"""
        return self.__hid

    @hid.setter
    def hid(self, hid: typing.Union[type(None), HID]) -> None:
        self.__hid = hid

    @property
    def iInterface(self) -> int:
        """int: Index of String Descriptor Describing this interface."""
        return self.__iInterface

    @iInterface.setter
    def iInterface(self, iInterface: int) -> None:
        self.__iInterface = iInterface

    @property
    def bInterfaceProtocol(self) -> int:
        """int: Protocol Code (Assigned by USB Org) for this interface."""
        return self.__bInterfaceProtocol

    @bInterfaceProtocol.setter
    def bInterfaceProtocol(self, bInterfaceProtocol: int) -> None:
        self.__bInterfaceProtocol = bInterfaceProtocol

    @property
    def bInterfaceSubClass(self) -> int:
        """int: Subclass Code (Assigned by USB Org) for this interface."""
        return self.__bInterfaceSubClass

    @bInterfaceSubClass.setter
    def bInterfaceSubClass(self, bInterfaceSubClass: int) -> None:
        self.__bInterfaceSubClass = bInterfaceSubClass

    @property
    def bInterfaceClass(self) -> int:
        """int: Class Code (Assigned by USB Org) for this interface."""
        return self.__bInterfaceClass

    @bInterfaceClass.setter
    def bInterfaceClass(self, bInterfaceClass: int) -> None:
        self.__bInterfaceClass = bInterfaceClass

    @property
    def class_str(self) -> str:
        """str: Returns the class of this interface as a string."""
        return Gallimaufry.Classes.classes[self.bInterfaceClass]

    @property
    def bNumEndpoints(self) -> int:
        """int: Number of Endpoints used for this interface"""
        return self.__bNumEndpoints

    @bNumEndpoints.setter
    def bNumEndpoints(self, bNumEndpoints: int) -> None:
        self.__bNumEndpoints = bNumEndpoints

    @property
    def bAlternateSetting(self) -> int:
        """int: Value used to select alternative setting"""
        return self.__bAlternateSetting

    @bAlternateSetting.setter
    def bAlternateSetting(self, bAlternateSetting: int) -> None:
        self.__bAlternateSetting = bAlternateSetting

    @property
    def bInterfaceNumber(self) -> int:
        """int: Number of Interface"""
        return self.__bInterfaceNumber

    @bInterfaceNumber.setter
    def bInterfaceNumber(self, bInterfaceNumber: int) -> None:
        self.__bInterfaceNumber = bInterfaceNumber

import Gallimaufry.Classes
