import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.metadata_utils import read_json_file


state = read_json_file("data/metadata/orders_state.json")

print("Orders metadata state:")
print(state)

print("Last loaded updated_at:")
print(state["last_loaded_updated_at"])