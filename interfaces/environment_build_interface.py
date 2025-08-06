# interfaces/environment_build_interface.py
import subprocess
from PySide6.QtCore import Qt
from pathlib import Path
from typing import Any, Self, List, Dict, Optional
from PySide6.QtWidgets import QWidget, QLayout, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QFrame, QLayoutItem
from qfluentwidgets import PrimaryPushButton, LineEdit, InfoBar, InfoBarPosition, PushButton, SingleDirectionScrollArea

from utils import config_util
from styles.default import red_style, green_style, indigo_style, BACKGROUND_STYLE, TITLE_STYLE

class EnvironmentBuildInterface(QWidget):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("EnvironmentBuildInterface")
        # 初始化 UI
        self.init_ui()
        # 加载配置到 UI
        self.load_config_to_ui()
    
    def init_ui(self: Self) -> None:
        # 创建主滚动区域
        scroll_area: SingleDirectionScrollArea = SingleDirectionScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame) # pyright: ignore[reportAttributeAccessIssue]
        # 改为白色背景
        scroll_area.setStyleSheet(BACKGROUND_STYLE)
        # 创建内容容器
        content_widget: QWidget = QWidget()
        main_layout: QVBoxLayout = QVBoxLayout(content_widget)
        main_layout.setAlignment(Qt.AlignTop) # pyright: ignore[reportAttributeAccessIssue]
        # 标题
        title: QLabel = QLabel("环境构建工具", content_widget)
        title.setStyleSheet(TITLE_STYLE)
        # 环境构建区域
        env_group: QGroupBox = QGroupBox("环境构建", self)
        env_group.setStyleSheet(indigo_style.get_groupbox_style())
        env_layout: QVBoxLayout = QVBoxLayout(env_group)
        # 环境名称标签和输入框
        env_name_layout: QHBoxLayout = QHBoxLayout()
        self.env_name_input: LineEdit = LineEdit(self)
        self.env_name_input.setPlaceholderText("输入环境名称: (默认 .venv)")
        env_name_layout.addWidget(self.env_name_input)
        env_layout.addLayout(env_name_layout)
        # Python 版本标签和输入框
        python_version_layout: QHBoxLayout = QHBoxLayout()
        self.python_version_input: LineEdit = LineEdit(self)
        self.python_version_input.setPlaceholderText("输入 Python 版本: (默认 3.10)")
        python_version_layout.addWidget(self.python_version_input)
        env_layout.addLayout(python_version_layout)
        # pip 包管理
        pip_group: QGroupBox = QGroupBox("pip 包管理", self)
        pip_group.setStyleSheet(indigo_style.get_groupbox_style())
        pip_layout: QVBoxLayout = QVBoxLayout(pip_group)
        # 添加一个容器用于存放动态添加的输入框
        self.pip_inputs_container = QVBoxLayout()
        pip_layout.addLayout(self.pip_inputs_container)
        # 添加按钮布局
        pip_btn_layout: QHBoxLayout = QHBoxLayout()
        self.pip_add_btn: PushButton = PushButton("添加", self)
        self.pip_add_btn.setStyleSheet(green_style.get_button_style())
        self.pip_add_btn.setFixedWidth(100)
        self.pip_add_btn.clicked.connect(self.add_pip_input_row)
        pip_btn_layout.addWidget(self.pip_add_btn)
        pip_layout.addLayout(pip_btn_layout)
        env_layout.addWidget(pip_group)
        # conda 包管理
        conda_group: QGroupBox = QGroupBox("conda 包管理", self)
        conda_group.setStyleSheet(indigo_style.get_groupbox_style())
        conda_layout: QVBoxLayout = QVBoxLayout(conda_group)
        # 添加容器
        self.conda_inputs_container: QVBoxLayout = QVBoxLayout()
        conda_layout.addLayout(self.conda_inputs_container)
        # 添加按钮布局
        conda_btn_layout: QHBoxLayout = QHBoxLayout()
        self.conda_add_btn: PushButton = PushButton("添加", self)
        self.conda_add_btn.setStyleSheet(green_style.get_button_style())
        self.conda_add_btn.setFixedWidth(100)
        self.conda_add_btn.clicked.connect(self.add_conda_input_row)
        conda_btn_layout.addWidget(self.conda_add_btn)
        conda_layout.addLayout(conda_btn_layout)
        env_layout.addWidget(conda_group)
        # 操作按钮区域
        action_group: QGroupBox = QGroupBox("操作", conda_group)
        action_group.setStyleSheet(indigo_style.get_groupbox_style())
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        # 构建环境
        self.build_btn: PrimaryPushButton = PrimaryPushButton("构建环境", self)
        self.build_btn.setStyleSheet(indigo_style.get_button_style())
        self.build_btn.setMinimumHeight(40)
        self.build_btn.clicked.connect(self.build_env)
        action_layout.addWidget(self.build_btn)
        # 激活环境
        self.activate_btn: PrimaryPushButton = PrimaryPushButton("激活环境", self)
        self.activate_btn.setStyleSheet(indigo_style.get_button_style())
        self.activate_btn.setMinimumHeight(40)
        self.activate_btn.clicked.connect(self.activate_venv)
        action_layout.addWidget(self.activate_btn)
        # 导出依赖 requirements.txt
        self.export_req_btn: PrimaryPushButton = PrimaryPushButton("导出依赖 requirements.txt", self)
        self.export_req_btn.setStyleSheet(indigo_style.get_button_style())
        self.export_req_btn.setMinimumHeight(40)
        self.export_req_btn.clicked.connect(self.export_requirements)
        action_layout.addWidget(self.export_req_btn)
        # 导出依赖 environment.yml
        self.export_yml_btn: PrimaryPushButton = PrimaryPushButton("导出依赖 environment.yml", self)
        self.export_yml_btn.setStyleSheet(indigo_style.get_button_style())
        self.export_yml_btn.setMinimumHeight(40)
        self.export_yml_btn.clicked.connect(self.export_environment)
        action_layout.addWidget(self.export_yml_btn)
        # 添加到主布局
        main_layout.addWidget(title)
        main_layout.addWidget(env_group)
        main_layout.addWidget(action_group)
        # 将内容容器设置到滚动区域
        scroll_area.setWidget(content_widget)
        # 设置主布局为滚动区域
        outer_layout: QVBoxLayout = QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(outer_layout)
    
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
        # 清空现有输入框
        self.clear_all_inputs()
        # 添加 conda 包
        for dep in config.get('dependencies', []):
            if isinstance(dep, str) and not dep.startswith('python='):
                self.add_conda_input_row(dep)
        # 添加 pip 包
        for dep in config.get('dependencies', []):
            if isinstance(dep, dict) and 'pip' in dep:
                for pip_dep in dep['pip']:
                    self.add_pip_input_row(pip_dep)

    def build_env(self: Self) -> None:
        """构建环境"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 保存到配置
        self.save_ui_to_config()
        # 执行命令
        command: str = f"conda env create -f {config_util.config_path} --prefix ./{env_name}"
        process: subprocess.Popen = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # 后台输出
        print("开始创建环境!\n")
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        # 等待命令执行完成
        process.wait()
        # 创建 .gitignore 文件
        try:
            gitignore_path: Path = Path(f"./{env_name}/.gitignore")
            with open(gitignore_path, "w") as f:
                f.write("*")
            print(f"✅ 已创建 .gitignore 文件: {gitignore_path}!\n")
        except Exception as e:
            print(f"❌ 创建 .gitignore 文件失败: {str(e)}!\n")
        # 保存到配置
        self.save_ui_to_config()
        # 前台输出
        self.show_success("环境构建完成!")
    
    def activate_venv(self: Self) -> None:
        """激活环境"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 执行命令
        subprocess.run(
            f"start cmd /k call activate ./{env_name}", 
            shell=True
        )
        # 前台输出
        self.show_success(f"激活环境: {env_name}")
    
    def export_requirements(self: Self) -> None:
        """导出依赖 requirements.txt"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 执行命令
        command: str = f"./{env_name}/python.exe -m pip freeze > ./requirements.txt"
        process: subprocess.Popen = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # 后台输出
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        # 等待命令执行完成
        process.wait()
        # 前台输出
        self.show_success("requirements.txt 导出完成!")
    
    def export_environment(self: Self) -> None:
        """导出依赖 environment.yml"""
        # 获取参数
        env_name: str = self.get_env_name()
        # 执行命令
        command: str = f"conda env export -p ./{env_name} > environment.yml"
        process: subprocess.Popen = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # 后台输出
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        # 等待命令执行完成
        process.wait()
        # 前台输出
        self.show_success("environment.yml 导出完成!")
    
    def get_env_name(self: Self) -> str:
        """带默认参数地获取环境名"""
        env_name: str = self.env_name_input.text().strip()
        return env_name if env_name else '.venv'
    
    def get_python_version(self: Self) -> str:
        """带默认参数地获取 Python 版本"""
        python_version: str = self.python_version_input.text().strip()
        return python_version if python_version else '3.10'
    
    def show_error(self: Self, message: str) -> None:
        """前台错误提示"""
        InfoBar.error(
            title="错误",
            content=message,
            orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def show_success(self: Self, message: str) -> None:
        """前台成功提示"""
        InfoBar.success(
            title="成功",
            content=message,
            orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    def clear_all_inputs(self: Self) -> None:
        """清空所有动态添加的输入框"""
        self.clear_input_container(self.pip_inputs_container)
        self.clear_input_container(self.conda_inputs_container)
    
    def clear_input_container(self: Self, container: QVBoxLayout) -> None:
        """清空指定的输入容器"""
        while container.count():
            item: QLayoutItem = container.takeAt(0)
            layout: QLayout = item.layout()
            if layout:
                self.clear_layout(layout)
            container.removeItem(item)
    
    def clear_layout(self: Self, layout: QLayout) -> None:
        """递归清除布局中的所有部件"""
        while layout.count():
            item: QLayoutItem = layout.takeAt(0)
            widget: QWidget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sub_layout: QLayout = item.layout()
                if sub_layout:
                    self.clear_layout(sub_layout)
    
    def add_pip_input_row(self: Self, package_text: str = "") -> None:
        """增加 pip 包输入框"""
        row_layout: QHBoxLayout = QHBoxLayout()
        package_input: LineEdit = LineEdit(self)
        package_input.setPlaceholderText("输入 pip 包名")
        if package_text:
            package_input.setText(package_text)
        row_layout.addWidget(package_input)
        # 添加删除按钮
        remove_btn: PushButton = PushButton("移除", self)
        remove_btn.setStyleSheet(red_style.get_button_style())
        remove_btn.setFixedWidth(100)
        remove_btn.clicked.connect(lambda: self.remove_input_row(row_layout))
        row_layout.addWidget(remove_btn)
        # 添加到容器
        self.pip_inputs_container.addLayout(row_layout)
    
    def add_conda_input_row(self: Self, package_text: str = "") -> None:
        """增加 conda 包输入框"""
        row_layout: QHBoxLayout = QHBoxLayout()
        package_input: LineEdit = LineEdit(self)
        package_input.setPlaceholderText("输入 conda 包名")
        if package_text:
            package_input.setText(package_text)
        row_layout.addWidget(package_input)
        # 添加删除按钮
        remove_btn: PushButton = PushButton("移除", self)
        remove_btn.setStyleSheet(red_style.get_button_style())
        remove_btn.setFixedWidth(100)
        remove_btn.clicked.connect(lambda: self.remove_input_row(row_layout))
        row_layout.addWidget(remove_btn)
        # 添加到容器
        self.conda_inputs_container.addLayout(row_layout)
    
    def remove_input_row(self: Self, row_layout: QHBoxLayout) -> None:
        """移除输入框"""
        # 移除布局中的所有部件
        while row_layout.count():
            item: QLayoutItem = row_layout.takeAt(0)
            widget: QWidget = item.widget()
            if widget:
                widget.deleteLater()
        # 从容器布局中移除该行
        if self.pip_inputs_container.indexOf(row_layout) != -1:
            self.pip_inputs_container.removeItem(row_layout)
        elif self.conda_inputs_container.indexOf(row_layout) != -1:
            self.conda_inputs_container.removeItem(row_layout)
    
    def save_ui_to_config(self: Self) -> None:
        """将当前UI状态保存到配置文件"""
        config: Dict[str, Any] = {
            "name": self.get_env_name(),
            "dependencies": [],
        }
        # 添加 Python 版本
        python_version: str = self.get_python_version()
        if python_version:
            config["dependencies"].append(f"python={python_version}")
        # 添加 conda 包
        conda_packages: List[str] = []
        for i in range(self.conda_inputs_container.count()):
            row_layout: QLayout = self.conda_inputs_container.itemAt(i).layout()
            if row_layout:
                input_widget: QWidget = row_layout.itemAt(0).widget() # pyright: ignore[reportOptionalMemberAccess]
                if isinstance(input_widget, LineEdit):
                    package: str = input_widget.text().strip()
                    if package:
                        conda_packages.append(package)
        config["dependencies"].extend(conda_packages)
        # 添加 pip 包
        pip_packages: List[str] = []
        for i in range(self.pip_inputs_container.count()):
            row_layout: QLayout = self.pip_inputs_container.itemAt(i).layout()
            if row_layout:
                input_widget: QWidget = row_layout.itemAt(0).widget() # pyright: ignore[reportOptionalMemberAccess]
                if isinstance(input_widget, LineEdit):
                    package: str = input_widget.text().strip()
                    if package:
                        pip_packages.append(package)
        if pip_packages:
            config["dependencies"].append({"pip": pip_packages})
        # 保存配置
        config_util.save_config(config)
