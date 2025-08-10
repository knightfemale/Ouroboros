# interfaces/conda_manage_interface.py
import subprocess
from typing import Any, Self, List, Dict, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox

from utils import config_util, gui_util
from interfaces.interface import Interface
from utils.style_util import green_style

group_style: str = green_style.get_groupbox_style()
button_style: str = green_style.get_button_style()
lable_style: str = green_style.get_lable_style()

class CondaManageInterface(Interface):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("EnvironmentBuildInterface")
        # 初始化 UI
        self.init_ui()
        # 加载配置到 UI
        self.load_config_to_ui()
        # 全局变量
        self.conda_version: str = ""
        # 延时变量
        self.delay_variables = {
            "conda_version": {
                "label": self.conda_version_label,
                "command": ["conda", "--version"],
                "prefix": "Conda Version: ",
                "err": "未找到, 请确保 Conda 已安装",
                "operate": self.conda_operate,
            },
        }
    
    def conda_operate(self, lable: QLabel, text: str) -> None:
        """设置 Conda 版本的标签方式"""
        lable.setText(text.replace("conda ", ""))
    
    def init_ui(self: Self) -> None:
        """初始化 UI"""
        # 标题区域
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="Conda 环境构建")
        # 信息区域
        info_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "信息", style=group_style)
        info_layout: QVBoxLayout = QVBoxLayout(info_group)
        self.conda_version_label: QLabel = gui_util.LabelBuilder.create(self, info_layout, style=lable_style)
        # 操作区域
        action_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "操作", style=group_style)
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        self.build_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "构建环境", slot=self.build_env, style=button_style)
        self.save_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "保存配置", slot=self.save_ui_to_config, style=button_style)
        self.activate_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "激活环境", slot=self.activate_venv, style=button_style)
        self.export_pip_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "导出依赖 requirements.txt", slot=self.export_requirements, style=button_style)
        self.export_conda_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "导出依赖 environment.yml", slot=self.export_environment, style=button_style)
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
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, pip_layout, "添加", slot=lambda: self.pip_container.add_row(""), style=green_style.get_button_style())
        # conda 包管理区域
        conda_group: QGroupBox = gui_util.GroupBuilder.create(self, env_layout, "conda 包管理", style=group_style)
        conda_layout: QVBoxLayout = QVBoxLayout(conda_group)
        self.conda_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, conda_layout, "输入 conda 包名")
        self.conda_add_btn = gui_util.ButtonBuilder.create(self, conda_layout, "添加", slot=lambda: self.conda_container.add_row(""), style=green_style.get_button_style())
    
    def load_config_to_ui(self: Self) -> None:
        """从配置文件加载数据到 UI"""
        # 加载配置
        config: Dict[str, Any] = config_util.load_config()
        # 设置环境名称
        env_name: str = config.get('name', '.venv')
        self.env_name_input.setText(env_name)
        # 设置 Python 版本
        python_version: str = ""
        for dep in config.get('dependencies', []):
            if isinstance(dep, str) and dep.startswith('python='):
                python_version: str = dep.split('=')[1]
                break
        if python_version:
            self.python_version_input.setText(python_version)
        # 添加 conda 包
        conda_packages: Any = []
        for dep in config.get('dependencies', []):
            if isinstance(dep, str) and not dep.startswith('python='):
                conda_packages.append(dep)
        self.conda_container.set_items(conda_packages)
        # 添加 pip 包
        pip_packages: List[str] = []
        for dep in config.get('dependencies', []):
            if isinstance(dep, dict) and 'pip' in dep:
                for pip_dep in dep['pip']:
                    pip_packages.append(pip_dep)
        self.pip_container.set_items(pip_packages)
    
    def save_ui_to_config(self: Self) -> None:
        """将当前UI状态保存到配置文件"""
        # 先加载完整配置
        full_config: Dict[str, Any] = config_util.load_config()
        # 只更新环境构建部分
        full_config.update({
            "name": self.get_env_name(),
            "dependencies": self.collect_dependencies()
        })
        config_util.save_config(full_config)
        gui_util.MessageDisplay.success(self, "保存配置成功")
    
    def collect_dependencies(self) -> list:
        """收集所有依赖项"""
        deps: List[Any] = [f"python={self.get_python_version()}"]
        # 添加conda包
        deps.extend(self.conda_container.get_items())
        # 添加pip包
        pip_packages = self.pip_container.get_items()
        if pip_packages:
            deps.append({"pip": pip_packages})
        return deps
    
    def build_env(self: Self) -> None:
        """构建环境"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 保存到配置
        self.save_ui_to_config()
        # 执行命令
        gui_util.MessageDisplay.info(self, "开始环境构建")
        subprocess.run(f"start \"CondaBuild\" cmd /k conda env create --file {config_util.config_path} --prefix ./{env_name}", shell=True)
    
    def activate_venv(self: Self) -> None:
        """激活环境"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 执行命令
        gui_util.MessageDisplay.info(self, f"激活环境: {env_name}")
        subprocess.run(f"start \"{env_name}\" cmd /k call activate ./{env_name}", shell=True)
    
    def export_requirements(self: Self) -> None:
        """导出依赖 requirements.txt"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 执行命令
        gui_util.MessageDisplay.info(self, "开始导出 requirements.txt")
        subprocess.Popen(f"\"./{env_name}/python\" -m pip freeze > ./requirements.txt", shell=True)
    
    def export_environment(self: Self) -> None:
        """导出依赖 environment.yml"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 执行命令
        gui_util.MessageDisplay.info(self, "开始导出 environment.yml")
        subprocess.Popen(f"conda env export -p ./{env_name} > ./environment.yml", shell=True)
    
    def get_env_name(self: Self) -> str:
        """带默认参数地获取环境名"""
        env_name: str = self.env_name_input.text().strip()
        return env_name if env_name else '.venv'
    
    def get_python_version(self: Self) -> str:
        """带默认参数地获取 Python 版本"""
        python_version: str = self.python_version_input.text().strip()
        return python_version if python_version else '3.10'
