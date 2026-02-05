# utils/platform_util.py
import shutil
import platform
import subprocess
from typing import Optional, List, Tuple


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


def run_in_terminal(title: str, command: str) -> None:
    """在新终端中执行命令(仅 Linux)"""

    terminals: List[Tuple[str, List[str]]] = [
        ("konsole", ["konsole", "--new-tab", "-e", "bash", "-c", f"{command}; read"]),
        ("gnome-terminal", ["gnome-terminal", "--", "bash", "-c", f"{command}; read"]),
        ("xfce4-terminal", ["xfce4-terminal", "-e", f"bash -c '{command}; read'"]),
        ("xterm", ["xterm", "-e", "bash", "-c", f"{command}; read"]),
        ("eterm", ["eterm", "-e", "bash", "-c", f"{command}; read"]),
        ("urxvt", ["urxvt", "-e", "bash", "-c", f"{command}; read"]),
        ("lxterminal", ["lxterminal", "-e", "bash", "-c", f"{command}; read"]),
        ("mate-terminal", ["mate-terminal", "--", "bash", "-c", f"{command}; read"]),
    ]
    for name, args in terminals:
        if shutil.which(name):
            subprocess.Popen(args)
            return
    subprocess.Popen(["bash", "-c", f"{command}; read"])
