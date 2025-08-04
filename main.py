# main.py
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon

# 导入自定义页面
from interfaces.home_interface import HomeInterface
from interfaces.help_interface import HelpInterface
from interfaces.nuitka_packaging_interface import NuitkaPackagingInterface
from interfaces.environment_build_interface import EnvironmentBuildInterface

class MainWindow(FluentWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ouroboros")
        self.resize(1280, 720)
        
        # 创建子界面实例
        self.homeInterface = HomeInterface(self)
        self.environmentBuildInterface = EnvironmentBuildInterface(self)
        self.nuitkaPackagingInterface = NuitkaPackagingInterface(self)
        self.helpInterface = HelpInterface(self)
        
        # 添加导航项
        self.add_navigation_items()

    def create_interface(self, text, object_name) -> QWidget:
        """创建并初始化一个界面"""
        interface = QWidget()
        interface.setObjectName(object_name)
        
        layout = QVBoxLayout(interface)
        label = QLabel(text, interface)
        label.setAlignment(Qt.AlignCenter) # pyright: ignore[reportAttributeAccessIssue]
        label.setStyleSheet("font-size: 30px; color: #666666;")
        layout.addWidget(label)
        
        return interface

    def add_navigation_items(self) -> None:
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
