import enforce

@enforce.runtime_validation
class HID:
    """Describes a USB HID.

    Args:
        hid_descriptor_packet (dict): hid_descriptor_packet
    """

    def __init__(self, hid_descriptor_packet):
        self._parse_hid_descriptor_packet(hid_descriptor_packet)

    def _parse_hid_descriptor_packet(self, hid_descriptor_packet):
        self.bcdHID = int(hid_descriptor_packet['usbhid.descriptor.hid.bcdHID'],16)
        self.bCountryCode = int(hid_descriptor_packet['usbhid.descriptor.hid.bCountryCode'],16)
        self.bNumDescriptors = int(hid_descriptor_packet['usbhid.descriptor.hid.bNumDescriptors'])
        self.bDescriptorType = int(hid_descriptor_packet['usbhid.descriptor.hid.bDescriptorType'])
        self.wDescriptorLength = int(hid_descriptor_packet['usbhid.descriptor.hid.wDescriptorLength'])

    def __repr__(self) -> str:
        return "<HID bNumDescriptors={0}>".format(self.bNumDescriptors)


    ##############
    # Properties #
    ##############

    @property
    def wDescriptorLength(self) -> int:
        return self.__wDescriptorLength

    @wDescriptorLength.setter
    def wDescriptorLength(self, wDescriptorLength: int) -> None:
        self.__wDescriptorLength = wDescriptorLength

    @property
    def bDescriptorType(self) -> int:
        return self.__bDescriptorType

    @bDescriptorType.setter
    def bDescriptorType(self, bDescriptorType: int) -> None:
        self.__bDescriptorType = bDescriptorType

    @property
    def bNumDescriptors(self) -> int:
        return self.__bNumDescriptors

    @bNumDescriptors.setter
    def bNumDescriptors(self, bNumDescriptors: int) -> None:
        self.__bNumDescriptors = bNumDescriptors

    @property
    def bCountryCode(self) -> int:
        return self.__bCountryCode

    @bCountryCode.setter
    def bCountryCode(self, bCountryCode: int) -> None:
        self.__bCountryCode = bCountryCode

    @property
    def bcdHID(self) -> int:
        return self.__bcdHID

    @bcdHID.setter
    def bcdHID(self, bcdHID: int) -> None:
        self.__bcdHID = bcdHID

