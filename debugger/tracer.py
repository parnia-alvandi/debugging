import sys
import os

class Tracer:
    def __init__(self, show_vars=False):
        self.show_vars = show_vars
        self.base_dir = os.getcwd()        #Project folder

    def trace_func(self, frame, event, arg):
        filename = frame.f_code.co_filename

        if "tracer.py" in filename:        #Don't trace "tracer.py"
            return self.trace_func

        if not filename.startswith(self.base_dir):       #Only project files
            return self.trace_func

        if event == "line":
            lineno = frame.f_lineno
            print(f"[TRACE] {filename}:{lineno}")

            if self.show_vars:
                local_vars = {
                    k: v for k, v in frame.f_locals.items()
                    if not k.startswith("__")
                }
                print(f"   Variables: {local_vars}")

        return self.trace_func

    def start(self):
        sys.settrace(self.trace_func)

    def stop(self):
        sys.settrace(None)