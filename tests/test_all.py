import sys
import os
import json
import tempfile
import unittest

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from debugger.tracer import Tracer
from debugger.logger import ErrorLogger
from debugger.inspector import VariableInspector


class TestTracer(unittest.TestCase):

    def test_tracer_has_set_target(self):
        """set_target باید وجود داشته باشه"""
        tracer = Tracer()
        self.assertTrue(hasattr(tracer, "set_target"), "set_target method is missing!")

    def test_set_target_sets_path(self):
        """set_target باید مسیر رو ست کنه"""
        tracer = Tracer()
        tracer.set_target("examples/buggy_program.py")
        self.assertIsNotNone(tracer.target_script)

    def test_tracer_start_stop(self):
        """start و stop نباید خطا بدن"""
        tracer = Tracer()
        tracer.start()
        tracer.stop()

    def test_tracer_show_vars_flag(self):
        """show_vars باید درست ست بشه"""
        tracer = Tracer(show_vars=True)
        self.assertTrue(tracer.show_vars)


class TestErrorLogger(unittest.TestCase):

    def setUp(self):
        # یه فایل موقت برای لاگ
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.logger = ErrorLogger(file_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_log_error_creates_entry(self):
        """log_error باید یه entry در JSON بسازه"""
        try:
            raise ValueError("test error")
        except ValueError as e:
            self.logger.log_error(e)

        with open(self.tmp.name) as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["type"], "ValueError")
        self.assertEqual(data[0]["message"], "test error")
        self.assertIn("time", data[0])
        self.assertIn("traceback", data[0])

    def test_log_multiple_errors(self):
        """چند بار لاگ کردن باید همه رو نگه داره"""
        for i in range(3):
            try:
                raise RuntimeError(f"error {i}")
            except RuntimeError as e:
                self.logger.log_error(e)

        with open(self.tmp.name) as f:
            data = json.load(f)

        self.assertEqual(len(data), 3)

    def test_log_has_crash_location(self):
        """لاگ باید اطلاعات محل crash رو داشته باشه"""
        try:
            raise ZeroDivisionError("division by zero")
        except ZeroDivisionError as e:
            self.logger.log_error(e)

        with open(self.tmp.name) as f:
            data = json.load(f)

        self.assertIn("crash_location", data[0])


class TestVariableInspector(unittest.TestCase):

    def test_inspect_returns_locals(self):
        """inspect باید متغیرهای محلی رو برگردونه"""
        import inspect
        frame = inspect.currentframe()
        x = 42
        y = "hello"
        result = VariableInspector.inspect(frame)
        self.assertIn("x", result)
        self.assertIn("y", result)

    def test_inspect_filters_dunder(self):
        """متغیرهای __ نباید برگشت داده بشن"""
        import inspect
        frame = inspect.currentframe()
        result = VariableInspector.inspect(frame)
        for key in result:
            self.assertFalse(key.startswith("__"))

    def test_inspect_all_frames(self):
        """inspect_all_frames باید یه لیست برگردونه"""
        try:
            raise ValueError("test")
        except ValueError as e:
            frames = VariableInspector.inspect_all_frames(e.__traceback__)
            self.assertIsInstance(frames, list)
            self.assertGreater(len(frames), 0)
            self.assertIn("file", frames[0])
            self.assertIn("line", frames[0])
            self.assertIn("locals", frames[0])


class TestCLIIntegration(unittest.TestCase):

    def test_buggy_program_runs_and_logs(self):
        """buggy_program باید اجرا بشه و خطاش لاگ بشه"""
        tmp_log = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp_log.close()

        logger = ErrorLogger(file_path=tmp_log.name)
        try:
            # شبیه‌سازی اجرای buggy_program
            exec(open("examples/buggy_program.py").read(), {"__name__": "__main__"})
        except ZeroDivisionError as e:
            logger.log_error(e)

        with open(tmp_log.name) as f:
            data = json.load(f)

        self.assertEqual(data[0]["type"], "ZeroDivisionError")
        os.unlink(tmp_log.name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
