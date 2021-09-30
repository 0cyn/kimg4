#
#  kimg4 | tests
#  tests.py
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

import unittest
from kimg4.img4 import *


class TestCase(unittest.TestCase):
    def test_img4(self):
        with open('bins/iBoot.d10.RELEASE.im4p', 'rb') as infp:
            with open('bins/iboot.dec', 'wb') as out:
                img4 = IM4P(infp.read())
                dec = img4.decrypt_data('63333cd053f28fba0f4117041bbfe7d5', 'd115427fc0d078aae70515b93640b606eb62c48147a3ec4d44be1f97c0570e8e')
                out.write(dec)


if __name__ == '__main__':
    unittest.main()
