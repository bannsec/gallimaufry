import Colorer
import enforce
import typing
from .Device import Device

Devices = typing.List[type(Device)]
Packets = typing.List[typing.Dict]

@enforce.runtime_validation
class USB:

    def __init__(self, pcap) -> None:
        """
        pcap == string path to pcap file.
        """
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

    def __repr__(self) -> str:
        return "<USB packets={0}>".format(len(self.pcap))

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """Returns a textual summary of this pcap."""
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
    def pcap(self) -> str:
        """Returns the json dump of this pcap."""
        return self.__pcap

    @property
    def pcap_filename(self) -> str:
        """Path to pcap file."""
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
        """The USB devices discovered."""
        return self.__devices

    @devices.setter
    def devices(self, devices: Devices) -> None:
        self.__devices = devices

import os
import shutil
import subprocess
import json
from collections import OrderedDict
from .helpers import *
