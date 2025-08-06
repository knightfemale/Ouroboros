# utils/config_util.py
import yaml
from pathlib import Path
from typing import Dict, Any

config_path: Path = Path("./ouroboros.yml")

def load_config(file_path: Path=config_path) -> Dict[str, Any]:
    """加载配置文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_config(config: Dict, file_path: Path=config_path) -> None:
    """保存配置文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)
