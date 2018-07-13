import logging
logger = logging.getLogger("USB.Classes.HID.Mouse")

import enforce

#@enforce.runtime_validation
class Mouse:

    def __init__(self, pcap):
        """Basic Mouse parsing class.

        pcap == packet capture from tshark with ONLY those packets for a specific endpoint.
        """
        self.pcap = pcap
        self.actions_list = []

        self._parse_pcap()

    def _parse_pcap(self):

        for packet in self.pcap:
            # Not interrupt packet
            if 'usb.capdata' not in packet['_source']['layers']:
                continue

            cap_data = packet['_source']['layers']['usb.capdata']
            button, x, y, wheel = [int(field,16) for field in cap_data.split(":")]
            
            if x > 127:
                x = x - 256
            if y > 127:
                y = y - 256
            if wheel > 127:
                wheel = wheel - 256

            action = {
                'x': x,
                'y': y,
                'wheel': wheel,
                'button': button
                }

            self.actions_list.append(action)

    def __repr__(self) -> str:
        return "<Mouse actions={0}>".format(len(self.actions_list))


    @property
    def actions(self) -> str:
        """Returns the actions captured as a string."""
        return ''.join("X={:d} Y={:d} W={:d}] B={:d}\n".format(action['x'], action['y'], action['wheel'], action['button']) for action in self.actions_list)

    @property
    def actions_list(self) -> list:
        """Returns the actions captured as a list."""
        return self.__actions_list

    @actions_list.setter
    def actions_list(self, actions_list: list) -> None:
        self.__actions_list = actions_list

    @property
    def pcap(self):
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap) -> None:
        self.__pcap = pcap

