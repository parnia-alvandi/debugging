import argparse
import os
import sys
from debugger.tracer import Tracer
from debugger.logger import ErrorLogger
from debugger.inspector import VariableInspector

def parse_args():
    parser = argparse.ArgumentParser(description="Python Debugging Tool")
    parser.add_argument("script", help="Python script to debug")
    parser.add_argument("--trace", action="store_true", help="Trace execution line by line")
    parser.add_argument("--vars", action="store_true", help="Show local variables on each line")
    parser.add_argument("--inspect", action="store_true", help="Inspect variables on error")
    return parser.parse_args()

def run_debugger():
    args = parse_args()

    # بررسی وجود فایل قبل از هر کاری
    if not os.path.isfile(args.script):
        print(f"[ERROR] File not found: '{args.script}'")
        sys.exit(1)

    tracer = Tracer(show_vars=args.vars)
    tracer.set_target(args.script)  # ← حالا این متد وجود داره
    logger = ErrorLogger()

    # context درست برای exec
    script_globals = {
        "__file__": os.path.abspath(args.script),
        "__name__": "__main__",
    }

    print(f"[DEBUG] Running: {args.script}")
    print("-" * 40)

    try:
        if args.trace:
            tracer.start()

        with open(args.script) as f:
            code = compile(f.read(), args.script, "exec")  # compile بهتر از exec مستقیم
            exec(code, script_globals)

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")

        # اگه --inspect بود، متغیرهای آخرین frame رو نشون بده
        if args.inspect:
            import traceback
            tb = e.__traceback__
            while tb.tb_next:
                tb = tb.tb_next
            frame = tb.tb_frame
            variables = VariableInspector.inspect(frame)
            if variables:
                print(f"[INSPECT] Variables at crash point: {variables}")

        logger.log_error(e)

    finally:
        tracer.stop()
        print("-" * 40)
        print("[DEBUG] Execution finished.")