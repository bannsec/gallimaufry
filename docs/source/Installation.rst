Installation
############
Installation is fairly strait forward. You can install it manually, or use a
pre-build Docker image.

***********
Manual/pypi
***********
Manual installation simply involves ensuring that you have ``tshark`` installed
and then installing the ``usb_pcap`` package. You can do that as follows:

.. code-block:: bash

    $ # Install tshark
    $ sudo apt-get update && sudo apt-get install -y tshark python3
    $ # Optionally, create a virtual environment
    $ mkvirtualenv --python=$(which python3) -i usb_pcap usb_pcap

******
Docker
******
There is an automated Docker build for this project that will take care of
ensuring everything that needs to be installed is.

To download the latest version, do the following:

.. code-block:: bash

    $ sudo docker pull bannsec/usb_pcap

You can run the container as follows:

.. code-block:: bash

    $ sudo docker run -it --rm -v $PWD:/pcaps bannsec/usb_pcap

That will drop you into a shell where you can run the tool. It will also mount
your current directory inside the container under ``/pcaps``.
