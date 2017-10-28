#!/usr/bin/env python

import os
from Gallimaufry.USB import USB

here = os.path.dirname(os.path.realpath(__file__))

pcap_file_name = os.path.join(here,"csaw_2012_net300.pcap")

def test_csaw_2012_net300():
    pcap = USB(pcap_file_name)

    assert len(pcap.pcap) == 2844
    assert len(pcap.devices) == 2
    assert 'teensyduino' in pcap.devices[0].product.lower()
    assert pcap.devices[0].bluetooth_major == 2
    assert pcap.devices[0].bluetooth_minor == 0
    assert set(d.bus_id for d in pcap.devices) == set([2])
    assert set(d.device_address for d in pcap.devices) == set([0,26])

    d = next(d for d in pcap.devices if d.device_address == 26)
    c = d.configurations[0]
    i = next(i for i in c.interfaces if i.bInterfaceNumber == 0)
    e = i.endpoints[0]
    keyboard = e.keyboard
    
    assert keyboard.keystrokes == '[RIGHT_GUI]rxterm -geometry 12x1+0+0\necho k\n[RIGHT_GUI]rxterm -geometry 12x1+75+0\necho e\n[RIGHT_GUI]rxterm -geometry 12x1+150+0\necho y\n[RIGHT_GUI]rxterm -geometry 12x1+225+0\necho {\n[RIGHT_GUI]rxterm -geometry 12x1+300+0\necho c\n[RIGHT_GUI]rxterm -geometry 12x1+375+0\necho 4\n[RIGHT_GUI]rxterm -geometry 12x1+450+0\necho 8\n[RIGHT_GUI]rxterm -geometry 12x1+525+0\necho b\n[RIGHT_GUI]rxterm -geometry 12x1+600+0\necho a\n[RIGHT_GUI]rxterm -geometry 12x1+675+0\necho 9\n[RIGHT_GUI]rxterm -geometry 12x1+0+40\necho 9\n[RIGHT_GUI]rxterm -geometry 12x1+75+40\necho 3\n[RIGHT_GUI]rxterm -geometry 12x1+150+40\necho d\n[RIGHT_GUI]rxterm -geometry 12x1+225+40\necho 3\n[RIGHT_GUI]rxterm -geometry 12x1+300+40\necho 5\n[RIGHT_GUI]rxterm -geometry 12x1+450+40\necho c\n[RIGHT_GUI]rxterm -geometry 12x1+375+40\necho 3\n[RIGHT_GUI]rxterm -geometry 12x1+525+40\necho a\n[RIGHT_GUI]rxterm -geometry 12x1+600+40\necho }\n'
