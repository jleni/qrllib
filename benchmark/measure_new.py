#!/usr/bin/env python
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from measure import measure
from pyqrllib import pyqrllib


def create_key(tree_height, seed):
    pyqrllib.Xmss(seed=seed, height=tree_height)


def sign(xmss, message):
    xmss.sign(message)


def verify(message, signature, pk, height):
    pyqrllib.Xmss.verify(message, signature, pk, height)


def prepare(height):
    seed = pyqrllib.ucharVector(48, 0)
    xmss = pyqrllib.Xmss(seed=seed, height=height)
    message = pyqrllib.ucharVector([i for i in range(256)])
    signature = xmss.sign(message)

    return seed, xmss, message, signature, xmss.getPK(), height


def run():
    measure('new', prepare, create_key, sign, verify)


if __name__ == '__main__':
    run()
