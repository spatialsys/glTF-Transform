from collections import defaultdict
from statistics import mean, stdev
from tabulate import tabulate
import os
from timeit import default_timer as timer


FILE="/Users/mike/Downloads/champagne.glb"
FILE="/Users/mike/Downloads/hospital-room_m2-intuitive.glb"
#FILE="/Users/mike/Downloads/champagne.glb"
FILE="/Users/mike/Downloads/luis/arlo.glb"

results = defaultdict(lambda: defaultdict(dict))


iterations = range(3)
jobs = [1, 2, 4, 5, 6, 7, 10]
ktx_threads = [1, 2, 3, 4, 5, 6, 7, 10, 20]
fast_run=False
print_averages_every_run=True
if fast_run:
    iterations = range(2)
    jobs = [5]
    ktx_threads = [1, 4]
medium_run=False
if medium_run:
    iterations = range(5)
    jobs = [5]
    ktx_threads = [1, 4]

def print_averages():
    averages = defaultdict(lambda: defaultdict(dict))
    for num_jobs, t in results.items():
        for num_ktx_threads, u in t.items():
            averages[num_jobs][num_ktx_threads] = mean(u.values())

    table = []
    for num_jobs, t in averages.items():
        row = ["%d jobs" % num_jobs]
        row += [v for v in t.values()]

        table.append(row)
    print(tabulate(table, ["%d ktx threads" % d for d in ktx_threads]))

def print_averages_and_std_dev():
    averages = defaultdict(lambda: defaultdict(dict))
    std_devs = defaultdict(lambda: defaultdict(dict))
    for num_jobs, t in results.items():
        for num_ktx_threads, u in t.items():
            if len(u.values()) > 1:
                averages[num_jobs][num_ktx_threads] = "%.2f ± %.2f" % (mean(u.values()), stdev(u.values()))
            else:
                averages[num_jobs][num_ktx_threads] = "%.2f" % mean(u.values())

    table = []
    for num_jobs, t in averages.items():
        row = ["%d jobs" % num_jobs]
        row += [v for v in t.values()]

        table.append(row)
    print(tabulate(table, ["%d ktx threads" % d for d in ktx_threads]))

for iter in iterations:
    for num_jobs in jobs:
        for num_ktx_threads in ktx_threads:
            start = timer()
            cmd = 'time node packages/cli/bin/cli.js etc1s --quality 255 --slots \!normalTexture --jobs=%d --ktx-threads=%d %s %s.tc.glb' % (num_jobs, num_ktx_threads, FILE, FILE)
            print(cmd)
            os.system(cmd)
            elapsed_time = timer() - start
            results[num_jobs][num_ktx_threads][iter] = elapsed_time
            if print_averages_every_run:
                print_averages_and_std_dev()



print_averages()

