import enforce
import logging

logger = logging.getLogger("USB.Configuration")

import typing
from collections import OrderedDict

@enforce.runtime_validation
class Configuration:
    """Represents a USB Configuration.

    Args:
        packet (dict):  json packet containing the descriptor for this object
        pcap (list): the pcap json blob


    Ref: http://www.beyondlogic.org/usbnutshell/usb5.shtml#ConfigurationDescriptors
    """

    def __init__(self, packet, pcap):
        self.pcap = pcap

        self._parse_configuration_descriptor(packet)

    def _parse_configuration_descriptor(self, packet):
        # Init the interfaces
        self.interfaces = []

        # Pull out the descriptor
        descriptor = get_configuration_descriptor(packet)

        self.bNumInterfaces = int(descriptor['usb.bNumInterfaces'])
        self.bConfigurationValue = int(descriptor['usb.bConfigurationValue'])
        self.iConfiguration = int(descriptor['usb.iConfiguration'])
        self.bMaxPower = int(descriptor['usb.bMaxPower']) * 2 # Number specified is in 2mA units
        self.self_powered = bool(int(descriptor['usb.configuration.bmAttributes_tree']['usb.configuration.selfpowered']))
        self.legacy_10bus_powered = bool(int(descriptor['usb.configuration.bmAttributes_tree']['usb.configuration.legacy10buspowered']))
        self.remote_wakeup = bool(int(descriptor['usb.configuration.bmAttributes_tree']['usb.configuration.remotewakeup']))

        # Loop through the configurations
        found_config = False
        for layer in packet['_source']['layers'].values():
            # Is this a config field?
            if 'usb.bDescriptorType' in layer and int(layer['usb.bDescriptorType'],16) == 2:
                found_config = True
                continue

            # If we haven't hit the config yet, move on
            if not found_config:
                continue

            # Interface Descriptor
            if int(layer['usb.bDescriptorType'],16) == 0x4:
                self.interfaces.append(Interface(layer, pcap=self.pcap))

            # HID Descriptor
            elif int(layer['usb.bDescriptorType'],16) == 0x21:
                self.interfaces[-1]._parse_hid_descriptor_packet(layer)

            # Endpoint Descriptor
            elif int(layer['usb.bDescriptorType'],16) == 0x5:
                self.interfaces[-1]._parse_endpoint_descriptor_packet(layer)

            else:
                logger.error("Not sure what this descriptor is... usb.bDescriptorType = {0}".format(int(layer['usb.bDescriptorType'],16)))

        # Instantiate any handlers
        for interface in self.interfaces:
            interface.handler

    def __repr__(self) -> str:
        return "<Configuration bNumInterfaces={0} bConfigurationValue={1}>".format(self.bNumInterfaces, self.bConfigurationValue)

    ##############
    # Properties #
    ##############

    @property
    def pcap(self) -> typing.List[OrderedDict]:
        """list: List of packets relevant to this Configuration."""
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap: typing.List[OrderedDict]) -> None:
        self.__pcap = pcap

    @property
    def summary(self) -> str:
        """str: Textual summary of this Configuration."""
        summary  = "Configuration {0}\n".format(self.bConfigurationValue)
        summary += "-" * (len(summary) - 1) + "\n"

        summary += "bNumInterfaces = {0}\n".format(self.bNumInterfaces)
        summary += "self_powered = {0}\n".format(self.self_powered)
        summary += "remote_wakeup = {0}\n\n".format(self.remote_wakeup)

        summary += "Interfaces\n"
        summary += "-----------\n"

        # Loop through Interfaces
        for interface in self.interfaces:
            summary += "\n"
            for line in interface.summary.split("\n"):
                summary +=  " "*4 + line + "\n"

        return summary.strip()

    @property
    def interfaces(self) -> list:
        """list: Each USB Configuration has at least one interface."""
        return self.__interfaces

    @interfaces.setter
    def interfaces(self, interfaces: list) -> None:
        self.__interfaces = interfaces

    @property
    def bMaxPower(self) -> int:
        """int: The maximum power this configuration will drain from the bus, in mA."""
        return self.__bMaxPower

    @bMaxPower.setter
    def bMaxPower(self, bMaxPower: int) -> None:
        self.__bMaxPower = bMaxPower

    @property
    def remote_wakeup(self) -> bool:
        """bool: Does this configuration support remote wakeup?"""
        return self.__remote_wakeup

    @remote_wakeup.setter
    def remote_wakeup(self, remote_wakeup: bool) -> None:
        self.__remote_wakeup = remote_wakeup

    @property
    def legacy_10bus_powered(self) -> bool:
        """bool: Is this legacy 10 bus powered?"""
        return self.__legacy_10bus_powered

    @legacy_10bus_powered.setter
    def legacy_10bus_powered(self, legacy_10bus_powered: bool) -> None:
        self.__legacy_10bus_powered = legacy_10bus_powered

    @property
    def self_powered(self) -> bool:
        """bool: Is this configuration self powered?"""
        return self.__self_powered

    @self_powered.setter
    def self_powered(self, self_powered:bool) -> None:
        self.__self_powered = self_powered

    @property
    def iConfiguration(self) -> int:
        """int: The string descriptor index for this configuration."""
        return self.__iConfiguration

    @iConfiguration.setter
    def iConfiguration(self, iConfiguration:int) -> None:
        self.__iConfiguration = iConfiguration

    @property
    def bConfigurationValue(self) -> int:
        """int: The value used to select this configuration."""
        return self.__bConfigurationValue

    @bConfigurationValue.setter
    def bConfigurationValue(self, bConfigurationValue:int) -> None:
        self.__bConfigurationValue = bConfigurationValue

    @property
    def bNumInterfaces(self) -> int:
        """int: The number of interfaces associated with this Configuration Descriptor."""
        return self.__bNumInterfaces

    @bNumInterfaces.setter
    def bNumInterfaces(self, bNumInterfaces: int) -> None:
        self.__bNumInterfaces = bNumInterfaces

from .helpers import *
from .Interface import Interface
