class VariableInspector:
    @staticmethod
    def inspect(frame):
        """متغیرهای محلی یه frame رو برمی‌گردونه (بدون متغیرهای دندری)"""
        return {
            k: v for k, v in frame.f_locals.items()
            if not k.startswith("__")
        }

    @staticmethod
    def inspect_all_frames(tb):
        """همه frame‌های traceback رو بررسی می‌کنه"""
        frames = []
        while tb:
            frame = tb.tb_frame
            frames.append({
                "file": frame.f_code.co_filename,
                "line": tb.tb_lineno,
                "function": frame.f_code.co_name,
                "locals": VariableInspector.inspect(frame)
            })
            tb = tb.tb_next
        return frames