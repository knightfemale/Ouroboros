# utils/delay_util.py
import subprocess
from PySide6.QtCore import QThread, Signal
from typing import List, Callable, Optional
from PySide6.QtWidgets import QWidget, QLabel

class DelayLabelThread(QThread):
    # 信号: 结果文本, 变量名, 前缀
    result_ready = Signal(str, str, str)
    
    def __init__(self, command: List[str], prefix: str, err: str,parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.command = command
        self.prefix = prefix
        self.err = err
    
    def run(self) -> None:
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
                text=True,
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.result_ready.emit(stdout.strip(), "", f"{self.prefix}")
            else:
                error_msg = stderr.strip() or "Unknown error"
                self.result_ready.emit(f"{self.prefix}{self.err}: {error_msg}", "", "")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            self.result_ready.emit(f"{self.prefix}{self.err}: {str(e)}", "", "")

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
    # 如果已有缓存值，直接使用
    if hasattr(parent, var_name) and getattr(parent, var_name):
        operate(lable, getattr(parent, var_name))
        return
    # 创建并启动后台线程
    thread = DelayLabelThread(command, prefix, err, parent)
    # 连接信号
    def handle_result(text: str, target_var: str, result_prefix: str) -> None:
        if target_var:
            # 如果设置了变量名，则缓存结果
            full_text = f"{result_prefix}{text}"
            setattr(parent, target_var, full_text)
            operate(lable, full_text)
        else:
            # 直接更新标签
            operate(lable, text)
    thread.result_ready.connect(handle_result)
    thread.start()
