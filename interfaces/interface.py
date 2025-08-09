# interfaces/interface.py
from PySide6.QtWidgets import QWidget
from typing import Any, Self, Dict, Optional

from utils import delay_util

class Interface(QWidget):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 延时变量
        self.delay_variables: Dict[str, Dict[str, Any]] = {}
    
    def showEvent(self: Self, event: Any) -> None:
        """当界面显示时触发"""
        super().showEvent(event)
        for key, value in self.delay_variables.items():
            delay_util.set_delay_lable(self, key, value["label"], value["command"], value["prefix"], value["err"], value["operate"])
