# interfaces/home_interface.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from qfluentwidgets import PrimaryPushButton

from styles.default import ENV_BUTTON_STYLE, PACK_BUTTON_STYLE

class HomeInterface(QWidget):
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
        
        # 创建按钮容器
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter) # pyright: ignore[reportAttributeAccessIssue]
        
        # 创建环境构建跳转按钮
        self.env_button = PrimaryPushButton("环境构建工具", self)
        self.env_button.setFixedSize(180, 60)
        self.env_button.setStyleSheet(ENV_BUTTON_STYLE)
        
        # 创建打包工具跳转按钮
        self.pack_button = PrimaryPushButton("打包部署工具", self)
        self.pack_button.setFixedSize(180, 60)
        self.pack_button.setStyleSheet(PACK_BUTTON_STYLE)
        
        # 添加按钮到布局
        button_layout.addWidget(self.env_button)
        button_layout.addSpacing(40)
        button_layout.addWidget(self.pack_button)
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(40)
        layout.addLayout(button_layout)
        layout.addSpacing(30)
        
        self.setLayout(layout)
