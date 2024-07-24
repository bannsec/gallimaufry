import logging
logger = logging.getLogger("USB.Classes.DualShock4")

from ..helpers import Bits
import matplotlib.pyplot as plt

# Based on: https://www.psdevwiki.com/ps4/DS4-USB

class DualShock4:

    def __init__(self, pcap):
        """DualShock PS4 controller parsing.

        pcap == packet capture from tshark with ONLY those packets for a specific endpoint.
        """
        self.pcap = pcap
        self.actions = []
        self._parse_pcap()

    def _parse_pcap(self):

        for packet in self.pcap:
            # Not interrupt packet
            if 'usb.capdata' not in packet['_source']['layers']:
                continue

            cap_data = packet['_source']['layers']['usb.capdata'].split(":")

            if len(cap_data) != 64:
                logging.warn('Expecting capdata length of 64, got {} instead'.format(len(cap_data)))

            action = DualShock4Action()
            action.report_id = int(cap_data[0],16)
            action.l_x_axis = int(cap_data[1],16) # 0 == left
            action.l_y_axis = int(cap_data[2],16) # 0 == up
            action.r_x_axis = int(cap_data[3],16) # 0 == left
            action.r_y_axis = int(cap_data[4],16) # 0 == up

            buttons = Bits(int(cap_data[5],16), 8) # Bits of size 8
            action.button_triangle = buttons[7]
            action.button_circle = buttons[6]
            action.button_x = buttons[5]
            action.button_square = buttons[4]
            action.dpad = buttons[0:3]

            buttons = Bits(int(cap_data[6],16), 8) # Bits of size 8
            action.button_r3 = buttons[7]
            action.button_l3 = buttons[6]
            action.button_options = buttons[5]
            action.button_share = buttons[4]
            action.button_r2 = buttons[3]
            action.button_l2 = buttons[2]
            action.button_r1 = buttons[1]
            action.button_l1 = buttons[0]

            counter = Bits(int(cap_data[7],16), 8) # Bits of size 8
            action.counter = counter[2:7]
            action.button_tpad_click = counter[1]
            action.button_ps = counter[0]

            action.l2_pressure = int(cap_data[8], 16) # 0 released, 0xff full pressure
            action.r2_pressure = int(cap_data[9], 16)

            action.battery = int(cap_data[12], 16)

            self.actions.append(action)

    def __repr__(self) -> str:
        return "<DualShock4 actions={0}>".format(len(self.actions))

    def save_movement_plot(self, fname):
        """Attempt to render left and right stick movement on a plot."""

        x = [0]
        y = [0]

        for action in self.actions:
            x.append( x[-1] + action.r_x_normalized )
            y.append( y[-1] + action.r_y_normalized )

        plt.plot(x, y, '-')

        x = [0]
        y = [0]

        for action in self.actions:
            x.append( x[-1] + action.l_x_normalized )
            y.append( y[-1] + action.l_y_normalized )

        plt.plot(x, y, '.')

        plt.savefig(fname)
        

    @property
    def pcap(self):
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap) -> None:
        self.__pcap = pcap

class DualShock4Action(object):
    __slots__ = 'report_id', 'l_x_axis', 'l_y_axis', 'r_x_axis', \
                'r_y_axis', 'button_triangle', 'button_circle', \
                'button_x', 'button_square', 'dpad', 'button_r3', \
                'button_l3', 'button_options', 'button_share', \
                'button_r2', 'button_l2', 'button_r1', 'button_l1', \
                'counter', 'button_tpad_click', 'button_ps', \
                'l2_pressure', 'r2_pressure', 'battery'

    def __repr__(self):
        info = ['DS4Action']

        buttons = []

        for button in [x for x in self.__slots__ if x.startswith('button')]:
            if getattr(self, button):
                buttons.append(button[7:])

        if buttons != []:
            info.append('buttons={buttons}'.format(
                buttons=','.join(buttons),
                ))

        # 0x08 is released dpad
        if self.dpad_utf8 != '':
            info.append('DPAD=' + self.dpad_utf8)

        return '<{info}>'.format(info=' '.join(info))

    @property
    def dpad_utf8(self):
        lookup = {
            8: '',
            7: '↑←',
            6: '←',
            5: '↓←',
            4: '↓',
            3: '↓→',
            2: '→',
            1: '↑→',
            0: '↑'
        }

        return lookup[self.dpad]

    @property
    def l_x_normalized(self):
        """Normalize the x direction for the left stick. Negative is moving left, positive is moving right."""
        return (self.l_x_axis - 128) / 127

    @property
    def l_y_normalized(self):
        """Normalize the y direction for the left stick. Negative is moving down, positive is moving up."""
        return (128 - self.l_y_axis) / 127

    @property
    def r_x_normalized(self):
        """Normalize the x direction for the right stick. Negative is moving left, positive is moving right."""
        return (self.r_x_axis - 128) / 127

    @property
    def r_y_normalized(self):
        """Normalize the y direction for the right stick. Negative is moving down, positive is moving up."""
        return (128 - self.r_y_axis) / 127
