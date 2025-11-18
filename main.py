# main.py
import sys
from typing import Self
from pathlib import Path
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon

# 导入自定义页面
from interfaces.home_interface import HomeInterface
from interfaces.nuitka_build_interface import NuitkaBuildInterface
from interfaces.conda_manage_interface import CondaManageInterface
from interfaces.uv_manage_interface import UVManageInterface
from interfaces.help_interface import HelpInterface

from resources import icon
from utils import icon_util


class MainWindow(FluentWindow):
    def __init__(self: Self) -> None:
        super().__init__()
        # 创建窗口
        self.setWindowTitle(f"Ouroboros-{Path.cwd().name}")
        self.resize(1280, 720)
        # 创建子界面实例
        self.homeInterface: HomeInterface = HomeInterface(self)
        self.nuitka_build_interface: NuitkaBuildInterface = NuitkaBuildInterface(self)
        self.conda_manage_interface: CondaManageInterface = CondaManageInterface(self)
        self.uv_manage_interface = UVManageInterface(self)
        self.helpInterface: HelpInterface = HelpInterface(self)
        # 添加导航项
        self.add_navigation_items()
        # 连接首页按钮信号
        self.homeInterface.pack_button.clicked.connect(lambda: self.switchTo(self.nuitka_build_interface))
        self.homeInterface.env_button.clicked.connect(lambda: self.switchTo(self.conda_manage_interface))
        self.homeInterface.uv_button.clicked.connect(lambda: self.switchTo(self.uv_manage_interface))

    def add_navigation_items(self: Self) -> None:
        # 添加主导航项
        self.addSubInterface(
            self.homeInterface,
            FluentIcon.HOME,
            "首页",
        )
        self.addSubInterface(
            self.nuitka_build_interface,
            icon_util.FluentIcon.NUITKA,
            "Nuitka 编译打包",
        )
        self.addSubInterface(
            self.conda_manage_interface,
            icon_util.FluentIcon.CONDA,
            "Conda 环境管理",
        )
        self.addSubInterface(
            self.uv_manage_interface,
            icon_util.FluentIcon.UV,
            "UV 环境管理",
        )
        # 添加底部导航
        self.addSubInterface(
            self.helpInterface,
            FluentIcon.HELP,
            "帮助与支持",
            position=NavigationItemPosition.BOTTOM,
        )
        # 默认选中首页
        self.switchTo(self.homeInterface)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
