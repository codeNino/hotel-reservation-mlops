import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail=None):
        super().__init__(error_message)
        self.error_message = self._get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def _get_detailed_error_message(error_message, error_detail=None):
        _, _, exc_tb = sys.exc_info()

        if exc_tb is None and hasattr(error_detail, "__traceback__"):
            exc_tb = error_detail.__traceback__

        if exc_tb:
            tb_summary = traceback.extract_tb(exc_tb)[-1]
            file_name = tb_summary.filename
            line_number = tb_summary.lineno
            func_name = tb_summary.name
            return f"Error in {file_name}, function '{func_name}', line {line_number} :: {error_message}"
        else:
            return f"Error: {error_message}"

    def __str__(self):
        return self.error_message