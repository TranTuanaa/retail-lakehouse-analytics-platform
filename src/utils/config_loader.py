from pathlib import Path
import yaml


def load_config(config_path: str = "configs/pipeline.yaml") -> dict:
    """
    Load pipeline configuration from a YAML file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        A dictionary containing pipeline configuration.
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config