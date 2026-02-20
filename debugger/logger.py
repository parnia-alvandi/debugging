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
        error_data = {
            "time": datetime.now().isoformat(),
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }

        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(error_data)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        print("[LOGGER] Error saved to logs/errors.json")