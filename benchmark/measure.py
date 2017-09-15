#!/usr/bin/env python
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import time

import csv


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


def measure(test_set,
            prepare,
            create_key,
            sign,
            verify):
    data = []

    ITERATIONS = 3
    SAMPLES_CREATE = 3
    SAMPLES_SIGN = 16
    SAMPLES_VERIFY = 1000

    with open('data_{}.csv'.format(test_set), 'a') as f:
        field_names = ['source', 'operation', 'height', 'time']
        writer = csv.writer(f)
        writer.writerow(field_names)

        for height in range(4, 18, 2):
            # prepare data
            seed, xmss, message, signature, pk, height = prepare(height)

            # r = measure_execution_time(create_key, SAMPLES_CREATE, ITERATIONS, height, seed)
            # writer.writerow([test_set, 'create', height, max(r)])
            #
            # print("[{:8}] h={} create {}".format(test_set, height, max(r)))

            r = measure_execution_time(sign, SAMPLES_SIGN, ITERATIONS, xmss, message)
            writer.writerow([test_set, 'sign', height, max(r)])
            print("[{:8}] h={} sign   {}".format(test_set, height, max(r)))

            # r = measure_execution_time(verify, SAMPLES_VERIFY, ITERATIONS,
            #                            message, signature, pk, height)
            # writer.writerow([test_set, 'verify', height, max(r)])
            # print("[{:8}] h={} verify {}".format(test_set, height, max(r)))
