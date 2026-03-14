# utils/platform_util.py
import os
import platform
import subprocess
from typing import Optional


_system: Optional[str] = None


def get_system() -> str:
    """获取系统类型(缓存结果)"""

    global _system
    if _system is None:
        _system = platform.system()
    return _system


def is_windows() -> bool:
    """是否为 Windows"""

    return get_system() == "Windows"


def is_linux() -> bool:
    """是否为 Linux"""

    return get_system() == "Linux"


def run_command(command: str) -> None:
    """在后台线程中执行命令, GUI 退出后命令会继续运行"""

    subprocess.Popen(command, shell=True, cwd=os.getcwd())
