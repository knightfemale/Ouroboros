# interfaces/help_interface.py
from PySide6.QtCore import Qt
from typing import Self, Optional
from qfluentwidgets import HyperlinkButton
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from utils.style_util import TITLE_STYLE


class HelpInterface(QWidget):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("HelpInterface")
        # 初始化 UI
        self.init_ui()

    def init_ui(self: Self) -> None:
        """初始化 UI"""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # pyright: ignore[reportAttributeAccessIssue]
        # 标题
        title: QLabel = QLabel("帮助与支持", self)
        title.setStyleSheet(TITLE_STYLE)
        # 仓库链接跳转按钮
        gitee_btn: HyperlinkButton = HyperlinkButton(
            "https://gitee.com/qishiji/Ouroboros",
            "gitee 仓库",
            self,
        )
        github_btn: HyperlinkButton = HyperlinkButton(
            "https://github.com/knightfemale/Ouroboros",
            "GitHub 仓库",
            self,
        )
        # 加入到布局
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(gitee_btn)
        layout.addWidget(github_btn)
        self.setLayout(layout)
