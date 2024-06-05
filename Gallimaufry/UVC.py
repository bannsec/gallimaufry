
# Implementation of USB video class according to the document:
# "Universal Serial Bus Device Class Definition for Video Devices"
# Revision 1.5

# Control subypes
VC_DESCRIPTOR_UNDEFINED = 0x00
VC_HEADER               = 0x01
VC_INPUT_TERMINAL       = 0x02
VC_OUTPUT_TERMINAL      = 0x03
VC_SELECTOR_UNIT        = 0x04
VC_PROCESSING_UNIT      = 0x05
VC_EXTENSION_UNIT       = 0x06
VC_ENCODING_UNIT        = 0x07

# Streaming subtypes
VS_UNDEFINED            = 0x00
VS_INPUT_HEADER         = 0x01
VS_OUTPUT_HEADER        = 0x02
VS_STILL_IMAGE_FRAME    = 0x03
VS_FORMAT_UNCOMPRESSED  = 0x04
VS_FRAME_UNCOMPRESSED   = 0x05
VS_FORMAT_MJPEG         = 0x06
VS_FRAME_MJPEG          = 0x07
VS_FORMAT_MPEG2TS       = 0x0A
VS_FORMAT_DV            = 0x0C
VS_COLORFORMAT          = 0x0D
VS_FORMAT_FRAME_BASED   = 0x10
VS_FRAME_FRAME_BASED    = 0x11
VS_FORMAT_STREAM_BASED  = 0x12
VS_FORMAT_H264          = 0x13
VS_FRAME_H264           = 0x14
VS_FORMAT_H264_SIMULCAST= 0x15

controlSubtypes = {
        VC_DESCRIPTOR_UNDEFINED: 'Undefined',
        VC_HEADER: 'Header',
        VC_INPUT_TERMINAL: 'Input terminal',
        VC_OUTPUT_TERMINAL: 'Output terminal',
        VC_SELECTOR_UNIT: 'Selector Unit',
        VC_PROCESSING_UNIT: 'Processor unit',
        VC_EXTENSION_UNIT: 'Extension unit',
        VC_ENCODING_UNIT: 'Encoding unit'
        }

streamingSubtypes = {
        VS_UNDEFINED: 'Undefined',
        VS_INPUT_HEADER: 'Input header',
        VS_OUTPUT_HEADER: 'Output header',
        VS_STILL_IMAGE_FRAME: 'Still image frame',
        VS_FORMAT_UNCOMPRESSED: 'Format uncompressed',
        VS_FRAME_UNCOMPRESSED: 'Frame uncompressed',
        VS_FORMAT_MJPEG: 'Format MJPEG',
        VS_FRAME_MJPEG: 'Frame MJPEG',
        VS_FORMAT_MPEG2TS: 'Format MPEG2TS',
        VS_FORMAT_DV: 'Format DV',
        VS_COLORFORMAT: 'Color Format',
        VS_FORMAT_FRAME_BASED: 'Format frame based',
        VS_FRAME_FRAME_BASED: 'Frame frame based',
        VS_FORMAT_STREAM_BASED: 'Format stream based',
        VS_FORMAT_H264: 'Format H264',
        VS_FRAME_H264: 'Frame H264',
        VS_FORMAT_H264_SIMULCAST: 'Format H264 simulcast'
        }

class StreamingDescriptor:
    """Describes a Streaming descriptor.

    """
    def __init__(self, uvc_descriptor_packet):
        self._parse_uvc_streaming_descriptor_packet(uvc_descriptor_packet)

    def _parse_uvc_streaming_descriptor_packet(self, uvc_descriptor_packet):
        self.bDescriptorSubType = int(uvc_descriptor_packet['usbvideo.streaming.descriptorSubType'], 16)

    def __repr__(self) -> str:
        return "<StreamingDescriptor bDescriptorSubType={0}>".format(self.descriptor_subtype_str)

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """str: Returns textual summary of this descriptor."""
        summary = "Streaming Descriptor\n"
        summary += "-"*(len(summary)-1) + "\n"
        summary += "bDescriptorSubType: {0}\n".format(self.descriptor_subtype_str)
        return summary

    @property
    def descriptor_subtype_str(self) -> str:
        """str: String representation of descriptor subtype."""
        return streamingSubtypes[self.bDescriptorSubType]

class ControlDescriptor:
    """Describes a control descriptor.

    """
    def __init__(self, uvc_descriptor_packet):
        self._parse_uvc_control_descriptor_packet(uvc_descriptor_packet)

    def _parse_uvc_control_descriptor_packet(self, uvc_descriptor_packet):
        self.bDescriptorSubType = int(uvc_descriptor_packet['usbvideo.control.descriptorSubType'], 16)

    def __repr__(self) -> str:
        return "<ControlDescriptor bDescriptorSubType={0}>".format(self.descriptor_subtype_str)

    ##############
    # Properties #
    ##############

    @property
    def summary(self) -> str:
        """str: Returns textual summary of this descriptor."""
        summary = "Control Descriptor\n"
        summary += "-"*(len(summary)-1) + "\n"
        summary += "bDescriptorSubType: {0}\n".format(self.descriptor_subtype_str)
        return summary

    @property
    def descriptor_subtype_str(self) -> str:
        """str: String representation of descriptor subtype."""
        return controlSubtypes[self.bDescriptorSubType]
