import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from debugger.tracer import Tracer

def add(a, b):
    return a + b

tracer = Tracer(show_vars=True)
tracer.start()

x = 5
y = 8
print(add(x, y))

tracer.stop()