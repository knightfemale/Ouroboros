# main.py
import sys
from typing import Self
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon

# 导入自定义页面
from interfaces.home_interface import HomeInterface
from interfaces.help_interface import HelpInterface
from interfaces.nuitka_packaging_interface import NuitkaPackagingInterface
from interfaces.environment_build_interface import EnvironmentBuildInterface

class MainWindow(FluentWindow):
    def __init__(self: Self) -> None:
        super().__init__()
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
    
    def add_navigation_items(self: Self) -> None:
        # 添加主导航项
        self.addSubInterface(
            self.homeInterface,
            FluentIcon.HOME,
            "首页",
        )
        self.addSubInterface(
            self.nuitkaPackagingInterface,
            FluentIcon.ZIP_FOLDER,
            "Nuitka 编译打包",
        )
        self.addSubInterface(
            self.environmentBuildInterface,
            FluentIcon.DEVELOPER_TOOLS,
            "Conda 环境管理",
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
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
