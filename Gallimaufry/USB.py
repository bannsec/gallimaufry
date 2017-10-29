from . import Colorer
import enforce
import typing
from collections import OrderedDict
from .Device import Device

Devices = typing.List[type(Device)]
Packets = typing.List[typing.Dict]
PacketsOut = typing.List[OrderedDict]
TypeIntOptional = typing.Optional[int]

@enforce.runtime_validation
class USB:
    """Base class for defining a USB packet capture.

    Args:
        pcap (str): Path to a pcap file to parse.
    """

    def __init__(self, pcap) -> None:
        self.__prechecks__()

        self.pcap_filename = pcap
        self.devices = []

        self._enumerate_devices()

    def _enumerate_devices(self) -> None:
        """Given the pcap loaded, enumerate and setup what devices are in the capture."""

        # Grab the descriptors
        device_descriptors = (packet for packet in self.pcap if has_device_descriptor(packet))

        # Build out a new device for each
        for device in device_descriptors:
            self.devices.append(Device(device, self.pcap))


    def __find_packets_by_field_name(self, field_name: str, field_value, packets: Packets) -> Packets:
        
        # Not filtering on value
        if field_value == None:
            return [packet for packet in packets if 
                    any(field_name in packet['_source']['layers'][layer] for layer in packet['_source']['layers'])
                    ]

        # Filtering on value
        return [packet for packet in packets if 
                any(field_name in packet['_source']['layers'][layer] and packet['_source']['layers'][layer][field_name] == field_value
                    for layer in packet['_source']['layers'])
                ]

    def _find_packets(self, field_name: str = None, field_value = None) -> Packets:
        """Returns packets that have the given field inside them."""
        # TODO: Maybe just remove this?

        # Setup our initial packets list
        packets = self.pcap

        # Going to add other filtering options later
        if field_name:
            packets = self.__find_packets_by_field_name(field_name, field_value, packets)

        return packets

    def __prechecks__(self):
        """
        Makes sure things needed are installed.
        """

        if shutil.which("tshark") == None:
            raise Exception("tshark not found. Please install it.")

    def __parse_pcap(self) -> bool:
        """Loads up the pcap for this object.
        
        Returns True on successful load, False otherwise"""

        def preprocess(pcap: str) -> str:
            # Work around the tshark issue where the json fields are not unique...
            # For now, just give them each a unique int. Because who cares.
            bad_words = ["HID DESCRIPTOR","ENDPOINT DESCRIPTOR"]
            pcap2 = []
            i = 0
            for line in pcap.split("\n"):
                for bad_word in bad_words:
                    if bad_word in line:
                        line = line.replace(bad_word, "{0} {1}".format(bad_word, i))
                        i += 1
                pcap2.append(line)
            return '\n'.join(pcap2)

        self.__pcap = json.loads(preprocess(subprocess.check_output(["tshark","-r",self.pcap_filename,"-T","json","-O","usb"]).decode('cp1252')),object_pairs_hook=OrderedDict)

        return True

    def pcap_filter(self, bus_id: TypeIntOptional = None, device_address: TypeIntOptional = None, endpoint_number: TypeIntOptional = None) -> PacketsOut:
        """Return only those packets that match ALL of the input selection.
        
        Args:
            bus_id: The bus id to select
            device_address: The device address to select
            endpoint_number: The endpoint number to select

        Returns:
            list: A list of OrderedDict packets matching the filter criteria.

        Example:
            If you wanted to select only those packets with a bus_id of 1,
            device_address of 0 and endpoint_number of 1, you could do the
            following::

                >> from Gallimaufry.USB import USB
                >> pcap = USB("pcap.pcap")
                >> filt = pcap.pcap_filter(bus_id=1,device_address=0,endpoint_number=1)
        """

        pcap = self.pcap

        if bus_id is not None:
            pcap = [packet for packet in pcap if int(packet['_source']['layers']['usb']['usb.bus_id'],10) == bus_id]

        if device_address is not None:
            pcap = [packet for packet in pcap if int(packet['_source']['layers']['usb']['usb.device_address'],10) == device_address]

        if endpoint_number is not None:
            # Remember, the endpoint number is the lower 3 bits of the actual endpoint_number field
            pcap = [packet for packet in pcap if int(packet['_source']['layers']['usb']['usb.endpoint_number'],16) & 0b111 == endpoint_number]

        return pcap

    def __repr__(self) -> str:
        return "<USB packets={0}>".format(len(self.pcap))

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """str: a textual summary of this pcap."""
        summary = "PCAP: {0}\n".format(self.pcap_filename)
        summary += "Total Packets: {0}\n\n".format(len(self.pcap))

        summary += "Devices\n"
        summary += "-------\n"

        for device in self.devices:
            summary += "\n"
            for line in device.summary.split("\n"):
                summary +=  " "*4 + line + "\n"

        return summary.strip()

    @property
    def pcap(self) -> list:
        """list: list of dictionaries describing the packets of this pcap."""
        return self.__pcap


    @property
    def pcap_filename(self) -> str:
        """str: full path to pcap file."""
        return self.__pcap_filename

    @pcap_filename.setter
    def pcap_filename(self, pcap: str) -> None:
        self.__pcap_filename = os.path.abspath(pcap)

        if not os.path.isfile(self.__pcap_filename):
            raise Exception("PCAP file doesn't exist.")

        # Load it up!
        self.__parse_pcap()

    @property
    def devices(self) -> Devices:
        """list: The USB devices discovered (USB.Device.Device)."""
        return self.__devices

    @devices.setter
    def devices(self, devices: Devices) -> None:
        self.__devices = devices

import os
import shutil
import subprocess
import json
from .helpers import *
