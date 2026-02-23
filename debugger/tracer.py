import sys
import os

class Tracer:
    def __init__(self, show_vars=False):
        self.show_vars = show_vars
        self.base_dir = os.getcwd()
        self.target_script = None  # فیلتر فقط روی اسکریپت هدف

    def set_target(self, script_path):
        """مسیر اسکریپت هدف رو ست می‌کنه تا فقط اون trace بشه"""
        self.target_script = os.path.abspath(script_path)

    def trace_func(self, frame, event, arg):
        filename = frame.f_code.co_filename
        abs_filename = os.path.abspath(filename)

        # خود tracer رو trace نکن
        if "tracer.py" in filename:
            return self.trace_func

        # اگه target مشخص شده، فقط اون فایل رو trace کن
        if self.target_script:
            if abs_filename != self.target_script:
                return self.trace_func
        else:
            # وگرنه فقط فایل‌های داخل پروژه رو trace کن
            if not abs_filename.startswith(self.base_dir):
                return self.trace_func

        if event == "line":
            lineno = frame.f_lineno
            # فقط اسم فایل رو نشون بده نه مسیر کامل
            short_name = os.path.relpath(abs_filename, self.base_dir)
            print(f"[TRACE] {short_name}:{lineno}")

            if self.show_vars:
                local_vars = {
                    k: v for k, v in frame.f_locals.items()
                    if not k.startswith("__")
                }
                if local_vars:
                    print(f"        Variables: {local_vars}")

        elif event == "call":
            func_name = frame.f_code.co_name
            if func_name != "<module>":
                short_name = os.path.relpath(abs_filename, self.base_dir)
                print(f"[CALL]  {short_name} → {func_name}()")

        elif event == "return":
            func_name = frame.f_code.co_name
            if func_name != "<module>" and arg is not None:
                print(f"[RETURN] {func_name}() → {arg!r}")

        elif event == "exception":
            exc_type, exc_value, _ = arg
            short_name = os.path.relpath(abs_filename, self.base_dir)
            print(f"[EXCEPTION] {short_name}:{frame.f_lineno} — {exc_type.__name__}: {exc_value}")

        return self.trace_func

    def start(self):
        sys.settrace(self.trace_func)

    def stop(self):
        sys.settrace(None)