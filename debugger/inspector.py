class VariableInspector:
    @staticmethod
    def inspect(frame):
        return frame.f_locals.copy()