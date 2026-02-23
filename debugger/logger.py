import json
import traceback
from datetime import datetime
import os

LOG_FILE = "logs/errors.json"

class ErrorLogger:
    def __init__(self, file_path=LOG_FILE):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def log_error(self, e):
        tb = e.__traceback__
        # پیدا کردن آخرین frame برای اطلاعات دقیق‌تر
        crash_info = {}
        if tb:
            while tb.tb_next:
                tb = tb.tb_next
            crash_info = {
                "file": tb.tb_frame.f_code.co_filename,
                "line": tb.tb_lineno,
                "function": tb.tb_frame.f_code.co_name,
            }

        error_data = {
            "time": datetime.now().isoformat(),
            "type": type(e).__name__,
            "message": str(e),
            "crash_location": crash_info,
            "traceback": traceback.format_exc()
        }

        # خواندن لاگ‌های قبلی
        data = []
        if os.path.isfile(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            except (json.JSONDecodeError, IOError):
                data = []

        data.append(error_data)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[LOGGER] Error logged → {self.file_path} (total: {len(data)} errors)")