#!/usr/bin/env python3

import os
from USB import USB
from USB.Classes.HID.Keyboard import Keyboard

here = os.path.dirname(os.path.abspath(__file__))

usb = USB(os.path.join(here,"data.pcap"))

# For this, since we don't have a full capture, we're just going to tell the parser that this is a Keyboard.

k = Keyboard(usb.pcap)

print(k.keystrokes)
