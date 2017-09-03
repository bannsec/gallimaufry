import enforce
import logging

logger = logging.getLogger("USB.Endpoint")

# Transfer Types
TT_CONTROL     = 0
TT_ISOCHRONOUS = 1
TT_BULK        = 2
TT_INTERRUPT   = 3

@enforce.runtime_validation
class Endpoint:

    def __init__(self, endpoint_descriptor_packet, pcap):
        """
        endpoint_descriptor_packet = json packet for endpoint descriptor
        pcap = json packet capture
        """
        self._parse_endpoint_descriptor_packet(endpoint_descriptor_packet)

        # This will filter down the pcap to only those packets relevant to this endpoint
        self.pcap = pcap

    def _parse_endpoint_descriptor_packet(self, endpoint_descriptor_packet):
        print(endpoint_descriptor_packet)

        self.bEndpointAddress = int(endpoint_descriptor_packet['usb.bEndpointAddress'],16)
        self.bmAttributes = int(endpoint_descriptor_packet['usb.bmAttributes'],16)
        self.wMaxPacketSize = int(endpoint_descriptor_packet['usb.wMaxPacketSize'])
        self.bInterval = int(endpoint_descriptor_packet['usb.bInterval'])

    def __repr__(self) -> str:
        return "<Endpoint number={0} direction={1} transfer_type={2}>".format(self.number, self.direction_str, self.transfer_type_str)

    ##############
    # Properties #
    ##############

    @property
    def pcap(self):
        """Packet Capture json packets that are relevant to this specific Endpoint."""
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap) -> None:
        self.__pcap = [packet for packet in pcap if
                'usb.endpoint_number' in packet['_source']['layers']['usb'] and
                (int(packet['_source']['layers']['usb']['usb.endpoint_number'],16) & 0b111) == self.number
                ]

    @property
    def usage_type(self):
        """Only applicable for Iso Mode."""
        if self.transfer_type != TT_ISOCHRONOUS:
            logger.error("Usage Type is only applicable for Endpoints of mode Isochronous")
            return None

        return (self.bmAttributes >> 4) & 0b11

    @property
    def usage_type_str(self):
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
    def synchronisation_type(self):
        """Only applicable for Iso Mode."""
        if self.transfer_type != TT_ISOCHRONOUS:
            logger.error("Synchronisation Type is only applicable for Endpoints of mode Isochronous")
            return None

        return (self.bmAttributes >> 2) & 0b11

    @property
    def synchronisation_type_str(self):
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
        return self.bmAttributes & 0b11

    @property
    def transfer_type_str(self) -> str:
        types = {
                TT_CONTROL: 'Control',
                TT_ISOCHRONOUS: 'Isochronous',
                TT_BULK: 'Bulk',
                TT_INTERRUPT: 'Interrupt'
                }
        return types[self.transfer_type]

    @property
    def number(self) -> int:
        return self.bEndpointAddress & 0b111

    @property
    def direction(self) -> int:
        return (self.bEndpointAddress >> 7) & 1

    @property
    def direction_str(self) -> str:
        return "Out" if self.direction == 0 else "In"

    @property
    def bInterval(self) -> int:
        return self.__bInterval

    @bInterval.setter
    def bInterval(self, bInterval: int) -> None:
        self.__bInterval = bInterval

    @property
    def wMaxPacketSize(self) -> int:
        return self.__wMaxPacketSize

    @wMaxPacketSize.setter
    def wMaxPacketSize(self, wMaxPacketSize: int) -> None:
        self.__wMaxPacketSize = wMaxPacketSize

    @property
    def bmAttributes(self) -> int:
        return self.__bmAttributes

    @bmAttributes.setter
    def bmAttributes(self, bmAttributes: int) -> None:
        self.__bmAttributes = bmAttributes

    @property
    def bEndpointAddress(self) -> int:
        return self.__bEndpointAddress

    @bEndpointAddress.setter
    def bEndpointAddress(self, bEndpointAddress: int) -> None:
        self.__bEndpointAddress = bEndpointAddress
