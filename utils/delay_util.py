# utils/delay_util.py
import subprocess
from typing import Dict, Optional
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QLabel

class DelayThread(QThread):
    # 信号: 标签, 结果文本
    operate = Signal(object, str)
    
    def __init__(self, interface: Optional[QWidget], details: dict) -> None:
        super().__init__(interface)
        self.interface = interface
        self.details = details
    
    def run(self) -> None:
        try:
            process = subprocess.Popen(
                self.details["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
                text=True,
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                text = f"{self.details["prefix"]}{stdout.strip()}"
                self.details["var"] = text
                self.operate.emit(self.details["object"], text)
            else:
                text = stderr.strip() or "Unknown error"
                self.operate.emit(self.details["object"], f"{self.details["prefix"]}{self.details["err"]}: {text}")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            self.operate.emit(self.details["object"], f"{self.details["prefix"]}{self.details["err"]}: {str(e)}")

def set_delay_var(interface: QWidget, details: Dict) -> None:
    """设置延时标签"""
    # 如果已有缓存值, 直接使用
    if details["var"]:
        details["operate"](details["object"], details["var"])
        return
    else:
        details["operate"](details["object"], f"{details["prefix"]}正在获取...")
    # 创建并启动后台线程
    thread = DelayThread(interface, details)
    # 连接信号
    thread.operate.connect(details["operate"])
    # 启动线程
    thread.start()

def set_label_text(lable: QLabel, text: str) -> None:
    """默认的设置标签方式"""
    lable.setText(text)
