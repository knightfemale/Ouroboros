# utils/delay_util.py
import subprocess
from typing import List, Callable
from PySide6.QtWidgets import QWidget, QLabel

def label_operate(lable: QLabel, text: str) -> None:
    """默认的设置标签方式"""
    lable.setText(text)

def set_delay_lable(
    parent: QWidget,
    var_name: str,
    lable: QLabel,
    command: List[str],
    prefix: str,
    err: str,
    operate: Callable[[QLabel, str], None],
) -> None:
    """设置延时标签"""
    var = getattr(parent, var_name)
    if var:
        operate(lable, var)
        return
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True,
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            text = f"{prefix}{stdout.strip()}"
            setattr(parent, var_name, text)
            operate(lable, text)
        else:
            text = stderr.strip() or "Unknown error"
            lable.setText(f"{prefix}{err}: {text}")
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        lable.setText(f"{prefix}{err}: {str(e)}")
