#####################
HackIT 2017: Foren100
#####################

********
Overview
********
For the Foren100 challenge we are given a file named `task.pcap`. The first
thing to do is open it in something like ``Wireshark``. A quick peek with
``Wireshark`` shows that they have captured USB packets. Our goal will likely
be to extract the flag from the data being transferred.

****************
Step 0: Analysis
****************
At this point, we're not quite sure what data is being passed around in these
USB packets. Based on the nature of the protocol, it could be many things, and
the method of transferring that information does not often allow you to simply
run ``strings`` to discover what it is. Let's open it up with ``usb_pcap``::

    In [1]: from Gallimaufry import USB

    In [2]: pcap = USB("./task.pcap")

    In [3]: pcap
    Out[3]: <USB packets=835>

Now that we've loaded up the pcap, we should take a look at what's inside it.
With smaller pcap files, the easiest way is probably to use the ``summary``
property::

    In [4]: print(pcap.summary)
    PCAP: /home/user/opt/usb_pcap/examples/keyboard/HackIT2017/task.pcap
    Total Packets: 835

    Devices
    -------

        Apple, Inc. - Aluminum Keyboard (ISO)
        -------------------------------------
        bus_id: 1
        device_address: 3
        device_version: 0.6.9
        bluetooth_version: 2.0.0
        packets: 514

        Configurations
        --------------

            Configuration 1
            ---------------
            bNumInterfaces = 2
            self_powered = False
            remote_wakeup = False

            Interfaces
            -----------

                Interface 0
                -----------
                Class: HID – Human Interface Device
                SubClass: Boot Interface Subclass
                Protocol: Keyboard

                Endpoints
                ---------

                    Endpoint 1
                    ----------
                    direction: In
                    transfer_type: Interrupt
                    packets: 478

                Interface 1
                -----------
                Class: HID – Human Interface Device
                SubClass: No Subclass
                Protocol: None

                Endpoints
                ---------

                    Endpoint 2
                    ----------
                    direction: In
                    transfer_type: Interrupt
                    packets: 0

This is a very clean usb pcap. There's only one Device, with one Configuration,
and two interfaces. Of those interfaces, only one interface and one endpoint
have data. It's a fair bet that we should look at what's in that data.

******************************
Step 1: Extract the Keystrokes
******************************
Here we can drill down into the object to extract the keystrokes. Let's take a
look at the devices::

	In [6]: pcap.devices
	Out[6]: [<Apple, Inc. Aluminum Keyboard (ISO) v0.6.9 USB2.0.0 bus_id=1 address=3>]

Drill down next into the configurations::

	In [7]: pcap.devices[0].configurations
	Out[7]: [<Configuration bNumInterfaces=2 bConfigurationValue=1>]

There's only one. Let's look at the Interfaces::

	In [8]: pcap.devices[0].configurations[0].interfaces
	Out[8]:
	[<Interface HID – Human Interface Device bInterfaceNumber=0>,
	 <Interface HID – Human Interface Device bInterfaceNumber=1>]

From the summary, we know we want Interface 0. Finally, checkout the endpoints::

	In [9]: pcap.devices[0].configurations[0].interfaces[0].endpoints
	Out[9]: [<Endpoint number=1 direction=In transfer_type=Interrupt packets=478>]

There's only one of them. At this point, we have an Endpoint object. The
library has identified that this endpoint is a keyboard, and has added a
``Keyboard`` object to it. Let's pull that out.::

	In [10]: keyboard = pcap.devices[0].configurations[0].interfaces[0].endpoints[0].keyboard

	In [11]: keyboard
	Out[11]: <Keyboard keystrokes=208>


Notice that the ``Keyboard`` object has identified 208 keystrokes for this
endpoint. Let's extract them::

	In [12]: print(keyboard.keystrokes)
	w
	k
	f
	b
	3'[Up Arrow][[Up Arrow]l[Up Arrow]#[Up Arrow]{w$[Down Arrow]>b[Down Arrow]ag[Down Arrow][e[Down Arrow]ci.[[Up Arrow][f[Up Arrow]{k[Up Arrow]n$[Up Arrow]ju}[Down Arrow]:[Down Arrow]3[Down Arrow]u[Down Arrow]%=[Up Arrow]~[Up Arrow]y[Up Arrow]6[Up Arrow],'[Down Arrow]p[Down Arrow]b[Down Arrow]7[Down Arrow]%&[Up Arrow]d[Up Arrow]0[Up Arrow]j[Up Arrow]pt[Down Arrow]i[Down Arrow]a[Down Arrow][[Down Arrow]k([Up Arrow]=[Up Arrow]r[Up Arrow]m[Up Arrow]]=[Down Arrow]0[Down Arrow]d[Down Arrow]>[Down Arrow]lc[Up Arrow]*[Up Arrow]_[Up Arrow]{[Up Arrow]j%[Down Arrow]u[Down Arrow]s[Down Arrow]([Down Arrow]*2[Up Arrow]0[Up Arrow]n[Up Arrow]'[Up Arrow];9[Down Arrow]h[Down Arrow]4[Down Arrow]][Down Arrow]y4[Up Arrow]'[Up Arrow]k[Up Arrow];[Up Arrow]+p[Down Arrow]f[Down Arrow]e[Down Arrow]$[Down Arrow]!}[Up Arrow]1[Up Arrow]_[Up Arrow]k[Up Arrow]s&[Down Arrow]s[Down Arrow]2[Down Arrow]c[Down Arrow]%q[Up Arrow]$[Up Arrow].[Up Arrow]![Up Arrow]#,[Down Arrow]s[Down Arrow]0[Down Arrow]c[Down Arrow]z3[Up Arrow]e[Up Arrow]}[Up Arrow]-[Up Arrow]i

At this point you may notice there are a bunch of ``[Up Arrow]`` and
``[Down Arrow]`` in the output. This is ``usp_pcap``'s way of telling you that
arrow characters were pushed. Thus, simply printing out the output like this,
while a good start, won't get us all the way. ``usb_pcap`` has the ability to
attempt to interpret keystrokes in different settings. As of writing, the only
setting it is interpreting is a notepad like setting. The goal for this setting
is to interpret characters (such as the arrows) and maintain state of a cursor
object, thus allowing it to correctly reproduce what was being typed.

To utilize this, use the ``keystrokes_interpret`` property, like so::

    In [13]: print(keyboard.keystrokes_interpret)
    w{w$ju},'pt]=j%;9+ps&#,i
    k#>bn$:6pjim0{u'h;fks!s-
    flag{k3yb0ard_sn4ke_2.0}
    b[[e[fu~7d[=>*(0]'$1c$ce
    3'ci.[%=%&k(lc*2y4!}%qz3

We can see that the flag is in the middle of the other random looking keys.

Flag: ``flag{k3yb0ard_sn4ke_2.0}``

*********
Resources
*********
* `task.pcap <https://github.com/Owlz/usb_pcap/blob/master/docs/source/examples/hackit_2017_foren100.pcap?raw=true>`_
