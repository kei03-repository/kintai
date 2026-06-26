from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_FILE = BASE_DIR.parent.parent / "業務進捗報告_島.xlsx"
TEMPLATE_SOURCE = os.getenv("TEMPLATE_SOURCE", str(DEFAULT_TEMPLATE_FILE))
OUTPUT_DIR = BASE_DIR.parent / "excel_output"
