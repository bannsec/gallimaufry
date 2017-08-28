import enforce

@enforce.runtime_validation
class USB:

    def __init__(self, pcap):
        """
        pcap == string path to pcap file.
        """
        self.__prechecks__()

        self.pcap = pcap

    def __prechecks__(self):
        """
        Makes sure things needed are installed.
        """

        if shutil.which("tshark") == None:
            raise Exception("tshark not found. Please install it.")


    # tshark -r ./task.pcap -T json -O usb
    ##############
    # Properties #
    ##############

    @property
    def pcap(self):
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap):
        self.__pcap = os.path.abspath(pcap)

        if not os.path.isfile(self.__pcap):
            raise Exception("PCAP file doesn't exist.")

import os
import shutil
