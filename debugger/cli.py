import argparse
from debugger.tracer import Tracer
from debugger.logger import ErrorLogger

def parse_args():
    parser = argparse.ArgumentParser(description="Python Debugging Tool")
    parser.add_argument("script", help="Python script to debug")
    parser.add_argument("--trace", action="store_true", help="Trace execution")
    parser.add_argument("--vars", action="store_true", help="Show variables")
    return parser.parse_args()

def run_debugger():
    args = parse_args()
    tracer = Tracer(show_vars=args.vars)
    tracer.set_target(args.script)
    logger = ErrorLogger()

    try:
        if args.trace:
            tracer.start()

        with open(args.script) as f:
            code = f.read()
            exec(code, {})

    except Exception as e:
        print("[ERROR]", e)
        logger.log_error(e)

    finally:
        tracer.stop()