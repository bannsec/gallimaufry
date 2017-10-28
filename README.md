[![Documentation Status](https://readthedocs.org/projects/gallimaufry/badge/?version=latest)](http://gallimaufry.readthedocs.org/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/bannsec/gallimaufry.svg?branch=master)](https://travis-ci.org/bannsec/gallimaufry)

# Overview
`Gallimaufry` is a python framework for parsing and working with packet capture files (PCAPs) of USB traffic. It utilizes `tshark` in the backend to perform the initial translation of the packet capture into python. The goal of this framework is to make it easy to parse out information from USB pcaps as well as easy to extend the framework for more USB traffic types.

For a quick understanding of how it works, check out the [examples](http://gallimaufry.readthedocs.io/en/latest/index.html) in the documentation.

# Docs
http://gallimaufry.readthedocs.io/en/latest/index.html

# Quick Start
Once installed, you can load up a pcap and analyze it:

```python
In [1]: from Gallimaufry.USB import USB

In [2]: usb = USB("./task.pcap")

In [3]: usb
Out[3]: <USB packets=835>

In [4]: usb.devices
Out[4]: [<Apple, Inc. Aluminum Keyboard (ISO) v0.6.9 USB2.0.0 bus_id=1 address=3>]
```

# Requires
 - python 3.5+
 - tshark

# Install

## Pip
Install using pip:

```bash
$ pip install .
```

## Docker
There is an auto-build Docker container that has everything set up already. Download it with the following:

```bash
$ sudo docker pull bannsec/Gallimaufry
```

Run it:

```bash
$ sudo docker run -it --rm -v $PWD:/my_mount bannsec/Gallimaufry
```

