Overview
=============
``usb_pcap`` is a python3 wrapper for parsing USB packet capture (or .pcap)
files. It utilizes ``tshark`` on the backend for parsing of the packet capture
files. The output of parsing the pcap file is a python class object that
represents everything it knows about what's in the pcap.

Structure
=========
The pcap object will basically mimic the underlying USB protocol. This means,
in general, you will have the following class hierarchy:

USB -> Devices -> Configurations -> Interfaces -> Endpoints

For more information about the structure of USB descriptors, there's a very
nice writeup at `beyondlogic <http://www.beyondlogic.org/usbnutshell/usb5.shtml>`_.

Caveats
=======
Auto parsing for ``usb_pcap`` currently relies on parsing information from what
are called Descriptors. Descriptors are the way that the USB protocol tells the
host what is connected and what to expect. The packet capture may not have all
the descriptors. If it does not, those objects will not be automatically
generated. However, you can manually parse them (as in the PicoCTF example) if
you provide a bit more information.
