#!/usr/bin/env python

import os
from Gallimaufry.USB import USB

here = os.path.dirname(os.path.realpath(__file__))

def test_device_string_descriptor():
    pcap = USB(os.path.join(here,"examples","webcam","logitech_C310_enum.pcapng"))
    
    device = pcap.devices[0]

    assert device.string_descriptors == {2: '7DC902A0'}
    assert len(device.configurations[0].interfaces[0].uvc) == 8
    assert len(device.configurations[0].interfaces[1].uvc) == 42
