# interfaces/uv_manage_interface.py
import subprocess
from pathlib import Path
from typing import Any, Self, List, Dict, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox

from utils.style_util import purple_style
from interfaces.interface import Interface
from utils import config_util, gui_util, delay_util

group_style: str = purple_style.get_groupbox_style()
button_style: str = purple_style.get_button_style()
lable_style: str = purple_style.get_lable_style()

class UVManageInterface(Interface):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("UVManageInterface")
        # 初始化 UI
        self.init_ui()
        # 加载配置到 UI
        self.load_config_to_ui()
        # 延时变量
        self.delay_variables = {
            "uv_version": {
                "var": None,
                "object": self.uv_version_label,
                "command": ["uv", "--version"],
                "prefix": "UV Version: ",
                "err": "未找到, 请确保 uv 已安装",
                "operate": delay_util.set_label_text,
            },
        }
    
    def init_ui(self: Self) -> None:
        """初始化 UI"""
        # 标题区域
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="UV 环境构建")
        # 信息区域
        info_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "信息", style=group_style)
        info_layout: QVBoxLayout = QVBoxLayout(info_group)
        self.uv_version_label: QLabel = gui_util.LabelBuilder.create(self, info_layout, style=lable_style)
        # 操作区域
        action_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "操作", style=group_style)
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        self.export_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "初始化项目", slot=self.init_project, style=button_style)
        self.build_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "同步环境", slot=self.sync_env, style=button_style)
        self.save_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "保存配置", slot=self.save_ui_to_config, style=button_style)
        self.activate_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "激活环境", slot=self.activate_venv, style=button_style)
        # 环境参数区域
        env_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "环境参数", style=group_style)
        env_layout: QVBoxLayout = QVBoxLayout(env_group)
        # 环境名称和版本
        self.env_name_input = gui_util.InputBuilder.create(self, env_layout, "环境名称", "输入环境名称(默认: .venv)", lable_style=lable_style)
        self.python_version_input = gui_util.InputBuilder.create(self, env_layout, "Python 版本", "输入 Python 版本(默认: 3.10)", lable_style=lable_style)
        # pip 包管理区域
        pip_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "pip 包管理", style=group_style)
        pip_layout: QVBoxLayout = QVBoxLayout(pip_group)
        self.pip_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, pip_layout, "输入 pip 包名")
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, pip_layout, "添加", slot=lambda: self.pip_container.add_row(""), style=button_style)
    
    def load_config_to_ui(self: Self) -> None:
        """从配置文件加载数据到 UI"""
    
    def save_ui_to_config(self: Self) -> None:
        """将当前UI状态保存到配置文件"""
    
    def init_project(self: Self) -> None:
        """初始化项目"""
    
    def sync_env(self: Self) -> None:
        """同步环境"""
    
    def activate_venv(self: Self) -> None:
        """激活环境"""
    
    def get_env_name(self: Self) -> str:
        """带默认参数地获取环境名"""
        env_name: str = self.env_name_input.text().strip()
        return env_name if env_name else '.venv'
    
    def get_python_version(self: Self) -> str:
        """带默认参数地获取 Python 版本"""
        python_version: str = self.python_version_input.text().strip()
        return python_version if python_version else '3.10'
