# interfaces/environment_build_interface.py
import subprocess
from PySide6.QtCore import Qt
from qfluentwidgets import PrimaryPushButton, LineEdit, InfoBar, InfoBarPosition, PushButton
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout

class EnvironmentBuildInterface(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName("EnvironmentBuildInterface")
        self.init_ui()
    
    def init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop) # pyright: ignore[reportAttributeAccessIssue]
        
        # 标题
        title = QLabel("环境构建工具", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #333333;")
        
        # 环境配置区域
        env_group = QGroupBox("环境配置", self)
        env_layout = QVBoxLayout(env_group)
        
        # 环境名称标签和输入框
        env_name_layout = QHBoxLayout()
        env_name_label = QLabel("输入环境名称：", self)
        env_name_label.setStyleSheet("font-size: 16px; color: #000000;")
        self.env_name_input = LineEdit(self)
        self.env_name_input.setPlaceholderText(".venv")
        env_name_layout.addWidget(env_name_label)
        env_name_layout.addWidget(self.env_name_input)

        # Python 版本标签和输入框
        python_version_layout = QHBoxLayout()
        python_version_label = QLabel("输入 Python 版本：", self)
        python_version_label.setStyleSheet("font-size: 16px; color: #000000;")
        self.python_version_input = LineEdit(self)
        self.python_version_input.setPlaceholderText("3.10")
        python_version_layout.addWidget(python_version_label)
        python_version_layout.addWidget(self.python_version_input)

        # 添加到环境配置布局
        env_layout.addLayout(env_name_layout)
        env_layout.addLayout(python_version_layout)
        
        # 创建环境按钮
        create_btn_layout = QHBoxLayout()
        self.create_btn = PrimaryPushButton("创建环境", self)
        self.create_btn.setMinimumHeight(40)
        self.create_btn.clicked.connect(self.create_venv)
        create_btn_layout.addWidget(self.create_btn)
        
        # 包管理区域
        pkg_group = QGroupBox("依赖包管理", self)
        pkg_layout = QVBoxLayout(pkg_group)
        
        # pip 包管理
        pip_group = QGroupBox("pip", self)
        pip_layout = QVBoxLayout(pip_group)
        
        # 添加 pip 包输入提示
        pip_add_label = QLabel("管理 pip 包：", self)
        pip_add_label.setStyleSheet("font-size: 16px; color: #000000;")
        
        # 添加一个容器用于存放动态添加的输入框
        self.pip_inputs_container = QVBoxLayout()
        
        pip_layout.addWidget(pip_add_label)
        pip_layout.addLayout(self.pip_inputs_container)
        
        # 添加按钮布局
        pip_btn_layout = QHBoxLayout()
        self.pip_add_btn = PushButton("添加", self)
        self.pip_add_btn.setFixedWidth(100)
        self.pip_add_btn.clicked.connect(self.add_pip_input_row)
        pip_btn_layout.addWidget(self.pip_add_btn)
        pip_layout.addLayout(pip_btn_layout)
        
        # conda 包管理
        conda_group = QGroupBox("conda", self)
        conda_layout = QVBoxLayout(conda_group)
        
        # 添加 conda 包输入提示
        conda_add_label = QLabel("管理 conda 包：", self)
        conda_add_label.setStyleSheet("font-size: 16px; color: #000000;")

        # 添加容器
        self.conda_inputs_container = QVBoxLayout()
        
        conda_layout.addWidget(conda_add_label)
        conda_layout.addLayout(self.conda_inputs_container)

        # 添加按钮布局
        conda_btn_layout = QHBoxLayout()
        self.conda_add_btn = PushButton("添加", self)
        self.conda_add_btn.setFixedWidth(100)
        self.conda_add_btn.clicked.connect(self.add_conda_input_row)
        conda_btn_layout.addWidget(self.conda_add_btn)
        conda_layout.addLayout(conda_btn_layout)
        
        pkg_layout.addWidget(pip_group)
        pkg_layout.addWidget(conda_group)
        
        # 操作按钮区域
        action_group = QGroupBox("操作", self)
        action_layout = QVBoxLayout(action_group)
        
        self.activate_btn = PrimaryPushButton("激活环境", self)
        self.activate_btn.setMinimumHeight(40)
        self.activate_btn.clicked.connect(self.activate_venv)
        
        self.update_btn = PrimaryPushButton("更新依赖", self)
        self.update_btn.setMinimumHeight(40)
        self.update_btn.clicked.connect(self.update_package)
        
        self.export_req_btn = PrimaryPushButton("导出依赖 requirements.txt", self)
        self.export_req_btn.setMinimumHeight(40)
        self.export_req_btn.clicked.connect(self.export_package)
        
        self.export_yml_btn = PrimaryPushButton("导出依赖 environment.yml", self)
        self.export_yml_btn.setMinimumHeight(40)
        self.export_yml_btn.clicked.connect(self.export_environment_yml)
        
        action_layout.addWidget(self.activate_btn)
        action_layout.addWidget(self.update_btn)
        action_layout.addWidget(self.export_req_btn)
        action_layout.addWidget(self.export_yml_btn)
        
        # 添加到主布局
        main_layout.addWidget(title)
        main_layout.addWidget(env_group)
        main_layout.addLayout(create_btn_layout)
        main_layout.addWidget(pkg_group)
        main_layout.addWidget(action_group)
        
        self.setLayout(main_layout)
    
    def create_venv(self) -> None:
        env_name = self.get_env_name()
        python_version = self.get_python_version()
        
        self.toggle_buttons(False)
        
        command = f"conda create -p .\\{env_name} python={python_version or '3.10'} -y"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print("开始创建环境!\n")
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        
        process.wait()
        # 创建 .gitignore 文件
        try:
            gitignore_path = f".\\{env_name}\\.gitignore"
            with open(gitignore_path, "w") as f:
                f.write("*")
            print(f"✅ 已创建 .gitignore 文件: {gitignore_path}!\n")
        except Exception as e:
            print(f"❌ 创建 .gitignore 文件失败: {str(e)}!\n")
        
        print("✅ 环境创建完成!\n")
        self.toggle_buttons(True)
    
    def update_package(self) -> None:
        env_name = self.get_env_name()
        
        self.toggle_buttons(False)
        
        # 获取所有 pip 包输入框的内容
        pip_packages = []
        for i in range(self.pip_inputs_container.count()):
            row_layout = self.pip_inputs_container.itemAt(i).layout()
            if row_layout:
                for j in range(row_layout.count()):
                    widget = row_layout.itemAt(j).widget() # pyright: ignore[reportOptionalMemberAccess]
                    if isinstance(widget, LineEdit):
                        package = widget.text().strip()
                        if package:
                            pip_packages.append(package)
                        break
        
        # 获取所有 conda 包输入框的内容
        conda_packages = []
        for i in range(self.conda_inputs_container.count()):
            row_layout = self.conda_inputs_container.itemAt(i).layout()
            if row_layout:
                for j in range(row_layout.count()):
                    widget = row_layout.itemAt(j).widget() # pyright: ignore[reportOptionalMemberAccess]
                    if isinstance(widget, LineEdit):
                        package = widget.text().strip()
                        if package:
                            conda_packages.append(package)
                        break
        
        # 安装 pip 包
        for package in pip_packages:
            self.install_pip_package(env_name, package)
        
        # 安装 conda 包
        for package in conda_packages:
            self.install_conda_package(env_name, package)
        
        print("✅ 依赖更新完成!\n")
        self.toggle_buttons(True)
    
    def install_pip_package(self, env_name: str, package: str) -> None:
        env_name = self.get_env_name()
        
        self.toggle_buttons(False)
        
        command = f".\\{env_name}\\python.exe -m pip install {package} -i https://pypi.tuna.tsinghua.edu.cn/simple"
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print(f"开始安装pip包: {package}\n")
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        
        process.wait()
        print(f"✅ pip包安装完成: {package}\n")
    
    def install_conda_package(self, env_name: str, package: str) -> None:
        env_name = self.get_env_name()
        
        self.toggle_buttons(False)
        
        command = f"conda install -p .\\{env_name} {package} -y"
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print(f"开始安装conda包: {package}\n")
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        
        process.wait()
        print(f"✅ conda包安装完成: {package}\n")
    
    def export_package(self) -> None:
        env_name = self.get_env_name()
        
        self.toggle_buttons(False)
        
        command = f".\\{env_name}\\python.exe -m pip freeze > .\\requirements.txt"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print("开始导出 requirements.txt 文件...\n")
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        
        process.wait()
        print("✅ requirements.txt 导出完成!\n")
        self.toggle_buttons(True)
    
    def export_environment_yml(self) -> None:
        env_name = self.get_env_name()
        
        self.toggle_buttons(False)
        
        command = f"conda env export -p .\\{env_name} > environment.yml"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print("开始导出 environment.yml 文件...\n")
        for line in process.stdout: # pyright: ignore[reportOptionalIterable]
            print(line.strip())
        
        process.wait()
        print("✅ environment.yml 导出完成!\n")
        self.toggle_buttons(True)
    
    def activate_venv(self) -> None:
        env_name = self.get_env_name()
        
        self.show_success(f"正在激活环境: {env_name}")
        
        subprocess.run(
            f"start cmd /k call activate .\\{env_name}", 
            shell=True
        )
    
    def get_env_name(self) -> str:
        env_name = self.env_name_input.text().strip()
        return env_name if env_name else '.venv'
    
    def get_python_version(self) -> str:
        python_version = self.python_version_input.text().strip()
        return python_version if python_version else '3.10'
    
    def toggle_buttons(self, enabled: bool) -> None:
        self.create_btn.setEnabled(enabled)
        self.update_btn.setEnabled(enabled)
        self.export_req_btn.setEnabled(enabled)
        self.export_yml_btn.setEnabled(enabled)
        self.activate_btn.setEnabled(enabled)
        self.pip_add_btn.setEnabled(enabled)
        self.conda_add_btn.setEnabled(enabled)
    
    def show_error(self, message: str) -> None:
        InfoBar.error(
            title="错误",
            content=message,
            orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def show_success(self, message: str) -> None:
        InfoBar.success(
            title="成功",
            content=message,
            orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    # 在类中添加新方法
    def add_pip_input_row(self) -> None:
        row_layout = QHBoxLayout()
        package_input = LineEdit(self)
        package_input.setPlaceholderText("输入 pip 包名")
        row_layout.addWidget(package_input)
        
        # 添加删除按钮
        remove_btn = PushButton("移除", self)
        remove_btn.setFixedWidth(100)
        remove_btn.clicked.connect(lambda: self.remove_input_row(row_layout))
        row_layout.addWidget(remove_btn)
        
        self.pip_inputs_container.addLayout(row_layout)

    def add_conda_input_row(self) -> None:
        row_layout = QHBoxLayout()
        package_input = LineEdit(self)
        package_input.setPlaceholderText("输入 conda 包名")
        row_layout.addWidget(package_input)
        
        # 添加删除按钮
        remove_btn = PushButton("移除", self)
        remove_btn.setFixedWidth(100)
        remove_btn.clicked.connect(lambda: self.remove_input_row(row_layout))
        row_layout.addWidget(remove_btn)
        
        self.conda_inputs_container.addLayout(row_layout)

    def remove_input_row(self, row_layout: QHBoxLayout) -> None:
        # 移除布局中的所有部件
        while row_layout.count():
            item = row_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 从容器布局中移除该行
        if self.pip_inputs_container.indexOf(row_layout) != -1:
            self.pip_inputs_container.removeItem(row_layout)
        elif self.conda_inputs_container.indexOf(row_layout) != -1:
            self.conda_inputs_container.removeItem(row_layout)
