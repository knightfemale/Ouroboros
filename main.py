# main.py
import os
import sys
from typing import Self
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon

from utils import config_util

# 导入自定义页面
from interfaces.home_interface import HomeInterface
from interfaces.help_interface import HelpInterface
from interfaces.nuitka_packaging_interface import NuitkaPackagingInterface
from interfaces.environment_build_interface import EnvironmentBuildInterface

class MainWindow(FluentWindow):
    def __init__(self: Self) -> None:
        super().__init__()
        # 检查并创建默认配置文件
        self.ensure_default_config()
        # 创建窗口
        self.setWindowTitle("Ouroboros")
        self.resize(1280, 720)
        # 创建子界面实例
        self.homeInterface: HomeInterface = HomeInterface(self)
        self.environmentBuildInterface: EnvironmentBuildInterface = EnvironmentBuildInterface(self)
        self.nuitkaPackagingInterface: NuitkaPackagingInterface = NuitkaPackagingInterface(self)
        self.helpInterface: HelpInterface = HelpInterface(self)
        # 添加导航项
        self.add_navigation_items()
        # 连接首页按钮信号
        self.homeInterface.env_button.clicked.connect(lambda: self.switchTo(self.environmentBuildInterface))
        self.homeInterface.pack_button.clicked.connect(lambda: self.switchTo(self.nuitkaPackagingInterface))
    
    def create_interface(self: Self, text: str, object_name: str) -> QWidget:
        """创建并初始化一个界面"""
        interface: QWidget = QWidget()
        interface.setObjectName(object_name)
        layout: QVBoxLayout = QVBoxLayout(interface)
        label: QLabel = QLabel(text, interface)
        label.setAlignment(Qt.AlignCenter) # pyright: ignore[reportAttributeAccessIssue]
        label.setStyleSheet("font-size: 30px; color: #666666;")
        layout.addWidget(label)
        
        return interface
    
    def add_navigation_items(self: Self) -> None:
        # 添加主导航项
        self.addSubInterface(
            self.homeInterface,
            FluentIcon.HOME,
            "首页",
        )
        self.addSubInterface(
            self.environmentBuildInterface,
            FluentIcon.DEVELOPER_TOOLS,
            "环境构建",
        )
        self.addSubInterface(
            self.nuitkaPackagingInterface,
            FluentIcon.ZIP_FOLDER,
            "Nuitka 打包",
        )
        # 添加分隔线
        self.navigationInterface.addSeparator()
        # 添加帮助项(放在底部)
        self.addSubInterface(
            self.helpInterface, 
            FluentIcon.HELP, 
            "帮助与支持",
            position=NavigationItemPosition.BOTTOM,
        )
        # 默认选中首页
        self.switchTo(self.homeInterface)
    
    def ensure_default_config(self: Self) -> None:
        """确保配置文件存在"""
        if not os.path.exists("ouroboros.yml"):
            config_util.save_config({
                "name": "",
                "dependencies": [
                    {"pip": []},
                ],
            })

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
