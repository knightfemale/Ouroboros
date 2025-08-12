# utils/config_util.py
import toml
import yaml
from pathlib import Path
from typing import Any, Dict

# 项目配置文件路径
config_path: Path = Path("./ouroboros.yml")
# uv 配置文件路径
uv_config_path: Path = Path("./pyproject.toml")
# 全局配置文件路径
global_config_path: Path = Path.home() / "ouroboros.toml"

def load_config(file_path: Path=config_path) -> Dict[str, Any]:
    """加载项目配置文件"""
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_config(config: Dict, file_path: Path=config_path) -> None:
    """保存项目配置文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)

def load_uv_config(file_path: Path=uv_config_path) -> Dict[str, Any]:
    """加载 uv 配置文件"""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return toml.load(f) or {}
        except Exception:
            return {}
    return {}

def save_uv_config(config: Dict, file_path: Path=uv_config_path) -> None:
    """保存 uv 配置文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)

def load_global_config() -> Dict[str, Any]:
    """加载全局配置文件"""
    if global_config_path.exists():
        try:
            with open(global_config_path, 'r', encoding='utf-8') as f:
                return toml.load(f) or {}
        except Exception:
            return {}
    return {}

def save_global_config(config: Dict) -> None:
    """保存全局配置文件"""
    with open(global_config_path, 'w', encoding='utf-8') as f:
        toml.dump(config, f)
