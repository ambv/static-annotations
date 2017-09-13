import sys
import tracemalloc


tracemalloc.start()
try:
    import heavy_module_no_annotations
except ImportError:
    print('Run `generate_heavy_modules.py` first.', file=sys.stderr)
    sys.exit(1)
snapshot = tracemalloc.take_snapshot()
mem_size2 = sum(stat.size for stat in snapshot.statistics('filename'))
print(f"No Annotations: {mem_size2/1024/1024:.2f} MB")
tracemalloc.stop()

tracemalloc.start()
try:
    import heavy_module_annotations
except ImportError:
    print('Run `generate_heavy_modules.py` first.', file=sys.stderr)
    sys.exit(1)
snapshot = tracemalloc.take_snapshot()
mem_size1 = sum(stat.size for stat in snapshot.statistics('filename'))
print(f"Annotations: {mem_size1/1024/1024:.2f} MB")
tracemalloc.stop()

print(f"Difference: {(mem_size1-mem_size2)/1024/1024:.2f} MB")
