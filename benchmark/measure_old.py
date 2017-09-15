#!/usr/bin/env python
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import time

import csv
from binascii import hexlify

from qrl.crypto import hmac_drbg
from qrl.crypto.xmss import XMSS

test_set = 'old'

def measure_execution_time(f, samples, iterations, *args, **kwargs):
    timings = []
    for i in range(iterations):
        start = time.time()

        for _ in range(samples):
            f(*args, **kwargs)

        end = time.time()
        elapsed = (end - start) / samples
        timings.append(elapsed)
    return timings


def create_key(tree_height, seed):
    XMSS(2 ** tree_height, seed)


def sign(xmss, message):
    xmss.SIGN(message)


def verify(message, signature):
    XMSS.VERIFY(message, signature)


def main():
    data = []

    ITERATIONS = 1
    SAMPLES_CREATE = 1
    SAMPLES_SIGN = 1
    SAMPLES_VERIFY = 1000

    for height in range(2, 4):
        print("Height : {}".format(height))

        # prepare data
        old_seed, old_pseed, old_sseed = hmac_drbg.new_keys()
        num_signatures = 2 ** height
        old_xmss = XMSS(num_signatures, old_seed)
        old_message = hexlify(bytearray([i for i in range(256)]))
        old_signature = old_xmss.SIGN(old_message)

        print("Benchmarking legacy")
        r = measure_execution_time(create_key, SAMPLES_CREATE, ITERATIONS, height, old_seed)

        data.append([test_set, 'create', height, max(r)])

        r = measure_execution_time(sign, SAMPLES_SIGN, ITERATIONS, old_xmss, old_message)
        data.append([test_set, 'sign', height, max(r)])

        r = measure_execution_time(verify, SAMPLES_VERIFY, ITERATIONS, old_message, old_signature)
        data.append([test_set, 'verify', height, max(r)])


    with open('data_{}.csv'.format(test_set), 'w') as f:
        field_names = ['source', 'operation', 'height', 'time']
        writer = csv.writer(f)
        writer.writerow(field_names)
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    main()
