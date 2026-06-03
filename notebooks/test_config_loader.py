import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config

config = load_config()

print("Pipeline name:", config["pipeline"]["name"])
print("Pipeline mode:", config["pipeline"]["mode"])
print("Source path:", config["source"]["path"])
print("Bronze path:", config["bronze"]["path"])
print("Silver path:", config["silver"]["path"])
print("Gold path:", config["gold"]["path"])
print("Metadata path:", config["metadata"]["path"])