#!/usr/bin/env python

import os
from Gallimaufry.USB import USB

here = os.path.dirname(os.path.realpath(__file__))

def test_device_string_descriptor():
    pcap = USB(os.path.join(here,"examples","general","device_string_descriptor.pcap"))

    device = pcap.devices[0]

    assert device.string_descriptors == {1: 'XHC MACH3 CARD'}
