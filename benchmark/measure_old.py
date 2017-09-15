#!/usr/bin/env python
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from binascii import hexlify

from qrl.crypto import hmac_drbg
from qrl.crypto.xmss import XMSS

from measure import measure


def create_key(tree_height, seed):
    XMSS(tree_height, seed)


def sign(xmss, message):
    xmss.SIGN(message)


def verify(message, signature, pk, height):
    XMSS.VERIFY(message, signature)


def prepare(height):
    seed, _, _ = hmac_drbg.new_keys()
    xmss = XMSS(height, seed)
    message = hexlify(bytearray([i for i in range(256)]))
    signature = xmss.SIGN(message)

    return seed, xmss, message, signature, None, height


def run():
    measure('old', prepare, create_key, sign, verify)


if __name__ == '__main__':
    run()
