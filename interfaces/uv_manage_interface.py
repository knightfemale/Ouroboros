# interfaces/uv_manage_interface.py
import platform
import subprocess
from pathlib import Path
from qfluentwidgets import LineEdit, PushButton
from typing import Any, Self, List, Dict, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout

from utils import config_util, gui_util, delay_util
from interfaces.interface import Interface
from utils.style_util import green_style, purple_style

group_style: str = purple_style.get_groupbox_style()
button_style: str = purple_style.get_button_style()
lable_style: str = purple_style.get_lable_style()

config_path: Path = config_util.config_path


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
        self.delay_variables: Dict[str, Any] = {
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
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="UV 环境管理")
        # 信息区域
        info_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "信息", style=group_style)
        info_layout: QVBoxLayout = QVBoxLayout(info_group)
        self.uv_version_label: QLabel = gui_util.LabelBuilder.create(self, info_layout, style=lable_style)
        # 操作区域
        action_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "操作", style=group_style)
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        action_btn_layout: QHBoxLayout = QHBoxLayout()
        action_layout.addLayout(action_btn_layout)
        action_btn_layout.addStretch()
        self.sync_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_btn_layout, "同步环境", slot=self.sync_env, style=button_style)
        self.save_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_btn_layout, "保存配置", slot=self.save_ui_to_config, style=button_style)
        self.activate_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_btn_layout, "激活环境", slot=self.activate_venv, style=button_style)
        self.export_pip_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_btn_layout, "导出 requirements.txt", slot=self.export_requirements, style=button_style)
        self.update_deps_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_btn_layout, "更新依赖", slot=self.update_dependencies, style=button_style)
        action_btn_layout.addStretch()
        # 环境参数区域
        env_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "环境参数", style=group_style)
        env_layout: QVBoxLayout = QVBoxLayout(env_group)
        self.python_version_input: LineEdit = gui_util.InputBuilder.create(self, env_layout, "Python 版本", "输入 Python 版本(默认: 3.10)", lable_style=lable_style)
        # 项目元数据区域
        metadata_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "项目元数据", style=group_style)
        metadata_layout: QVBoxLayout = QVBoxLayout(metadata_group)
        self.project_version_input: LineEdit = gui_util.InputBuilder.create(self, metadata_layout, "项目版本", "输入项目版本(例如: 0.0.1)", lable_style=lable_style)
        # 依赖管理区域
        pip_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "包管理", style=group_style)
        pip_layout: QVBoxLayout = QVBoxLayout(pip_group)
        self.pip_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, pip_layout, "输入包名")
        self.pip_add_btn: PushButton = gui_util.ButtonBuilder.create(self, pip_layout, "添加", slot=lambda: self.pip_container.add_row(""), style=green_style.get_button_style())
        # dev 依赖管理区域
        dev_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "开发依赖", style=group_style)
        dev_layout: QVBoxLayout = QVBoxLayout(dev_group)
        self.dev_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, dev_layout, "输入开发依赖包名")
        self.dev_add_btn: PushButton = gui_util.ButtonBuilder.create(self, dev_layout, "添加", slot=lambda: self.dev_container.add_row(""), style=green_style.get_button_style())

    def load_config_to_ui(self: Self) -> None:
        """从配置文件加载数据到 UI"""

        if config_path.exists():
            config: Dict[str, Any] = config_util.load_toml(config_path)
            # 加载项目版本
            if "project" in config and "version" in config["project"]:
                self.project_version_input.setText(config["project"]["version"])
            # 加载 Python 版本
            if "project" in config and "requires-python" in config["project"]:
                requires_python = config["project"]["requires-python"]
                # 保持原样显示
                self.python_version_input.setText(requires_python)
            # 加载普通依赖
            if "project" in config and "dependencies" in config["project"]:
                self.pip_container.set_items(config["project"]["dependencies"])
            # 加载开发依赖
            if "dependency-groups" in config and "dev" in config["dependency-groups"]:
                self.dev_container.set_items(config["dependency-groups"]["dev"])

    def sync_env(self: Self) -> None:
        """同步环境"""

        # 保存配置
        self.save_ui_to_config()
        # 执行同步命令
        gui_util.MessageDisplay.info(self, "开始同步环境")
        if platform.system() == "Windows":
            subprocess.run(f'start "UVSync" cmd /k uv sync', shell=True)
        elif platform.system() == "Linux":
            subprocess.run(f'x-terminal-emulator -e bash -c "uv sync; read"', shell=True)

    def activate_venv(self: Self) -> None:
        """激活环境"""

        gui_util.MessageDisplay.info(self, "激活环境: .venv")
        if platform.system() == "Windows":
            subprocess.run(f'start "UVActivate" cmd /k ".\\.venv\\Scripts\\activate"', shell=True)
        elif platform.system() == "Linux":
            subprocess.run(f'x-terminal-emulator -e bash -c "source ./.venv/bin/activate; read"', shell=True)

    def export_requirements(self: Self) -> None:
        """导出依赖 requirements.txt"""

        # 执行命令
        gui_util.MessageDisplay.info(self, "开始导出 requirements.txt")
        subprocess.Popen(f"uv pip freeze > ./requirements.txt", shell=True)

    def update_dependencies(self: Self) -> None:
        """更新依赖"""

        # 保存配置
        self.save_ui_to_config()
        gui_util.MessageDisplay.info(self, "开始更新依赖")
        if platform.system() == "Windows":
            subprocess.run(f'start "UVUpdate" cmd /k uv sync --upgrade', shell=True)
        elif platform.system() == "Linux":
            subprocess.run(f'x-terminal-emulator -e bash -c "uv sync --upgrade; read"', shell=True)

    def save_ui_to_config(self: Self) -> None:
        """将当前UI状态保存到配置文件"""

        if not config_path.exists():
            self.init_project()
        # 加载现有配置
        config: Dict[str, Any] = config_util.load_toml(config_path)
        # 确保 project 部分存在
        if "project" not in config:
            config["project"] = {}
        # 更新项目版本
        config["project"]["version"] = self.get_project_version()
        # 更新 Python 版本
        python_version_input = self.python_version_input.text().strip()
        if python_version_input and ("," in python_version_input or any(op in python_version_input for op in ["<", ">", "=", "~"])):
            # 如果用户输入了范围约束(包含逗号或操作符), 则保持原样
            config["project"]["requires-python"] = python_version_input
        else:
            # 否则使用默认的 >= 约束
            python_version = self.get_python_version()
            config["project"]["requires-python"] = f">={python_version}"
        # 更新普通依赖
        dependencies: List[str] = self.pip_container.get_items()
        if dependencies:
            config["project"]["dependencies"] = dependencies
        elif "dependencies" in config["project"]:
            del config["project"]["dependencies"]
        # 更新开发依赖
        dev_dependencies: List[str] = self.dev_container.get_items()
        if dev_dependencies:
            # 确保 dependency-groups 部分存在
            if "dependency-groups" not in config:
                config["dependency-groups"] = {}
            config["dependency-groups"]["dev"] = dev_dependencies
        elif "dependency-groups" in config and "dev" in config["dependency-groups"]:
            del config["dependency-groups"]["dev"]
            # 如果 dependency-groups 为空, 删除整个部分
            if not config["dependency-groups"]:
                del config["dependency-groups"]
        # 写入文件
        config_util.save_toml(config, config_path)
        self.load_config_to_ui()
        gui_util.MessageDisplay.success(self, "保存配置成功")

    def init_project(self: Self) -> None:
        """初始化 uv 配置文件"""

        base_config: Dict[str, Any] = {
            "project": {
                "name": f"{Path.cwd().name.lower()}",
            },
        }
        config_util.save_toml(base_config, config_path)
        gui_util.MessageDisplay.success(self, "uv 配置文件初始化完成")

    def get_project_version(self: Self) -> str:
        """带默认参数地获取项目版本"""

        project_version: str = self.project_version_input.text().strip()
        return project_version if project_version else "0.0.1"

    def get_python_version(self: Self) -> str:
        """带默认参数地获取 Python 版本"""

        python_version: str = self.python_version_input.text().strip()
        return python_version if python_version else "3.10"
