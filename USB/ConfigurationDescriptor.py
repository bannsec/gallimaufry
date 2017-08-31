import enforce

@enforce.runtime_validation
class ConfigurationDescriptor:

    def __init__(self, packet):
        """
        Represents a USB Configuration Descriptor.

        packet == json packet containing the descriptor for this object

        Ref: http://www.beyondlogic.org/usbnutshell/usb5.shtml#ConfigurationDescriptors
        """
        self._parse_configuration_descriptor(packet)

    def _parse_configuration_descriptor(self, packet):
        # Pull out the descriptor
        descriptor = get_configuration_descriptor(packet)

        self.bNumInterfaces = int(descriptor['usb.bNumInterfaces'])
        self.bConfigurationValue = int(descriptor['usb.bConfigurationValue'])
        self.iConfiguration = int(descriptor['usb.iConfiguration'])
        self.bMaxPower = int(descriptor['usb.bMaxPower']) * 2 # Number specified is in 2mA units
        self.self_powered = bool(int(descriptor['usb.configuration.bmAttributes_tree']['usb.configuration.selfpowered']))
        self.legacy_10bus_powered = bool(int(descriptor['usb.configuration.bmAttributes_tree']['usb.configuration.legacy10buspowered']))
        self.remote_wakeup = bool(int(descriptor['usb.configuration.bmAttributes_tree']['usb.configuration.remotewakeup']))

    def __repr__(self) -> str:
        return "<ConfigurationDescriptor bNumInterfaces={0} bConfigurationValue={1}>".format(self.bNumInterfaces, self.bConfigurationValue)

    ##############
    # Properties #
    ##############

    @property
    def bMaxPower(self) -> int:
        """The maximum power this configuration will drain from the bus, in mA."""
        return self.__bMaxPower

    @bMaxPower.setter
    def bMaxPower(self, bMaxPower: int) -> None:
        self.__bMaxPower = bMaxPower

    @property
    def remote_wakeup(self) -> bool:
        """Does this configuration support remote wakeup?"""
        return self.__remote_wakeup

    @remote_wakeup.setter
    def remote_wakeup(self, remote_wakeup: bool) -> None:
        self.__remote_wakeup = remote_wakeup

    @property
    def legacy_10bus_powered(self) -> bool:
        """Is this legacy 10 bus powered?"""
        return self.__legacy_10bus_powered

    @legacy_10bus_powered.setter
    def legacy_10bus_powered(self, legacy_10bus_powered: bool) -> None:
        self.__legacy_10bus_powered = legacy_10bus_powered

    @property
    def self_powered(self) -> bool:
        """Is this configuration self powered?"""
        return self.__self_powered

    @self_powered.setter
    def self_powered(self, self_powered:bool) -> None:
        self.__self_powered = self_powered

    @property
    def iConfiguration(self) -> int:
        """The string descriptor index for this configuration."""
        return self.__iConfiguration

    @iConfiguration.setter
    def iConfiguration(self, iConfiguration:int) -> None:
        self.__iConfiguration = iConfiguration

    @property
    def bConfigurationValue(self) -> int:
        """The value used to select this configuration."""
        return self.__bConfigurationValue

    @bConfigurationValue.setter
    def bConfigurationValue(self, bConfigurationValue:int) -> None:
        self.__bConfigurationValue = bConfigurationValue

    @property
    def bNumInterfaces(self) -> int:
        """The number of interfaces associated with this Configuration Descriptor."""
        return self.__bNumInterfaces

    @bNumInterfaces.setter
    def bNumInterfaces(self, bNumInterfaces: int) -> None:
        self.__bNumInterfaces = bNumInterfaces

from .helpers import *
