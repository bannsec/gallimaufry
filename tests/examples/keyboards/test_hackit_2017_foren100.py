#!/usr/bin/env python

import os
from Gallimaufry.USB import USB
from Gallimaufry.Classes.HID import HID

here = os.path.dirname(os.path.realpath(__file__))

pcap_file_name = os.path.join(here,"hackit_2017_foren100.pcap")

def test_hackit_2017_foren100():
    pcap = USB(pcap_file_name)

    assert "Boot Interface Subclass" in pcap.summary

    assert len(pcap.pcap) == 835
    assert len(pcap.devices) == 1
    
    d = pcap.devices[0]

    assert 'aluminum keyboard' in d.product.lower()
    assert 'apple' in d.vendor.lower()
    assert d.device_version == '0.6.9'
    assert d.bluetooth_major == 2
    assert d.bluetooth_minor == 0
    assert d.bus_id == 1
    assert d.device_address == 3

    assert len(d.configurations) == 1

    c = d.configurations[0]

    assert c.bMaxPower == 20
    assert c.bConfigurationValue == 1
    assert c.bNumInterfaces == 2
    assert c.iConfiguration == 0
    assert len(c.interfaces) == 2
    assert c.legacy_10bus_powered == True
    assert c.remote_wakeup == False
    assert c.self_powered == False

    i = next(i for i in c.interfaces if i.bInterfaceNumber == 0)

    assert i.bAlternateSetting == 0
    assert i.bInterfaceClass == 3
    assert i.bInterfaceNumber == 0
    assert i.bInterfaceProtocol == 1
    assert i.bInterfaceSubClass == 1
    assert i.bNumEndpoints == 1
    assert i.class_str == 'HID – Human Interface Device'
    assert len(i.endpoints) == 1
    assert type(i.handler) == HID
    assert i.iInterface == 0
    assert i.protocol_str == 'Keyboard'
    assert i.subclass_str == 'Boot Interface Subclass'

    e = i.endpoints[0]

    assert e.bEndpointAddress == 129
    assert e.bInterval == 10
    assert e.bmAttributes == 3
    assert e.direction == 1
    assert e.direction_str == "In"
    assert e.interface == i
    assert e.number == 1
    assert e.transfer_type == 3
    assert e.transfer_type_str == 'Interrupt'
    assert e.wMaxPacketSize == 8

    keyboard = e.keyboard
   
    assert 'flag{k3yb0ard_sn4ke_2.0}' in keyboard.keystrokes_interpret
