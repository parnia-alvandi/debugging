import sys

class Tracer:
    def __init__(self, show_vars=False):
        self.show_vars = show_vars

    def trace_func(self, frame, event, arg):
        if event == "line":
            lineno = frame.f_lineno
            filename = frame.f_code.co_filename
            print(f"[TRACE] {filename}:{lineno}")

            if self.show_vars:
                # فقط متغیرهای کاربر (نه builtins)
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