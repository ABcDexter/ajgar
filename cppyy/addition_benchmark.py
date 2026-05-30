###########
# Imports #
###########
import cppyy
import cProfile
from datetime import datetime
import time

###############
# Cppyy Setup #
###############
cppyy.cppdef("""
int add(int a, int b) {
    return a + b;
}
""")

#################
# CPython Setup #
##################
def py_add(a, b):
    return a + b

#########################
# Benchmarking function #
#########################

def benchmark_loop(func, iterations=1_000_000):
    #simple, not so efficient
    start_time = datetime.now()
    for _ in range(iterations):
        func(1, 2)
    end_time = datetime.now()
    return end_time - start_time


def benchmark_profiler(func, iterations=1_000_000):
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(iterations):
        func(1, 2)
    profiler.disable()
    profiler.print_stats()
    #return the time taken for the benchmark
    return profiler.dump_stats("benchmark.prof")


def benchmark_time(func, iterations=1_000_000):
    start_time = time.perf_counter_ns()
    for _ in range(iterations):
        func(1, 2)
    end_time = time.perf_counter_ns()
    return str((end_time - start_time)//1000000) + " milliseconds"

##################
# Run Benchmarks #
##################


# run a million additions to benchmark the performance of the Python function
time_py = benchmark_time(py_add)
print(f"Python addition took: {time_py}")

# run a million additions to benchmark the performance of the C++ function
time_cpp = benchmark_time(cppyy.gbl.add)
print(f"C++ addition took: {time_cpp}")

