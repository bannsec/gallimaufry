import logging
logger = logging.getLogger("USB.Device")

import enforce

@enforce.runtime_validation
class Device:
    """Defines a USB device.
    
    Args:
        device_descriptor (dict): The device descriptor packet to use in generating this device object.
        pcap (list): The full list of packets as returned by tshark.

    """

    def __init__(self, device_descriptor, pcap):
        self.string_descriptors = {}
        self._parse_device_descriptor(device_descriptor)

        # PCAP will filter the pcap down to only this device
        self.pcap = pcap

        self._resolve_string_descriptors()
        self._parse_configuration_descriptors()

    def _parse_configuration_descriptors(self) -> None:
        """Discover and add configuration descriptors to this device."""
        self.configurations = []
        
        # Find all the configuration descriptors
        for packet in self.pcap:
            if has_configuration_descriptor(packet) and has_endpoint_descriptor(packet):
                self.configurations.append(Configuration(packet, pcap=self.pcap))

        # Sanity check
        if len(self.configurations) != self.bNumConfigurations:
            logger.warn("Expected {0} Descriptors. Found {1}.".format(self.bNumConfigurations, len(self.configurations)))


    def _resolve_string_descriptors(self):
        """Look up any string descriptors for this device that have been transferred."""

        # Grab any string descriptor packets for this device
        string_descriptors = (packet for packet in self.pcap if has_string_descriptor(packet))

        # For each, figure out what the request was for
        for descriptor in string_descriptors:
            request_frame = int(descriptor['_source']['layers']['usb']['usb.request_in'])
            packet = next(packet for packet in self.pcap if int(packet['_source']['layers']['frame']['frame.number']) == request_frame)
            iDescriptor = int(packet['_source']['layers']['URB setup']['usb.DescriptorIndex'],16)
            bString = descriptor['_source']['layers']['STRING DESCRIPTOR']['usb.bString']

            self.string_descriptors[iDescriptor] = bString


    def _parse_device_descriptor(self, device_descriptor) -> None:
        """Given a descriptor packet, parse out the fields."""
        
        self.bus_id = int(device_descriptor['_source']['layers']['usb']['usb.bus_id'])
        self.device_address = int(device_descriptor['_source']['layers']['usb']['usb.device_address'])
        self.bNumConfigurations = int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.bNumConfigurations'])

        bcdUSB = "{0:04x}".format(int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.bcdUSB'],16))
        self.bluetooth_major = int(bcdUSB[:2],10)
        self.bluetooth_minor = int(bcdUSB[2:3],10)
        self.bluetooth_subminor = int(bcdUSB[3:4],10)

        bcdDevice = "{0:04x}".format(int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.bcdDevice'],16))
        self.device_major = int(bcdDevice[:2],10)
        self.device_minor = int(bcdDevice[2:3],10)
        self.device_subminor = int(bcdDevice[3:4],10)

        self.idVendor = int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.idVendor'],10)
        self.idProduct = int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.idProduct'],16)
        self.iManufacturer = int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.iManufacturer'],10)
        self.iProduct = int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.iProduct'],10)
        self.iSerialNumber = int(device_descriptor['_source']['layers']['DEVICE DESCRIPTOR']['usb.iSerialNumber'],10)

    def __repr__(self) -> str:
        return "<{4} {5} v{3} USB{2} bus_id={0} address={1}>".format(self.bus_id, self.device_address, self.bluetooth_version, self.device_version, self.vendor, self.product)

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """str: Return textual summary of this device."""
        summary = ""

        summary += self.vendor + " - " + self.product + "\n"
        summary += "-" * (len(summary)-1) + "\n"
        summary += "bus_id: {0}\n".format(self.bus_id)
        summary += "device_address: {0}\n".format(self.device_address)
        summary += "device_version: {0}\n".format(self.device_version)
        summary += "bluetooth_version: {0}\n".format(self.bluetooth_version)
        summary += "packets: {0}\n".format(len(self.pcap))

        # Print out string descriptors
        if self.string_descriptors != {}:
            summary += "string descriptors:\n"

            for key in sorted(self.string_descriptors):
                summary += "    {}. {}\n".format(key, self.string_descriptors[key])

        summary += "\nConfigurations\n"
        summary += "--------------\n"

        # Loop through Configurations
        for configuration in self.configurations:
            summary += "\n"
            for line in configuration.summary.split("\n"):
                summary +=  " "*4 + line + "\n"

        return summary.strip()

    @property
    def bNumConfigurations(self) -> int:
        """int: The number of Configurations this Device has."""
        return self.__bNumConfigurations

    @bNumConfigurations.setter
    def bNumConfigurations(self, bNumConfigurations: int) -> None:
        self.__bNumConfigurations = bNumConfigurations

    @property
    def pcap(self):
        """list: The packet capture specific to this USB device."""
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap):
        # Filter the pcap down to only packets relevant for this device.
        self.__pcap = [packet for packet in pcap if 
                int(packet['_source']['layers']['usb']['usb.bus_id']) == self.bus_id and 
                int(packet['_source']['layers']['usb']['usb.device_address']) == self.device_address
                ]

    @property
    def configurations(self):
        """list: Configurations for this USB Device"""
        return self.__configurations

    @configurations.setter
    def configurations(self, configurations):
        self.__configurations = configurations

    @property
    def string_descriptors(self) -> dict:
        """dict: A dictionary of string descriptors registered and returned by the device."""
        return self.__string_descriptors

    @string_descriptors.setter
    def string_descriptors(self, desc: dict) -> None:
        self.__string_descriptors = desc

    @property
    def iSerialNumber(self) -> int:
        """int: The string index for Serial Number."""
        return self.__iSerialNumber

    @iSerialNumber.setter
    def iSerialNumber(self, i: int) -> None:
        self.__iSerialNumber = i

    @property
    def iProduct(self) -> int:
        """int: The string index for product."""
        return self.__iProduct

    @iProduct.setter
    def iProduct(self, i: int) -> None:
        self.__iProduct = i

    @property
    def iManufacturer(self) -> int:
        """int: The string index for manufacturer."""
        return self.__iManufacturer

    @iManufacturer.setter
    def iManufacturer(self, i: int) -> None:
        self.__iManufacturer = i

    @property
    def product(self) -> str:
        """str: The USB Product Name."""
        return self.__product

    @property
    def idProduct(self) -> int:
        """int: The USB Product ID."""
        return self.__idProduct

    @idProduct.setter
    def idProduct(self, idProduct: int) -> None:
        self.__idProduct = idProduct
        self.__product = resolve_product_id(self.idVendor, self.idProduct)

    @property
    def vendor(self) -> str:
        """str: Returns string representation of vendor name."""
        return self.__vendor

    @property
    def idVendor(self) -> int:
        """int: The USB Vendor ID."""
        return self.__idVendor

    @idVendor.setter
    def idVendor(self, idVendor: int) -> None:
        self.__idVendor = idVendor
        self.__vendor = resolve_vendor_id(idVendor)

    @property
    def device_version(self) -> str:
        """str: The device version as a string."""
        return "{0}.{1}.{2}".format(self.device_major, self.device_minor, self.device_subminor)

    @property
    def device_subminor(self) -> int:
        """int: Device specific subminor version"""
        return self.__device_subminor

    @device_subminor.setter
    def device_subminor(self, device_subminor: int) -> None:
        self.__device_subminor = device_subminor

    @property
    def device_minor(self) -> int:
        """int: Device specific minor version."""
        return self.__device_minor

    @device_minor.setter
    def device_minor(self, device_minor: int) -> None:
        self.__device_minor = device_minor

    @property
    def device_major(self) -> int:
        """int: Device specific major version"""
        return self.__device_major

    @device_major.setter
    def device_major(self, device_major: int) -> None:
        self.__device_major = device_major


    @property
    def bluetooth_version(self) -> str:
        """str: The bluetooth version this device complies to as a string."""
        return "{0}.{1}.{2}".format(self.bluetooth_major, self.bluetooth_minor, self.bluetooth_subminor)

    @property
    def bluetooth_subminor(self) -> int:
        """int: The maximum subminor bluetooth version this device conforms to."""
        return self.__bluetooth_subminor

    @bluetooth_subminor.setter
    def bluetooth_subminor(self, bluetooth_subminor: int) -> None:
        self.__bluetooth_subminor = bluetooth_subminor

    @property
    def bluetooth_minor(self) -> int:
        """int: The maximum minor bluetooth version this device conforms to."""
        return self.__bluetooth_minor

    @bluetooth_minor.setter
    def bluetooth_minor(self, bluetooth_minor: int) -> None:
        self.__bluetooth_minor = bluetooth_minor

    @property
    def bluetooth_major(self) -> int:
        """int: The maximum major bluetooth version this device conforms to."""
        return self.__bluetooth_major

    @bluetooth_major.setter
    def bluetooth_major(self, bluetooth_major: int) -> None:
        self.__bluetooth_major = bluetooth_major


    @property
    def bus_id(self) -> int:
        """int: The usb bus id this Device communicates on."""
        return self.__bus_id

    @bus_id.setter
    def bus_id(self, bus_id: int) -> None:
        self.__bus_id = bus_id

    @property
    def device_address(self) -> int:
        """int: The usb device address this Device communicates on."""
        return self.__device_address

    @device_address.setter
    def device_address(self, device_address: int) -> None:
        self.__device_address = device_address

from .helpers import *
from .Configuration import Configuration
