# interfaces/home_interface.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from qfluentwidgets import PrimaryPushButton

from interfaces.interface import Interface
from styles.default import red_style, green_style

class HomeInterface(Interface):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName("HomeInterface")
        self.init_ui()
    
    def init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter) # pyright: ignore[reportAttributeAccessIssue]
        title = QLabel("Ouroboros - Python 项目自动化工具", self)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #666666;")
        description = QLabel("一站式解决方案: 环境构建、打包部署、性能优化", self)
        description.setStyleSheet("font-size: 18px; color: #666666;")
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter) # pyright: ignore[reportAttributeAccessIssue]
        self.pack_button = PrimaryPushButton("Nuitka 编译打包", self)
        self.pack_button.setFixedSize(180, 60)
        self.pack_button.setStyleSheet(red_style.get_button_style())
        self.env_button = PrimaryPushButton("Conda 环境管理", self)
        self.env_button.setFixedSize(180, 60)
        self.env_button.setStyleSheet(green_style.get_button_style())
        # 添加到布局
        button_layout.addWidget(self.pack_button)
        button_layout.addSpacing(40)
        button_layout.addWidget(self.env_button)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(40)
        layout.addLayout(button_layout)
        layout.addSpacing(30)
        self.setLayout(layout)
