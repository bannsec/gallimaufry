import enforce
import typing
from .HID import HID

@enforce.runtime_validation
class Interface:

    def __init__(self,interface_descriptor_packet):
        """
        interface_descriptor_packet == json of the interface descriptor packet that defines this interface.
        """

        # Assume no HID
        self.hid = None

        self._parse_interface_descriptor_packet(interface_descriptor_packet)

    def _parse_interface_descriptor_packet(self, interface_descriptor_packet):
        self.bInterfaceNumber = int(interface_descriptor_packet['usb.bInterfaceNumber'])
        self.bAlternateSetting = int(interface_descriptor_packet['usb.bAlternateSetting'])
        self.bNumEndpoints = int(interface_descriptor_packet['usb.bNumEndpoints'])
        self.bInterfaceClass = int(interface_descriptor_packet['usb.bInterfaceClass'])
        self.bInterfaceSubClass = int(interface_descriptor_packet['usb.bInterfaceSubClass'])
        self.bInterfaceProtocol = int(interface_descriptor_packet['usb.bInterfaceProtocol'],16)
        self.iInterface = int(interface_descriptor_packet['usb.iInterface'])

    def _parse_hid_descriptor_packet(self, hid_descriptor_packet):
        self.hid = HID(hid_descriptor_packet)

    def __repr__(self) -> str:
        return "<Interface bInterfaceNumber={0}>".format(self.bInterfaceNumber)

    ##############
    # Properties #
    ##############

    @property
    def hid(self) -> typing.Union[type(None), HID]:
        """
        Returns the HID object for this Interface, if one exists, otherwise None
        """
        return self.__hid

    @hid.setter
    def hid(self, hid: typing.Union[type(None), HID]) -> None:
        self.__hid = hid

    @property
    def iInterface(self) -> int:
        return self.__iInterface

    @iInterface.setter
    def iInterface(self, iInterface: int) -> None:
        self.__iInterface = iInterface

    @property
    def bInterfaceProtocol(self) -> int:
        return self.__bInterfaceProtocol

    @bInterfaceProtocol.setter
    def bInterfaceProtocol(self, bInterfaceProtocol: int) -> None:
        self.__bInterfaceProtocol = bInterfaceProtocol

    @property
    def bInterfaceSubClass(self) -> int:
        return self.__bInterfaceSubClass

    @bInterfaceSubClass.setter
    def bInterfaceSubClass(self, bInterfaceSubClass: int) -> None:
        self.__bInterfaceSubClass = bInterfaceSubClass

    @property
    def bInterfaceClass(self) -> int:
        return self.__bInterfaceClass

    @bInterfaceClass.setter
    def bInterfaceClass(self, bInterfaceClass: int) -> None:
        self.__bInterfaceClass = bInterfaceClass

    @property
    def bNumEndpoints(self) -> int:
        return self.__bNumEndpoints

    @bNumEndpoints.setter
    def bNumEndpoints(self, bNumEndpoints: int) -> None:
        self.__bNumEndpoints = bNumEndpoints

    @property
    def bAlternateSetting(self) -> int:
        return self.__bAlternateSetting

    @bAlternateSetting.setter
    def bAlternateSetting(self, bAlternateSetting: int) -> None:
        self.__bAlternateSetting = bAlternateSetting

    @property
    def bInterfaceNumber(self) -> int:
        return self.__bInterfaceNumber

    @bInterfaceNumber.setter
    def bInterfaceNumber(self, bInterfaceNumber: int) -> None:
        self.__bInterfaceNumber = bInterfaceNumber

