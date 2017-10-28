#!/usr/bin/env python

import os
from Gallimaufry.USB import USB
from Gallimaufry.Classes.HID.Keyboard import Keyboard

here = os.path.dirname(os.path.realpath(__file__))

pcap_file_name = os.path.join(here,"pico_2017_Just_Keyp_Trying.pcap")

def test_pico_2017_Just_Keyp_Trying():
    pcap = USB(pcap_file_name)

    assert len(pcap.pcap) == 66
    assert len(pcap.devices) == 0
    
    keyboard = Keyboard(pcap.pcap)

    assert keyboard.keystrokes.startswith('flag{pr355_0nwards_c98ccf99}')
