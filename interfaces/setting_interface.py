# interfaces/setting_interface.py
import subprocess
from pathlib import Path
from typing import Self, Optional

from qfluentwidgets import PushButton
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout

from utils import gui_util
from interfaces.interface import Interface
from utils.style_util import default_style, yellow_style, green_style, blue_style, purple_style


group_style: str = default_style.get_groupbox_style()
button_style: str = default_style.get_button_style()
lable_style: str = default_style.get_lable_style()

nuitka_group_style: str = yellow_style.get_groupbox_style()
nuitka_button_style: str = yellow_style.get_button_style()

conda_group_style: str = green_style.get_groupbox_style()
conda_button_style: str = green_style.get_button_style()

uv_group_style: str = purple_style.get_groupbox_style()
uv_button_style: str = purple_style.get_button_style()

docker_group_style: str = blue_style.get_groupbox_style()
docker_button_style: str = blue_style.get_button_style()


class SettingInterface(Interface):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("SettingInterface")
        # 初始化 UI
        self.init_ui()

    def init_ui(self: Self) -> None:
        """初始化 UI"""
        # 标题区域
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="全局设置", style="font-size: 24px; font-weight: bold; color: #333333; margin-bottom: 20px;")

        # 开发设置区域
        dev_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "开发设置", style=group_style)
        dev_layout: QVBoxLayout = QVBoxLayout(dev_group)

        # Nuitka 设置
        nuitka_group: QGroupBox = gui_util.GroupBuilder.create(self, dev_layout, "Nuitka", style=nuitka_group_style)
        nuitka_layout: QVBoxLayout = QVBoxLayout(nuitka_group)
        nuitka_btn_layout: QHBoxLayout = QHBoxLayout()
        nuitka_layout.addLayout(nuitka_btn_layout)
        nuitka_btn_layout.addStretch()
        self.clean_cache_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, nuitka_btn_layout, "清理缓存", slot=self.clean_caches, style=nuitka_button_style)
        nuitka_btn_layout.addStretch()

        # Conda 设置
        conda_group: QGroupBox = gui_util.GroupBuilder.create(self, dev_layout, "Conda", style=conda_group_style)
        conda_layout: QVBoxLayout = QVBoxLayout(conda_group)
        conda_btn_layout: QHBoxLayout = QHBoxLayout()
        conda_layout.addLayout(conda_btn_layout)
        conda_btn_layout.addStretch()
        self.clean_conda_cache_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, conda_btn_layout, "清理 conda 缓存", slot=self.clean_conda_cache, style=conda_button_style)
        self.clean_pip_cache_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, conda_btn_layout, "清理 pip 缓存", slot=self.clean_pip_cache, style=conda_button_style)
        conda_btn_layout.addStretch()

        # Docker 设置
        docker_group: QGroupBox = gui_util.GroupBuilder.create(self, dev_layout, "Docker", style=docker_group_style)
        docker_layout: QVBoxLayout = QVBoxLayout(docker_group)
        docker_btn_layout: QHBoxLayout = QHBoxLayout()
        docker_layout.addLayout(docker_btn_layout)
        docker_btn_layout.addStretch()
        self.clean_docker_cache_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, docker_btn_layout, "清理构建缓存", slot=self.clean_docker_cache, style=docker_button_style)
        docker_btn_layout.addStretch()

        # UV 设置
        uv_group: QGroupBox = gui_util.GroupBuilder.create(self, dev_layout, "UV", style=uv_group_style)
        uv_layout: QVBoxLayout = QVBoxLayout(uv_group)
        uv_btn_layout: QHBoxLayout = QHBoxLayout()
        uv_layout.addLayout(uv_btn_layout)
        uv_btn_layout.addStretch()
        self.uv_prune_cache_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, uv_btn_layout, "清理未使用缓存", slot=self.uv_prune_cache, style=uv_button_style)
        self.uv_clean_cache_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, uv_btn_layout, "清理全部缓存", slot=self.uv_clean_cache, style=uv_button_style)
        self.uv_update_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, uv_btn_layout, "更新 uv", slot=self.uv_update, style=uv_button_style)
        self.uv_upgrade_python_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, uv_btn_layout, "更新 python", slot=self.uv_upgrade_python, style=uv_button_style)
        uv_btn_layout.addStretch()

    def clean_caches(self: Self) -> None:
        """清理 Nuitka 缓存"""
        command: str = f'start "NuitkaBuild" cmd /k "{self.get_python_path()}" -m nuitka --clean-cache=all'
        gui_util.MessageDisplay.info(self, "开始清理缓存")
        subprocess.run(command, shell=True)

    def get_python_path(self: Self) -> str:
        """获取可能的 Python 解释器路径"""
        possible_paths = [
            Path.cwd() / ".venv/python.exe",
            Path.cwd() / ".venv/Scripts/python.exe",
        ]
        for path in possible_paths:
            if path.exists():
                return str(path)
        gui_util.MessageDisplay.error(self, "未找到可用解释器")
        return ""

    def clean_conda_cache(self: Self) -> None:
        """清理 conda 缓存"""
        command: str = f'start "CondaClean" cmd /k conda clean --all -y'
        gui_util.MessageDisplay.info(self, "开始清理 conda 缓存")
        subprocess.run(command, shell=True)

    def clean_pip_cache(self: Self) -> None:
        """清理 pip 缓存"""
        command: str = f'start "PipClean" cmd /k python -m pip cache purge'
        gui_util.MessageDisplay.info(self, "开始清理 pip 缓存")
        subprocess.run(command, shell=True)

    def uv_prune_cache(self: Self) -> None:
        """清理未使用缓存"""
        command: str = f'start "UVPrune" cmd /k uv cache prune'
        gui_util.MessageDisplay.info(self, "开始清理未使用缓存")
        subprocess.run(command, shell=True)

    def uv_clean_cache(self: Self) -> None:
        """清理全部缓存"""
        command: str = f'start "UVClean" cmd /k uv cache clean'
        gui_util.MessageDisplay.info(self, "开始清理全部缓存")
        subprocess.run(command, shell=True)

    def uv_update(self: Self) -> None:
        """更新 uv"""
        command: str = f'start "UVUpdate" cmd /k uv self update'
        gui_util.MessageDisplay.info(self, "开始更新 uv")
        subprocess.run(command, shell=True)

    def uv_upgrade_python(self: Self) -> None:
        """更新 python"""
        command: str = f'start "UVPythonUpgrade" cmd /k uv python upgrade --preview-features python-upgrade'
        gui_util.MessageDisplay.info(self, "开始更新 python")
        subprocess.run(command, shell=True)

    def clean_docker_cache(self: Self) -> None:
        """清理 Docker 构建缓存"""
        command: str = f'start "DockerClean" cmd /k "docker system df && docker builder prune --all --force && docker system df"'
        gui_util.MessageDisplay.info(self, "开始清理 Docker 构建缓存")
        subprocess.run(command, shell=True)
