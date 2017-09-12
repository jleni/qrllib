# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from __future__ import print_function

from time import sleep, time
from unittest import TestCase

from pyqrllib import pyqrllib


class TestHash(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHash, self).__init__(*args, **kwargs)

    def test_xmss(self):
        HEIGHT = 6

        seed = pyqrllib.ucharVector(32, 0)
        xmss = pyqrllib.Xmss(seed=seed, height=HEIGHT)

        print("Seed", len(seed))
        print(pyqrllib.vec2hexstr(seed, 32))

        print("PK  ", len(xmss.getPK()))
        print(pyqrllib.vec2hexstr(xmss.getPK(), 32))

        print("SK  ", len(xmss.getSK()))
        print(pyqrllib.vec2hexstr(xmss.getSK(), 32))

        self.assertIsNotNone(xmss)
        self.assertEqual(xmss.getHeight(), HEIGHT)

        message = pyqrllib.ucharVector([i for i in range(32)])
        print("Msg ", len(message))
        print(pyqrllib.vec2hexstr(message, 32))

        # Sign message
        signature = bytearray(xmss.sign(message))

        print("Sig ", len(signature))
        print(pyqrllib.vec2hexstr(signature, 128))

        print('----------------------------------------------------------------------')
        # Verify signature
        start = time()
        for i in range(1000):
            self.assertTrue(pyqrllib.verify(message,
                                            signature,
                                            xmss.getPK(),
                                            xmss.getHeight()))
        end = time()
        print(end - start)

        # Touch the signature
        signature[100] += 1
        self.assertFalse(pyqrllib.verify(message,
                                         signature,
                                         xmss.getPK(),
                                         xmss.getHeight()))
        signature[100] -= 1
        self.assertTrue(pyqrllib.verify(message,
                                        signature,
                                        xmss.getPK(),
                                        xmss.getHeight()))

        # Touch the message
        message[2] += 1
        self.assertFalse(pyqrllib.verify(message,
                                         signature,
                                         xmss.getPK(),
                                         xmss.getHeight()))
        message[2] -= 1
        self.assertTrue(pyqrllib.verify(message,
                                        signature,
                                        xmss.getPK(),
                                        xmss.getHeight()))
