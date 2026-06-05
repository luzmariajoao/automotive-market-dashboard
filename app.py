"""Entry point para Streamlit Cloud — redirige para src/dashboard.py"""
pythonimport sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
exec(open(Path(__file__).parent / "dashboard.py").read())
