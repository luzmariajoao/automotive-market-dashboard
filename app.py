"""Entry point para Streamlit Cloud — redirige para src/dashboard.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
exec(open(Path(__file__).parent / "src" / "dashboard.py").read())
