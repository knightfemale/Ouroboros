# utils/python_path_util.py
import platform
from typing import List
from pathlib import Path


def get_python_path() -> str:
    """获取可能的 Python 解释器路径"""
    if platform.system() == "Windows":
        possible_paths: List[Path] = [
            Path.cwd() / ".venv" / "python.exe",
            Path.cwd() / ".venv" / "Scripts" / "python.exe",
        ]
    elif platform.system() == "Linux":
        possible_paths: List[Path] = [
            Path.cwd() / ".venv" / "bin" / "python",
            Path.cwd() / ".venv" / "bin" / "python3",
        ]
    else:
        possible_paths: List[Path] = []
    for path in possible_paths:
        if path.exists():
            return str(path)
    return ""
