import time
import sys


t0 = time.time()
try:
    import heavy_module_no_annotations
except ImportError:
    print('Run `generate_heavy_modules.py` first.', file=sys.stderr)
    sys.exit(1)
t1 = time.time()
no_ann = t1 - t0
print(f"No Annotations: {no_ann:.2f}s")

t0 = time.time()
try:
    import heavy_module_annotations
except ImportError:
    print('Run `generate_heavy_modules.py` first.', file=sys.stderr)
    sys.exit(1)
t1 = time.time()
with_ann = t1 - t0
print(f"Annotations: {with_ann:.2f}s")

print(f"Difference: {with_ann - no_ann:.2f} seconds")
