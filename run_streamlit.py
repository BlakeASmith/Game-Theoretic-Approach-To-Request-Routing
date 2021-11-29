import os
from pathlib import Path

here = Path(__file__).parent
main_py = here / "request_routing_game/main.py"

def main():
    os.system(f"streamlit run {main_py}")