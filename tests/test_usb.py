#!/usr/bin/env python

import os
from Gallimaufry.USB import USB

here = os.path.dirname(os.path.realpath(__file__))

def test_pcap_filter():
    pcap = USB(os.path.join(here,"examples","keyboards","csaw_2012_net300.pcap"))

    for device in pcap.devices:
        assert len(device.pcap) == len(pcap.pcap_filter(bus_id=device.bus_id, device_address=device.device_address))

    pcap = USB(os.path.join(here,"examples","keyboards","pico_2017_Just_Keyp_Trying.pcap"))

    assert len(pcap.pcap) == len(pcap.pcap_filter(bus_id=2, device_address=1, endpoint_number=1))
