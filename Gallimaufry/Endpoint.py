import enforce
import logging

logger = logging.getLogger("USB.Endpoint")

import typing

# Transfer Types
TT_CONTROL     = 0
TT_ISOCHRONOUS = 1
TT_BULK        = 2
TT_INTERRUPT   = 3

@enforce.runtime_validation
class Endpoint:
    """Describes a USB Endpoint.

    Args:
        endpoint_descriptor_packet (dict): Packet for endpoint descriptor.
        pcap (list): list of packets in capture.
        interface (USB.Interface.Interface): pointer to parent interface object.

    Note:
        This class is generally automatically instantiated through
        USB.Interface.Interface.
    """

    def __init__(self, endpoint_descriptor_packet, pcap, interface):
        self.interface = interface

        self._parse_endpoint_descriptor_packet(endpoint_descriptor_packet)

        # This will filter down the pcap to only those packets relevant to this endpoint
        self.pcap = pcap

    def _parse_endpoint_descriptor_packet(self, endpoint_descriptor_packet):
        self.bEndpointAddress = int(endpoint_descriptor_packet['usb.bEndpointAddress'],16)
        self.bmAttributes = int(endpoint_descriptor_packet['usb.bmAttributes'],16)
        self.wMaxPacketSize = int(endpoint_descriptor_packet['usb.wMaxPacketSize'])
        self.bInterval = int(endpoint_descriptor_packet['usb.bInterval'])

    def __repr__(self) -> str:
        return "<Endpoint number={0} direction={1} transfer_type={2} packets={3}>".format(
                self.number,
                self.direction_str,
                self.transfer_type_str,
                len(self.pcap),
                )

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """str: Returns textual summary of this Endpoint."""
        summary = "Endpoint {0}\n".format(self.number)
        summary += "-"*(len(summary)-1) + "\n"
        summary += "direction: {0}\n".format(self.direction_str)
        summary += "transfer_type: {0}\n".format(self.transfer_type_str)
        summary += "packets: {0}\n".format(len(self.pcap))

        return summary

    @property
    def interface(self):
        """USB.Interface.Interface: Parent Interface object."""
        return self.__interface

    @interface.setter
    def interface(self, interface) -> None:
        self.__interface = interface

    @property
    def pcap(self):
        """list: Packet Capture json packets that are relevant to this specific Endpoint."""
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap) -> None:
        self.__pcap = [packet for packet in pcap if
                'usb.endpoint_number' in packet['_source']['layers']['usb'] and
                (int(packet['_source']['layers']['usb']['usb.endpoint_number'],16) & 0b111) == self.number
                ]

    @property
    def usage_type(self) -> typing.Union[int, type(None)]:
        """int: Only applicable for Iso Mode."""
        if self.transfer_type != TT_ISOCHRONOUS:
            logger.error("Usage Type is only applicable for Endpoints of mode Isochronous")
            return None

        return (self.bmAttributes >> 4) & 0b11

    @property
    def usage_type_str(self):
        """str: String representation of Endpoint usage type."""
        t = self.usage_type
        if t == None:
            return None

        types = {
                0: 'Data Endpoint',
                1: 'Feedback Endpoint',
                2: 'Explicit Feedback Data Endpoint',
                3: 'Reserved',
                }

        return types[t]

    @property
    def synchronisation_type(self) -> typing.Union[int, type(None)]:
        """int: Only applicable for Iso Mode."""
        if self.transfer_type != TT_ISOCHRONOUS:
            logger.error("Synchronisation Type is only applicable for Endpoints of mode Isochronous")
            return None

        return (self.bmAttributes >> 2) & 0b11

    @property
    def synchronisation_type_str(self):
        """str: String representation of synchronization type."""
        t = self.synchronisation_type
        if t == None:
            return None

        types = {
                0: 'No Synchonisation',
                1: 'Asynchronous',
                2: 'Adaptive',
                3: 'Synchronous',
                }

        return types[t]

    @property
    def transfer_type(self) -> int:
        """int: What type of transfering will this endpoint use?"""
        return self.bmAttributes & 0b11

    @property
    def transfer_type_str(self) -> str:
        """str: String representation of transfer type."""
        types = {
                TT_CONTROL: 'Control',
                TT_ISOCHRONOUS: 'Isochronous',
                TT_BULK: 'Bulk',
                TT_INTERRUPT: 'Interrupt'
                }
        return types[self.transfer_type]

    @property
    def number(self) -> int:
        """int: This Endpoint's number."""
        return self.bEndpointAddress & 0b111

    @property
    def direction(self) -> int:
        """int: This Endpoint's direction."""
        return (self.bEndpointAddress >> 7) & 1

    @property
    def direction_str(self) -> str:
        """str: String representation of this Endpoint's direction."""
        return "Out" if self.direction == 0 else "In"

    @property
    def bInterval(self) -> int:
        """int: Interval for polling endpoint data transfers."""
        return self.__bInterval

    @bInterval.setter
    def bInterval(self, bInterval: int) -> None:
        self.__bInterval = bInterval

    @property
    def wMaxPacketSize(self) -> int:
        """int: Maximum Packet Size this endpoint is capable of sending or receiving."""
        return self.__wMaxPacketSize

    @wMaxPacketSize.setter
    def wMaxPacketSize(self, wMaxPacketSize: int) -> None:
        self.__wMaxPacketSize = wMaxPacketSize

    @property
    def bmAttributes(self) -> int:
        """int: Bitmap of attributes for this Endpoint."""
        return self.__bmAttributes

    @bmAttributes.setter
    def bmAttributes(self, bmAttributes: int) -> None:
        self.__bmAttributes = bmAttributes

    @property
    def bEndpointAddress(self) -> int:
        """int: This Endpoint's address."""
        return self.__bEndpointAddress

    @bEndpointAddress.setter
    def bEndpointAddress(self, bEndpointAddress: int) -> None:
        self.__bEndpointAddress = bEndpointAddress
