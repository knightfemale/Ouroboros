# utils/delay_util.py
import subprocess
from PySide6.QtCore import QThread, Signal
from typing import List, Callable, Optional
from PySide6.QtWidgets import QWidget, QLabel

class DelayLabelThread(QThread):
    # 信号: 标签, 结果文本
    operate = Signal(QLabel, str)
    
    def __init__(
        self,
        interface: Optional[QWidget],
        var_name: str,
        lable: QLabel,
        command: List[str],
        prefix: str,
        err: str
    ) -> None:
        super().__init__(interface)
        self.interface = interface
        self.var_name = var_name
        self.lable = lable
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
                text = f"{self.prefix}{stdout.strip()}"
                setattr(self.interface, self.var_name, text)
                self.operate.emit(self.lable, text)
            else:
                text = stderr.strip() or "Unknown error"
                self.operate.emit(self.lable, f"{self.prefix}{self.err}: {text}")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            self.operate.emit(self.lable, f"{self.prefix}{self.err}: {str(e)}")

def set_delay_lable(
    interface: QWidget,
    var_name: str,
    lable: QLabel,
    command: List[str],
    prefix: str,
    err: str,
    operate: Callable[[QLabel, str], None],
) -> None:
    """设置延时标签"""
    # 如果已有缓存值, 直接使用
    if hasattr(interface, var_name) and getattr(interface, var_name):
        operate(lable, getattr(interface, var_name))
        return
    # 创建并启动后台线程
    thread = DelayLabelThread(interface, var_name, lable, command, prefix, err)
    # 连接信号
    thread.operate.connect(operate)
    # 启动线程
    thread.start()

def label_operate(lable: QLabel, text: str) -> None:
    """默认的设置标签方式"""
    lable.setText(text)