# interfaces/home_interface.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

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
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(30)
        
        self.setLayout(layout)
