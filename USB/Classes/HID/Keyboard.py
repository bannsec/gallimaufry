import logging
logger = logging.getLogger("USB.Classes.HID.Keyboard")

import enforce

#@enforce.runtime_validation
# Static method issue: https://github.com/RussBaz/enforce/issues/55
class Keyboard:

    def __init__(self, pcap):
        """Basic USB Keyboard parsing class.

        pcap == packet capture from tshark with ONLY those packets for a specific endpoint.
        """
        self.pcap = pcap
        self.keystrokes_list = []

        self._parse_pcap()

    def _parse_pcap(self):
        # TODO: Handle parsing non-interrupt based?

        for packet in self.pcap:
            # Not interrupt packet
            if 'usb.capdata' not in packet['_source']['layers']:
                continue

            cap_data = packet['_source']['layers']['usb.capdata']
            modifier, _, key1, key2, key3, key4, key5, key6 = [int(field,16) for field in cap_data.split(":")]
            
            modifier = Keyboard._parse_modifier(modifier)

            stroke = ""

            # Usually only one key is pressed at a time... but more than one is allowed
            for key in (key1, key2, key3, key4, key5, key6):
                # 0 means no key pressed
                if key != 0:
    
                    # Shift
                    if modifier['LEFT_SHIFT'] or modifier['RIGHT_SHIFT']:
                        key = key_codes[key][1]
                    else:
                        key = key_codes[key][0]

                    # Other mods
                    for k, v in modifier.items():
                        if k not in ["LEFT_SHIFT", "RIGHT_SHIFT"] and v == True:
                            key = "[{0}]".format(k) + key

                    stroke += key

            # If this was not a clear command
            if stroke != "":
                self.keystrokes_list.append(stroke)



    @staticmethod
    def _parse_modifier(modifier):
        """Given an integer modifer value, return what flags are set."""
        
        return {
                'LEFT_CONTROL'  : (modifier >> 0) & 0b1 == 1,
                'LEFT_SHIFT'    : (modifier >> 1) & 0b1 == 1,
                'LEFT_ALT'      : (modifier >> 2) & 0b1 == 1,
                'LEFT_GUI'      : (modifier >> 3) & 0b1 == 1,
                'RIGHT_CONTROL' : (modifier >> 4) & 0b1 == 1,
                'RIGHT_SHIFT'   : (modifier >> 5) & 0b1 == 1,
                'RIGHT_ALT'     : (modifier >> 6) & 0b1 == 1,
                'RIGHT_GUI'     : (modifier >> 7) & 0b1 == 1,
                }

    def __repr__(self) -> str:
        return "<Keyboard keystrokes={0}>".format(len(self.keystrokes_list))

    ##############
    # Properties #
    ##############

    @property
    def keystrokes_interpret(self) -> str:
        """Attempt to interpret keystrokes as typing in a document. This means interpret up/down/right/left arrows and stuff."""
        page = [[]]
        row = 0
        col = 0

        for key in self.keystrokes_list:

            # Ignoring this for now
            if key == "\r":
                continue

            if key == "[Up Arrow]":
                row = row - 1

                # Normalize
                if row < 0:
                    row = 0
                continue

            elif key == "[Down Arrow]":
                row = row + 1

                if row >= len(page):
                    row = len(page) - 1

                continue 

            elif key == "[Right Arrow]":
                col = col + 1

                if col >= len(page[row]):
                    col = len(page[row]) - 1

                continue

            elif key == "[Left Arrow]":
                col = col - 1
            
                if col < 0:
                    col = 0

                continue

            # Enter
            if key == "\n":
                row += 1
                col = 0
                page.insert(row, [])
                continue

            # Chars will take up one position
            col += 1

            page[row].insert(col, key)

        return "\n".join("".join(row) for row in page)

    @property
    def keystrokes(self) -> str:
        """Returns the keystrokes captured as a string."""
        return ''.join(self.keystrokes_list)

    @property
    def keystrokes_list(self) -> list:
        """Returns the keystrokes captured as a list."""
        return self.__keystrokes_list

    @keystrokes_list.setter
    def keystrokes_list(self, keystrokes_list: list) -> None:
        self.__keystrokes_list = keystrokes_list

    @property
    def pcap(self):
        return self.__pcap

    @pcap.setter
    def pcap(self, pcap) -> None:
        self.__pcap = pcap

# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf -- page 53
# Value: [normal, with-shift]
key_codes = {
        0x1:  ['[Keyboard ErrorRollOver]','[Keyboard ErrorRollOver]'],
        0x2:  ['[Keyboard POSTFail]','[Keyboard POSTFail]'],
        0x3:  ['[Keyboard ErrorUndefined]','[Keyboard ErrorUndefined]'],
        0x4:  ['a','A'],
        0x5:  ['b','B'],
        0x6:  ['c','C'],
        0x7:  ['d','D'],
        0x8:  ['e','E'],
        0x9:  ['f','F'],
        0xa:  ['g','G'],
        0xb:  ['h','H'],
        0xc:  ['i','I'],
        0xd:  ['j','J'],
        0xe:  ['k','K'],
        0xf:  ['l','L'],
        0x10: ['m','M'],
        0x11: ['n','N'],
        0x12: ['o','O'],
        0x13: ['p','P'],
        0x14: ['q','Q'],
        0x15: ['r','R'],
        0x16: ['s','S'],
        0x17: ['t','T'],
        0x18: ['u','U'],
        0x19: ['v','V'],
        0x1a: ['w','W'],
        0x1b: ['x','X'],
        0x1c: ['y','Y'],
        0x1d: ['z','Z'],
        0x1e: ['1','!'],
        0x1f: ['2','@'],
        0x20: ['3','#'],
        0x21: ['4','$'],
        0x22: ['5','%'],
        0x23: ['6','^'],
        0x24: ['7','&'],
        0x25: ['8','*'],
        0x26: ['9','('],
        0x27: ['0',')'],
        0x28: ['\n','\n'], # TODO: Maybe not interpret Enter?
        0x29: ['\x1b','\x1b'], # TODO: Maybe not interpret Escape?
        0x2a: ['[DELETE]','[DELETE]'],
        0x2b: ['\t','\t'],
        0x2c: [' ',' '],
        0x2d: ['-','_'],
        0x2e: ['=','+'],
        0x2f: ['[','{'],
        0x30: [']','}'],
        0x31: ['\\','|'],
        0x32: ['#', '~'],
        0x33: [';',':'],
        0x34: ['\'','"'],
        0x35: ['[Grave Accent]','[Tilde]'],
        0x36: [',','<'],
        0x37: ['.','>'],
        0x38: ['/','?'],
        0x39: ['[Caps Lock]','[Caps Lock]'],
        0x3a: ['[F1]','[F1]'],
        0x3b: ['[F2]','[F2]'],
        0x3c: ['[F3]','[F3]'],
        0x3d: ['[F4]','[F4]'],
        0x3e: ['[F5]','[F5]'],
        0x3f: ['[F6]','[F6]'],
        0x40: ['[F7]','[F7]'],
        0x41: ['[F8]','[F8]'],
        0x42: ['[F9]','[F9]'],
        0x43: ['[F10]','[F10]'],
        0x44: ['[F11]','[F11]'],
        0x45: ['[F12]','[F12]'],
        0x46: ['[PrintScreen]','[PrintScreen]'],
        0x47: ['[Scroll Lock]','[Scroll Lock]'],
        0x48: ['[Pause]','[Pause]'],
        0x49: ['[Insert]','[Insert]'],
        0x4a: ['[Home]','[Home]'],
        0x4b: ['[Page-Up]','[Page-Up]'],
        0x4c: ['[Delete Fwd]','[Delete Fwd]'],
        0x4d: ['[End]','[End]'],
        0x4e: ['[Page-Down]','[Page-Down]'],
        0x4f: ['[Right Arrow]','[Right Arrow]'],
        0x50: ['[Left Arrow]','[Left Arrow]'],
        0x51: ['[Down Arrow]','[Down Arrow]'],
        0x52: ['[Up Arrow]','[Up Arrow]'],
        0x53: ['[Num Lock]','[Clear]'],
        0x54: ['/','/'], # Keypads
        0x55: ['*','*'],
        0x56: ['-','-'],
        0x57: ['+','+'],
        0x58: ['\n','\n'], # TODO: Maybe replace with [ENTER]
        0x59: ['1','1'],
        0x5a: ['2','2'],
        0x5b: ['3','3'],
        0x5c: ['4','4'],
        0x5d: ['5','5'],
        0x5e: ['6','6'],
        0x5f: ['7','7'],
        0x60: ['8','8'],
        0x61: ['9','9'],
        0x62: ['0','0'],
        0x63: ['.','.'],
        0x64: ['\\','|'],
        0x65: ['[Application]','[Application]'],
        0x66: ['[Power]','[Power]'],
        0x67: ['=','='],
        0x68: ['[F13]','[F13]'],
        0x69: ['[F14]','[F14]'],
        0x6a: ['[F15]','[F15]'],
        0x6b: ['[F16]','[F16]'],
        0x6c: ['[F17]','[F17]'],
        0x6d: ['[F18]','[F18]'],
        0x6e: ['[F19]','[F19]'],
        0x6f: ['[F20]','[F20]'],
        0x70: ['[F21]','[F21]'],
        0x71: ['[F22]','[F22]'],
        0x72: ['[F23]','[F23]'],
        0x73: ['[F24]','[F24]'],
        0x74: ['[Execute]','[Execute]'],
        0x75: ['[Help]','[Help]'],
        0x76: ['[Menu]','[Menu]'],
        0x77: ['[Select]','[Select]'],
        0x78: ['[Stop]','[Stop]'],
        0x79: ['[Again]','[Again]'],
        0x7a: ['[Undo]','[Undo]'],
        0x7b: ['[Cut]','[Cut]'],
        0x7c: ['[Copy]','[Copy]'],
        0x7d: ['[Paste]','[Paste]'],
        0x7e: ['[Find]','[Find]'],
        0x7f: ['[Mute]','[Mute]'],
        0x80: ['[Volume Up]','[Volume Up]'],
        0x81: ['[Volume Down]','[Volume Down]'],
        0x82: ['[Caps Lock]','[Caps Lock]'],
        0x83: ['[Num Lock]','[Num Lock]'],
        0x84: ['[Scroll Lock]','[Scroll Lock]'],
        0x85: [',',','],
        0x86: ['=','='],
        0x87: ['1','1'],
        0x88: ['2','2'],
        0x89: ['3','3'],
        0x8a: ['4','4'],
        0x8b: ['5','5'],
        0x8c: ['6','6'],
        0x8d: ['7','7'],
        0x8e: ['8','8'],
        0x8f: ['9','9'],
        0x90: ['[LANG1]','[LANG1]'],
        0x91: ['[LANG2]','[LANG2]'],
        0x92: ['[LANG3]','[LANG3]'],
        0x93: ['[LANG4]','[LANG4]'],
        0x94: ['[LANG5]','[LANG5]'],
        0x95: ['[LANG6]','[LANG6]'],
        0x96: ['[LANG7]','[LANG7]'],
        0x97: ['[LANG8]','[LANG8]'],
        0x98: ['[LANG9]','[LANG9]'],
        0x99: ['[Alt Erase]','[Alt Erase]'],
        0x9a: ['[SysReq]','[SysReq]'],
        0x9b: ['[Cancel]','[Cancel]'],
        0x9c: ['[Clear]','[Clear]'],
        0x9d: ['[Prior]','[Prior]'],
        0x9e: ['[Return]','[Return]'],
        0x9f: ['[Separator]','[Separator]'],
        0xa0: ['[Out]','[Out]'],
        0xa1: ['[Oper]','[Oper]'],
        0xa2: ['[Clear]','[Clear]'],
        0xa3: ['[CrSel]','[CrSel]'],
        0xa4: ['[ExSel]','[ExSel]'],
        0xb0: ['00','00'],
        0xb1: ['000','000'],
        0xb2: ['[Thousands Separator]','[Thousands Separator]'],
        0xb3: ['[Decimal Separator]','[Decimal Separator]'],
        0xb4: ['[Currency Unit]','[Currency Unit]'],
        0xb5: ['[Currency Sub-Unit]','[Currency Sub-Unit]'],
        0xb6: ['(','('],
        0xb7: [')',')'],
        0xb8: ['{','{'],
        0xb9: ['}','}'],
        0xba: ['\t','\t'],
        0xbb: ['[Backspace]','[Backspace]'],
        0xbc: ['A','A'],
        0xbd: ['B','B'],
        0xbe: ['C','C'],
        0xbf: ['D','D'],
        0xc0: ['E','E'],
        0xc1: ['F','F'],
        0xc2: ['[xor]','[xor]'],
        0xc3: ['^','^'],
        0xc4: ['%','%'],
        0xc5: ['<','<'],
        0xc6: ['>','>'],
        0xc7: ['&','&'],
        0xc8: ['&&','&&'],
        0xc9: ['|','|'],
        0xca: ['||','||'],
        0xcb: [':',':'],
        0xcc: ['#','#'],
        0xcd: [' ',' '],
        0xce: ['@','@'],
        0xcf: ['!','!'],
        0xd0: ['[Memory Store]','[Memory Store]'],
        0xd1: ['[Memory Recall]','[Memory Recall]'],
        0xd2: ['[Memory Clear]','[Memory Clear]'],
        0xd3: ['[Memory Add]','[Memory Add]'],
        0xd4: ['[Memory Subtract]','[Memory Subtract]'],
        0xd5: ['[Memory Mult]','[Memory Mult]'],
        0xd6: ['[Memory Div]','[Memory Div]'],
        0xd7: ['+','-'],
        0xd8: ['[Clear]','[Clear]'],
        0xd9: ['[Clear Entry]','[Clear Entry]'],
        0xda: ['[Binary]','[Binary]'],
        0xdb: ['[Octal]','[Octal]'],
        0xdc: ['[Decimal]','[Decimal]'],
        0xdd: ['[Hexadecimal]','[Hexadecimal]'],
        0xe0: ['[Left-Control]','[Left-Control]'],
        0xe1: ['[Left-Shift]','[Left-Shift]'],
        0xe2: ['[Left-Alt]','[Left-Alt]'],
        0xe3: ['[Left-GUI]','[Left-GUI]'],
        0xe4: ['[Right-Control]','[Right-Control]'],
        0xe5: ['[Right-Shift]','[Right-Shift]'],
        0xe6: ['[Right-Alt]','[Right-Alt]'],
        0xe7: ['[Right-GUI]','[Right-GUI]'],
}

