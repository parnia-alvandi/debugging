import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'debugger')))

from tracer import Tracer

# ایجاد شیء Tracer و فعال کردن آن
tracer = Tracer(show_vars=True)
tracer.start()

# کد اصلی پروژه
def add(a, b):
    return a + b

x = 5
y = 8
print(add(x, y))

# غیرفعال کردن trace در آخر
tracer.stop()