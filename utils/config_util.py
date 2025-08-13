# utils/config_util.py
import yaml
import tomlkit
from pathlib import Path
from typing import Any, Dict
from tomlkit.items import Array, Table

# 项目配置文件路径
config_path: Path = Path("./ouroboros.yml")
# uv 配置文件路径
uv_config_path: Path = Path("./pyproject.toml")
# 全局配置文件路径
global_config_path: Path = Path.home() / "ouroboros.toml"

def load_yaml(file_path: Path) -> Dict[str, Any]:
    """加载 YAML 文件"""
    if file_path.exists():
        with open(file_path, "r", encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_yaml(config: Dict, file_path: Path) -> None:
    """保存 YAML 文件"""
    with open(file_path, "w", encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)

def load_toml(file_path: Path) -> Dict[str, Any]:
    """加载 TOML 文件"""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content: str = f.read()
                return tomlkit.parse(content).unwrap()
        except Exception:
            return {}
    return {}

def save_toml(config: Dict, file_path: Path) -> None:
    """保存 TOML 文件"""
    doc: tomlkit.TOMLDocument = tomlkit.document()
    for key, value in config.items():
        doc[key] = process_value(value)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(doc))

def process_value(value) -> Array | Table | Any:
    """递归处理使所有数组都使用多行格式"""
    if isinstance(value, list):
        array: Array = tomlkit.array()
        array.multiline(True)
        for item in value:
            array.append(process_value(item))
        return array
    elif isinstance(value, dict):
        table: Table = tomlkit.table()
        for k, v in value.items():
            table[k] = process_value(v)
        return table
    else:
        return value
