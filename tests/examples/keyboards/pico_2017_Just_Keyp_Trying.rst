###########################
Pico 2017: Just Keyp Trying
###########################

********
Overview
********
As with the previous examples, we are given a pcap that, upon opening, we
discover contains USB packets. This example will go over a trick that may be
necessary when you do not have all the packets. Specifically, it discusses how
to handle the case when we do not have all the descriptors present but still
want to parse out the keystrokes.

****************
Step 0: Analysis
****************
To start with, let's open the pcap with ``gallimaufry``::

    In [1]: from Gallimaufry.USB import USB

    In [2]: pcap = USB("./data.pcap")

    In [3]: pcap
    Out[3]: <USB packets=66>

This example is a very clean pcap. Only 66 packets! Let's see what packets
we've found by looking at the ``summary``::

    In [5]: print(pcap.summary)
    PCAP:
    data.pcap
    Total Packets: 66

    Devices
    -------

Here is where you find the gotcha. The summary returned nothing! The reason for
this is that, upon inspection of the pcap, the USB descriptor payloads are not
present. Due to this, ``gallimaufry`` does not know the types of objects to
create.

If you wanted to inspect the packets parsed through ``gallimaufry`` manually,
you can use the ``pcap`` property::

    In [6]: pcap.pcap
    OrderedDict([('_index', 'packets-2017-10-25'),
                  ('_type', 'pcap_file'),
                  ('_score', None),
                  ('_source',
                   OrderedDict([('layers',
                                 OrderedDict([('frame',
                                               OrderedDict([('frame.encap_type',
                                                             '152'),
                                                            ('frame.time',
                                                             'Mar 22, 2017 21:07:40.230170000 EDT'),
                                                            ('frame.offset_shift',
                                                             '0.000000000'),
                                                            ('frame.time_epoch',
                                                             '1490231260.230170000'),
                                                            ('frame.time_delta',
                                                             '3.716062000'),
                                                            ('frame.time_delta_displayed',
                                                             '3.716062000'),
                                                            ('frame.time_relative',
                                                             '23.453109000'),
                                                            ('frame.number', '65'),
                                                            ('frame.len', '35'),
                                                            ('frame.cap_len',
                                                             '35'),
                                                            ('frame.marked', '0'),
                                                            ('frame.ignored', '0'),
                                                            ('frame.protocols',
                                                             'usb')])),
                                              ('usb',
                                               OrderedDict([('usb.src', '2.1.1'),
                                                            ('usb.addr', 'host'),
                                                            ('usb.dst', 'host'),
                                                            ('usb.usbpcap_header_len',
                                                             '27'),
                                                            ('usb.irp_id',
                                                             '0xffffb689ac2d3940'),
                                                            ('usb.usbd_status',
                                                             '0'),
                                                            ('usb.function', '9'),
                                                            ('usb.irp_info',
                                                             '0x00000001'),
                                                            ('usb.irp_info_tree',
                                                             OrderedDict([('usb.irp_info.reserved',
                                                                           '0x00000000'),
                                                                          ('usb.irp_info.direction',
                                                                           '0x00000001')])),
                                                            ('usb.bus_id', '2'),
                                                            ('usb.device_address',
                                                             '1'),
                                                        ('usb.endpoint_number',
                                                         '0x00000081'),
                                                        ('usb.endpoint_number_tree',
                                                         OrderedDict([('usb.endpoint_number.direction',
                                                                       '1'),
                                                                      ('usb.endpoint_number.endpoint',
                                                                       '1')])),
                                                        ('usb.transfer_type',
                                                         '0x00000001'),
                                                        ('usb.data_len', '8'),
                                                        ('usb.bInterfaceClass',
                                                         '65535')])),
                                          ('usb.capdata',
                                           '01:00:00:00:00:00:00:00')]))]))]),
                                           <<clipped>>


Future work on this tool will include endpoint summaries that are agnostic of
Devices, but until that time you will have to do a bit of manual work to pull
out the packets you're interested in.

******************************
Step 1: Extract the Keystrokes
******************************
Since we were not able to auto-parse this pcap, we will need to first extract
the relevant packets. To do this, let's pull out all packets with the USB
endpoint number of 0x81::

    In [7]: packets = [packet for packet in pcap.pcap if int(packet['_source']['layers']['usb']['usb.endpoint_number'],16) == 0x81]

    In [8]: len(packets)
    Out [8]: 66

Note here that the number of packets we extracted is the same as the total
number of packets this capture has. The authors of this challenge were trying
to be nice to us by removing unnecessary payloads before giving it to us.

At this point, we would like to parse out the keystrokes. However, the
``Keyboard`` object wasn't automatically generated for us. Since we have the
packets we want, let's manually generate a ``Keyboard`` object with these
packets::

    In [9]: from Gallimaufry.Classes.HID.Keyboard import Keyboard

    In [10]: keyboard = Keyboard(packets)

    In [11]: keyboard
    Out [11]: <Keyboard keystrokes=29>

Our ``Keyboard`` object has been created, and it successfully parsed out 29
keystrokes from the packets it received. We can now ask it to print out those
keystrokes as we have done previously::

    In [12]: keyboard.keystrokes
    Out [12]: 'flag{pr355_0nwards_c98ccf99}[LEFT_CONTROL]c'

Funny enough, we also caught the authors executing a Ctrl-C using the Left
Control button.

*********
Resources
*********
* `data.pcap <https://github.com/bannsec/gallimaufry/blob/master/docs/source/examples/pico_2017_Just_Keyp_Trying.pcap?raw=true>`_
