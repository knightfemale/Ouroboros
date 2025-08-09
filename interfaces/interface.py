# interfaces/interface.py
from PySide6.QtCore import Qt
from typing import Any, Self, Dict, Optional
from qfluentwidgets import SingleDirectionScrollArea
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame

from utils import delay_util
from styles.default import BACKGROUND_STYLE

class Interface(QWidget):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 创建内容容器与主区域
        self.content_widget: QWidget = QWidget()
        self.main_layout: QVBoxLayout = QVBoxLayout(self.content_widget)
        self.main_layout.setAlignment(Qt.AlignTop) # pyright: ignore[reportAttributeAccessIssue]
        # 创建主滚动区域
        scroll_area = SingleDirectionScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame) # pyright: ignore[reportAttributeAccessIssue]
        scroll_area.setStyleSheet(BACKGROUND_STYLE)
        scroll_area.setWidget(self.content_widget)
        # 设置主布局为滚动区域
        self.outer_layout: QVBoxLayout = QVBoxLayout(self)
        self.outer_layout.addWidget(scroll_area)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.outer_layout)
        # 延时变量
        self.delay_variables: Dict[str, Dict[str, Any]] = {}
    
    def showEvent(self: Self, event: Any) -> None:
        """当界面显示时触发"""
        super().showEvent(event)
        for key, value in self.delay_variables.items():
            delay_util.set_delay_lable(self, key, value["label"], value["command"], value["prefix"], value["err"], value["operate"])
