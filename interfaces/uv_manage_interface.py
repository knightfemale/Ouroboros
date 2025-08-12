# interfaces/uv_manage_interface.py
import toml
import subprocess
from pathlib import Path
from typing import Any, Self, Dict, Optional
from qfluentwidgets import LineEdit, PushButton
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox

from utils import gui_util, delay_util
from interfaces.interface import Interface
from utils.style_util import green_style, purple_style

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
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="UV 环境构建")
        # 信息区域
        info_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "信息", style=group_style)
        info_layout: QVBoxLayout = QVBoxLayout(info_group)
        self.uv_version_label: QLabel = gui_util.LabelBuilder.create(self, info_layout, style=lable_style)
        # 操作区域
        action_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "操作", style=group_style)
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        self.sync_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_layout, "同步环境", slot=self.sync_env, style=button_style)
        self.save_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_layout, "保存配置", slot=self.save_ui_to_config, style=button_style)
        self.activate_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_layout, "激活环境", slot=self.activate_venv, style=button_style)
        # 环境参数区域
        env_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "环境参数", style=group_style)
        env_layout: QVBoxLayout = QVBoxLayout(env_group)
        self.python_version_input: LineEdit = gui_util.InputBuilder.create(self, env_layout, "Python 版本", "输入 Python 版本(默认: 3.10)", lable_style=lable_style)
        # 项目元数据区域
        metadata_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "项目元数据", style=group_style)
        metadata_layout: QVBoxLayout = QVBoxLayout(metadata_group)
        self.project_version_input: LineEdit = gui_util.InputBuilder.create(self, metadata_layout, "项目版本", "输入项目版本(例如: 0.1.0)", lable_style=lable_style)
        # pip 包管理区域
        pip_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "包管理", style=group_style)
        pip_layout: QVBoxLayout = QVBoxLayout(pip_group)
        self.pip_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, pip_layout, "输入包名")
        self.pip_add_btn: PushButton = gui_util.ButtonBuilder.create(self, pip_layout, "添加", slot=lambda: self.pip_container.add_row(""), style=green_style.get_button_style())
    
    def load_config_to_ui(self: Self) -> None:
        """从配置文件加载数据到 UI"""
        pyproject_path: Path = Path("./pyproject.toml")
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    pyproject = toml.load(f)
                    # 加载项目版本
                    if "project" in pyproject and "version" in pyproject["project"]:
                        self.project_version_input.setText(pyproject["project"]["version"])
                    # 加载项目版本
                    if "project" in pyproject and "requires-python" in pyproject["project"]:
                        self.python_version_input.setText(pyproject["project"]["requires-python"][2:])
                    # 加载依赖
                    if "project" in pyproject and "dependencies" in pyproject["project"]:
                        self.pip_container.set_items(pyproject["project"]["dependencies"])
            except Exception as e:
                gui_util.MessageDisplay.error(self, f"加载配置失败: {str(e)}")
    
    def sync_env(self: Self) -> None:
        """同步环境"""
        # 保存配置
        self.save_ui_to_config()
        # 执行同步命令
        gui_util.MessageDisplay.info(self, "开始同步环境")
        subprocess.run(f"start \"UVSync\" cmd /k uv sync", shell=True)
    
    def save_ui_to_config(self: Self) -> None:
        """将当前UI状态保存到配置文件"""
        config_path: Path = Path("./pyproject.toml")
        if not config_path.exists():
            self.init_project()
        config = {}
        # 加载现有配置
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = toml.load(f)
        except Exception as e:
            gui_util.MessageDisplay.error(self, f"读取配置失败: {str(e)}")
            return
        # 更新项目版本
        config["project"]["version"] = self.get_project_version()
        # 更新 Python 版本
        config["project"]["requires-python"] = f">={self.get_python_version()}"
        # 更新依赖
        dependencies = self.pip_container.get_items()
        if dependencies:
            config["project"]["dependencies"] = dependencies
        elif "dependencies" in config["project"]:
            del config["project"]["dependencies"]
        # 写入文件
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                toml.dump(config, f)
            gui_util.MessageDisplay.success(self, "保存配置成功")
        except Exception as e:
            gui_util.MessageDisplay.error(self, f"保存配置失败: {str(e)}")
    
    def activate_venv(self: Self) -> None:
        """激活环境"""
        gui_util.MessageDisplay.info(self, "激活环境: .venv")
        subprocess.run(
            f'start ".venv" cmd /k call activate ./.venv', 
            shell=True
        )
    
    def init_project(self: Self) -> None:
        """初始化 uv 配置文件"""
        config_path: Path = Path("./pyproject.toml")
        base_config = {
            "project": {
                "name": f"{Path.cwd().name.lower()}",
            },
        }
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                toml.dump(base_config, f)
            self.load_config_to_ui()
            gui_util.MessageDisplay.success(self, "uv 配置文件初始化完成")
        except Exception as e:
            gui_util.MessageDisplay.error(self, f"uv 配置文件初始化失败: {str(e)}")
    
    def get_project_version(self: Self) -> str:
        """带默认参数地获取 Python 版本"""
        project_version: str = self.project_version_input.text().strip()
        return project_version if project_version else '0.1.0'
    
    def get_python_version(self: Self) -> str:
        """带默认参数地获取 Python 版本"""
        python_version: str = self.python_version_input.text().strip()
        return python_version if python_version else '3.10'
