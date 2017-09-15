#!/usr/bin/env python
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import time

import csv

from pyqrllib import pyqrllib

test_set = 'new'

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
    pyqrllib.Xmss(seed=seed, height=tree_height)


def sign(xmss, message):
    xmss.sign(message)


def verify(message, signature, pk, height):
    pyqrllib.Xmss.verify(message, signature, pk, height)


def main():
    data = []

    ITERATIONS = 1
    SAMPLES_CREATE = 1
    SAMPLES_SIGN = 1
    SAMPLES_VERIFY = 1000

    for height in range(2, 4):
        print("Height : {}".format(height))

        # prepare data
        seed = pyqrllib.ucharVector(48, 0)
        xmss = pyqrllib.Xmss(seed=seed, height=height)
        message = pyqrllib.ucharVector([i for i in range(256)])
        signature = xmss.sign(message)

        print("Benchmarking qrllib")
        r = measure_execution_time(create_key, SAMPLES_CREATE, ITERATIONS, height, seed)
        data.append([test_set, 'create', height, max(r)])

        r = measure_execution_time(sign, SAMPLES_SIGN, ITERATIONS, xmss, message)
        data.append([test_set, 'sign', height, max(r)])

        r = measure_execution_time(verify, SAMPLES_VERIFY, ITERATIONS,
                                   message, signature, xmss.getPK(), xmss.getHeight())
        data.append([test_set, 'verify', height, max(r)])

    with open('data_{}.csv'.format(test_set), 'w') as f:
        field_names = ['source', 'operation', 'height', 'time']
        writer = csv.writer(f)
        writer.writerow(field_names)
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    main()
