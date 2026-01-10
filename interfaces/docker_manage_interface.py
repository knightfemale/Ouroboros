# interfaces/docker_manage_interface.py
from pathlib import Path
from typing import Any, Self, Dict, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox

from utils.style_util import blue_style
from interfaces.interface import Interface
from utils import config_util, gui_util, delay_util


group_style: str = blue_style.get_groupbox_style()
button_style: str = blue_style.get_button_style()
lable_style: str = blue_style.get_lable_style()

config_path: Path = config_util.config_path


class DockerManageInterface(Interface):

    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("DockerManageInterface")
        # 初始化 UI
        self.init_ui()
        # 延时变量
        self.delay_variables: Dict[str, Any] = {
            "docker_version": {
                "var": None,
                "object": self.docker_version_label,
                "command": ["docker", "--version"],
                "prefix": "Docker Version: ",
                "err": "未找到, 请确保 Docker 已安装",
                "operate": delay_util.set_label_text,
            },
        }

    def init_ui(self: Self) -> None:
        """初始化 UI"""

        # 标题区域
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="Docker 管理")
        # 信息区域
        info_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "信息", style=group_style)
        info_layout: QVBoxLayout = QVBoxLayout(info_group)
        self.docker_version_label: QLabel = gui_util.LabelBuilder.create(self, info_layout, style=lable_style)
