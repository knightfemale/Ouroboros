# utils/config_util.py
import yaml
import tomlkit
from pathlib import Path
from typing import Any, Dict
from tomlkit.items import Array, Table
from tomlkit import TOMLDocument, parse, document, dumps


# 项目配置文件路径
config_path: Path = Path("./pyproject.toml")
# 全局配置文件路径
global_config_path: Path = Path.home() / "ouroboros.toml"


def load_yaml(file_path: Path) -> Dict[str, Any]:
    """加载 YAML 文件"""
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def save_yaml(config: Dict, file_path: Path) -> None:
    """保存 YAML 文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)


def load_toml(file_path: Path) -> Dict[str, Any]:
    """加载 TOML 文件"""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content: str = f.read()
                return parse(content).unwrap()
        except Exception:
            return {}
    return {}


def save_toml(config: Dict, file_path: Path) -> None:
    """保存 TOML 文件"""
    doc: TOMLDocument = document()
    # 递归处理配置字典
    for key, value in config.items():
        doc[key] = process_value_recursive(value)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(dumps(doc))


def process_value_recursive(value: Any) -> Any:
    """递归处理值, 保持 TOML 结构的完整性"""
    if isinstance(value, list):
        return process_array(value)
    elif isinstance(value, dict):
        return process_table(value)
    else:
        return value


def process_array(items: list) -> Array:
    """处理数组, 保持多行格式"""
    array: Array = tomlkit.array()
    array.multiline(True)
    for item in items:
        if isinstance(item, dict):
            # 对于字典项, 创建内联表格
            inline_table = tomlkit.inline_table()
            for k, v in item.items():
                inline_table[k] = process_value_recursive(v)
            array.append(inline_table)
        else:
            array.append(process_value_recursive(item))
    return array


def process_table(data: dict) -> Table:
    """处理表格结构"""
    table: Table = tomlkit.table()
    for key, value in data.items():
        if isinstance(value, dict):
            # 嵌套表格
            nested_table = process_table(value)
            table[key] = nested_table
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # 数组的表格（如 [[tool.uv.index]]）
            table[key] = process_array_of_tables(value)
        else:
            table[key] = process_value_recursive(value)
    return table


def process_array_of_tables(items: list) -> list:
    """处理表格数组(如 [[tool.uv.index]])"""
    result = []
    for item in items:
        if isinstance(item, dict):
            table = tomlkit.table()
            for k, v in item.items():
                table[k] = process_value_recursive(v)
            result.append(table)
    return result
