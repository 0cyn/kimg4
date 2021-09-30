
#
#  kimg4 | kimg4
#  img4.py
#
#
#
#  This file is part of kimg4. kimg4 is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) kat 2021.
#

import kimg4.asn1 as asn1
import pyaes


def asn1_serialize(input_stream, parent=None):
    """
    This is a serializer for the output of python-asn1.
    It's specifically designed for IMG4 format ASN1/DER/BER format.

    I really dont trust it, it's not very well designed, but it should work well enough.

    :param input_stream: Input asn1 decoder
    :param parent: unused element during recursion. would make things smarter.
    :return:
    """
    vals = []
    while not input_stream.eof():
        tag = input_stream.peek()
        if tag.typ == asn1.Types.Primitive:
            tag, value = input_stream.read()
            vals.append(value)
        elif tag.typ == asn1.Types.Constructed:
            input_stream.enter()
            items = asn1_serialize(input_stream, parent=asn1.Types.Constructed)
            input_stream.leave()
            vals.append(items)
    return vals


class Keybag:
    def __init__(self, index, iv, key):
        self.index = index
        self.iv = iv
        self.key = key


class ASN1Base:
    def __init__(self, data: bytes):
        self.raw_data = data
        decoder = asn1.Decoder()
        decoder.start(self.raw_data)
        self.serialized_data = asn1_serialize(decoder)


class KBAG(ASN1Base):
    """
     sequence [
            sequence [
                0: int: 01
                1: octetstring: iv
                2: octetstring: key
            ]
            sequence [
                0: int: 02
                1: octetstring: iv
                2: octetstring: key
            ]
         ]
    """
    def __init__(self, data: bytes):
        super().__init__(data)
        keybags = self.serialized_data[0]
        self.keybags = []
        for keybag in keybags:
            self.keybags.append(Keybag(keybag[0], keybag[1], keybag[2]))


class IM4P(ASN1Base):
    """
    sequence [
       0: string "IM4P"
       1: string type    - ibot, rdsk, sepi, ...
       2: string description    - 'iBoot-1940.1.75'
       3: octetstring    - the encrypted/raw data
       4: octetstring    - KBAG
      ]
    """
    def __init__(self, data: bytes):
        super().__init__(data)
        data = self.serialized_data[0]

        self.im4p_type = data[1]
        self.description = data[2]
        self.data = data[3]
        if len(data) > 4:
            self.encrypted = True
            self.kbag = KBAG(data[4])

    def decrypt_data(self, iv, key):
        aes = pyaes.AESModeOfOperationCBC(bytes.fromhex(key), iv=bytes.fromhex(iv))
        decrypter = pyaes.Decrypter(aes)
        decrypted = decrypter.feed(self.data)
        decrypted += decrypter.feed()
        return decrypted
