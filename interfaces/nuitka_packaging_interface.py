# interfaces/nuitka_packaging_interface.py
import subprocess
from pathlib import Path
from PySide6.QtCore import Qt
from typing import Any, List, Dict
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGroupBox
from qfluentwidgets import PrimaryPushButton, LineEdit, PushButton, ModelComboBox, SwitchButton, SingleDirectionScrollArea

from utils import config_util, gui_util
from styles.default import TITLE_STYLE, LABLE_STYLE, BACKGROUND_STYLE, green_style, purple_style

class NuitkaPackagingInterface(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("NuitkaPackagingInterface")
        # 初始化 UI
        self.init_ui()
        # 加载配置到 UI
        self.load_config_to_ui()
    
    def init_ui(self) -> None:
        """初始化 UI"""
        # 创建主滚动区域
        scroll_area = SingleDirectionScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame) # pyright: ignore[reportAttributeAccessIssue]
        scroll_area.setStyleSheet(BACKGROUND_STYLE)
        # 创建内容容器
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setAlignment(Qt.AlignTop) # pyright: ignore[reportAttributeAccessIssue]
        # 标题区域
        title = QLabel("Nuitka 打包工具", self)
        title.setStyleSheet(TITLE_STYLE)
        main_layout.addWidget(title)
        # 操作按钮区域
        action_group = QGroupBox("操作", self)
        action_group.setStyleSheet(purple_style.get_groupbox_style())
        action_layout = QVBoxLayout(action_group)
        # 构建按钮
        self.build_btn = PrimaryPushButton("编译打包", self)
        self.build_btn.setStyleSheet(purple_style.get_button_style())
        self.build_btn.setMinimumHeight(40)
        self.build_btn.clicked.connect(self.start_packaging)
        action_layout.addWidget(self.build_btn)
        # 添加到主布局
        main_layout.addWidget(action_group)
        # 基本选项区域
        options_group = QGroupBox("基本选项", self)
        options_group.setStyleSheet(purple_style.get_groupbox_style())
        options_layout = QVBoxLayout(options_group)
        # 入口文件
        entry_layout = QHBoxLayout()
        self.entry_input = LineEdit(self)
        self.entry_input.setPlaceholderText("输入 Python 入口文件")
        entry_layout.addWidget(self.entry_input)
        options_layout.addLayout(entry_layout)
        # 输出文件
        output_layout = QHBoxLayout()
        self.output_name_input = LineEdit(self)
        self.output_name_input.setPlaceholderText("输出文件名(默认: 入口文件名)")
        output_layout.addWidget(self.output_name_input)
        options_layout.addLayout(output_layout)
        # 输出目录
        output_dir_layout = QHBoxLayout()
        self.output_dir_input = LineEdit(self)
        self.output_dir_input.setPlaceholderText("输出目录(默认: 根目录)")
        output_dir_layout.addWidget(self.output_dir_input)
        options_layout.addLayout(output_dir_layout)
        # 构建模式选择
        build_mode_layout = QHBoxLayout()
        build_mode_label = QLabel("构建模式", self)
        build_mode_label.setStyleSheet(LABLE_STYLE)
        self.build_mode_combo = ModelComboBox(self)
        self.build_mode_combo.addItems(["独立模式", "单文件格式", "模块模式"])
        build_mode_layout.addWidget(build_mode_label)
        build_mode_layout.addWidget(self.build_mode_combo)
        options_layout.addLayout(build_mode_layout)
        # 禁用控制台
        console_layout = QHBoxLayout()
        self.console_switch = SwitchButton(self)
        console_lable = QLabel("禁用控制台", self)
        console_lable.setStyleSheet(LABLE_STYLE)
        console_layout.addWidget(console_lable)
        console_layout.addWidget(self.console_switch)
        options_layout.addLayout(console_layout)
        # 删除构建文件夹
        remove_layout = QHBoxLayout()
        self.remove_switch = SwitchButton(self)
        self.remove_switch.setChecked(True)
        remove_lable = QLabel("删除构建文件夹")
        remove_lable.setStyleSheet(LABLE_STYLE)
        remove_layout.addWidget(remove_lable)
        remove_layout.addWidget(self.remove_switch)
        options_layout.addLayout(remove_layout)
        # 并行任务数
        jobs_layout = QHBoxLayout()
        self.jobs_input = LineEdit(self)
        self.jobs_input.setPlaceholderText("输入并行任务数(默认: all)")
        jobs_layout.addWidget(self.jobs_input)
        options_layout.addLayout(jobs_layout)
        # 加入布局
        main_layout.addWidget(options_group)
        # 显式导入区域
        import_group = QGroupBox("显式导入", self)
        import_group.setStyleSheet(purple_style.get_groupbox_style())
        import_layout = QVBoxLayout(import_group)
        # 启用包
        package_group = QGroupBox("启用包", self)
        package_group.setStyleSheet(purple_style.get_groupbox_style())
        package_layout = QVBoxLayout(package_group)
        self.packages_container = QVBoxLayout()
        package_layout.addLayout(self.packages_container)
        # 添加按钮布局
        package_btn_layout = QHBoxLayout()
        self.package_add_btn = PushButton("添加包", self)
        self.package_add_btn.setStyleSheet(green_style.get_button_style())
        self.package_add_btn.setFixedWidth(100)
        self.package_add_btn.clicked.connect(lambda: self.add_dynamic_row("packages"))
        package_layout.addLayout(package_btn_layout)
        # 加入布局
        package_btn_layout.addWidget(self.package_add_btn)
        import_layout.addWidget(package_group)
        # 启用模块
        module_group = QGroupBox("启用模块", self)
        module_group.setStyleSheet(purple_style.get_groupbox_style())
        module_layout = QVBoxLayout(module_group)
        self.modules_container = QVBoxLayout()
        module_layout.addLayout(self.modules_container)
        # 添加按钮布局
        module_btn_layout = QHBoxLayout()
        self.module_add_btn = PushButton("添加模块", self)
        self.module_add_btn.setStyleSheet(green_style.get_button_style())
        self.module_add_btn.setFixedWidth(100)
        self.module_add_btn.clicked.connect(lambda: self.add_dynamic_row("modules"))
        module_layout.addLayout(module_btn_layout)
        # 加入布局
        module_btn_layout.addWidget(self.module_add_btn)
        import_layout.addWidget(module_group)
        # 启用插件
        plugin_group = QGroupBox("启用插件", self)
        plugin_group.setStyleSheet(purple_style.get_groupbox_style())
        plugin_layout = QVBoxLayout(plugin_group)
        self.plugins_container = QVBoxLayout()
        plugin_layout.addLayout(self.plugins_container)
        # 添加按钮布局
        plugin_btn_layout = QHBoxLayout()
        self.plugin_add_btn = PushButton("添加插件", self)
        self.plugin_add_btn.setStyleSheet(green_style.get_button_style())
        self.plugin_add_btn.setFixedWidth(100)
        self.plugin_add_btn.clicked.connect(lambda: self.add_dynamic_row("plugins"))
        plugin_layout.addLayout(plugin_btn_layout)
        # 加入布局
        plugin_btn_layout.addWidget(self.plugin_add_btn)
        import_layout.addWidget(plugin_group)
        # 包含文件
        file_group = QGroupBox("包含文件", self)
        file_group.setStyleSheet(purple_style.get_groupbox_style())
        file_layout = QVBoxLayout(file_group)
        self.files_container = QVBoxLayout()
        file_layout.addLayout(self.files_container)
        # 添加按钮布局
        file_btn_layout = QHBoxLayout()
        self.file_add_btn = PushButton("添加文件", self)
        self.file_add_btn.setStyleSheet(green_style.get_button_style())
        self.file_add_btn.setFixedWidth(100)
        self.file_add_btn.clicked.connect(lambda: self.add_dynamic_row("files"))
        file_layout.addLayout(file_btn_layout)
        # 加入布局
        file_btn_layout.addWidget(self.file_add_btn)
        import_layout.addWidget(file_group)
        # 包含目录
        dir_group = QGroupBox("包含目录", self)
        dir_group.setStyleSheet(purple_style.get_groupbox_style())
        dir_layout = QVBoxLayout(dir_group)
        self.dirs_container = QVBoxLayout()
        dir_layout.addLayout(self.dirs_container)
        # 添加按钮布局
        dir_btn_layout = QHBoxLayout()
        self.dir_add_btn = PushButton("添加目录", self)
        self.dir_add_btn.setStyleSheet(green_style.get_button_style())
        self.dir_add_btn.setFixedWidth(100)
        self.dir_add_btn.clicked.connect(lambda: self.add_dynamic_row("dirs"))
        dir_layout.addLayout(dir_btn_layout)
        # 加入布局
        dir_btn_layout.addWidget(self.dir_add_btn)
        import_layout.addWidget(dir_group)
        # 添加到主布局
        main_layout.addWidget(import_group)
        # 高级选项区域
        advanced_group = QGroupBox("高级选项", self)
        advanced_group.setStyleSheet(purple_style.get_groupbox_style())
        advanced_layout = QVBoxLayout(advanced_group)
        # 显示 Scons 命令
        scons_layout = QHBoxLayout()
        self.scons_switch = SwitchButton(self)
        self.scons_switch.setChecked(True)
        scons_lable = QLabel("显示 Scons 命令")
        scons_lable.setStyleSheet(LABLE_STYLE)
        scons_layout.addWidget(scons_lable)
        scons_layout.addWidget(self.scons_switch)
        advanced_layout.addLayout(scons_layout)
        # 自动同意下载
        download_layout = QHBoxLayout()
        self.download_switch = SwitchButton(self)
        self.download_switch.setChecked(True)
        download_lable = QLabel("自动同意下载")
        download_lable.setStyleSheet(LABLE_STYLE)
        download_layout.addWidget(download_lable)
        download_layout.addWidget(self.download_switch)
        advanced_layout.addLayout(download_layout)
        # 编译器选择
        compiler_layout = QHBoxLayout()
        self.compiler_combox = ModelComboBox(self)
        self.compiler_combox.addItems(["Auto", "MSVC", "MinGW64", "Clang"])
        compiler_lable = QLabel("编译器", self)
        compiler_lable.setStyleSheet(LABLE_STYLE)
        compiler_layout.addWidget(compiler_lable)
        compiler_layout.addWidget(self.compiler_combox)
        advanced_layout.addLayout(compiler_layout)
        # 其他参数
        other_args_layout = QHBoxLayout()
        self.other_args_input = LineEdit(self)
        self.other_args_input.setPlaceholderText("其他 Nuitka 参数")
        other_args_lable = QLabel("其他参数")
        other_args_lable.setStyleSheet(LABLE_STYLE)
        other_args_layout.addWidget(other_args_lable)
        other_args_layout.addWidget(self.other_args_input)
        advanced_layout.addLayout(other_args_layout)
        # 添加到主布局
        main_layout.addWidget(advanced_group)
        # 将内容容器设置到滚动区域
        scroll_area.setWidget(content_widget)
        # 设置主布局为滚动区域
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(outer_layout)
    
    def load_config_to_ui(self) -> None:
        """从配置文件加载数据到 UI"""
        config = config_util.load_config().get("nuitka", {})
        # 基本选项
        self.entry_input.setText(config.get("entry", ""))
        self.output_name_input.setText(config.get("output_name", ""))
        self.output_dir_input.setText(config.get("output_dir", ""))
        build_mode = config.get("build_mode", "独立模式")
        self.build_mode_combo.setCurrentText(build_mode)
        self.console_switch.setChecked(config.get("disable_console", False))
        self.remove_switch.setChecked(config.get("remove", True))
        self.scons_switch.setChecked(config.get("scons", True))
        self.download_switch.setChecked(config.get("download", True))
        self.compiler_combox.setCurrentText(config.get("compiler", "Auto"))
        self.jobs_input.setText(config.get("jobs", ""))
        self.other_args_input.setText(config.get("other_args", ""))
        # 动态字段
        for field in ["plugins", "packages", "modules", "files", "dirs"]:
            container = getattr(self, f"{field}_container")
            gui_util.clear_input_container(container)
            for item in config.get(field, []):
                self.add_dynamic_row(field, item)
    
    def add_dynamic_row(self, field_type: str, text: str = "") -> None:
        """添加动态行到指定容器"""
        container = getattr(self, f"{field_type}_container")
        PLACEHOLDER: Dict[str, str] = {
            "packages": "输入包名(例如: numpy)",
            "modules": "输入模块名(例如: sys)",
            "plugins": "输入插件名(例如: pyside6)",
            "files": "输入文件路径(格式: 源文件=目标路径)",
            "dirs": "输入目录路径(格式: 源目录=目标路径)",
        }
        row_layout = gui_util.create_removable_input_row(self, PLACEHOLDER[field_type], text)
        remove_btn = row_layout.itemAt(1).widget()
        remove_btn.clicked.connect(lambda: self.remove_row(row_layout, container)) # pyright: ignore[reportAttributeAccessIssue]
        container.addLayout(row_layout)
    
    def remove_row(self, row_layout: QHBoxLayout, container: QVBoxLayout) -> None:
        """移除指定行"""
        container.removeItem(row_layout)
        gui_util.clear_layout(row_layout)
    
    def save_ui_to_config(self) -> None:
        """保存UI状态到配置文件"""
        config = config_util.load_config()
        nuitka_config = config.setdefault("nuitka", {})
        # 基本选项
        nuitka_config.update({
            "entry": self.entry_input.text().strip(),
            "output_name": self.output_name_input.text().strip(),
            "output_dir": self.output_dir_input.text().strip(),
            "build_mode": self.build_mode_combo.currentText(),
            "disable_console": self.console_switch.isChecked(),
            "remove_output": self.remove_switch.isChecked(),
            "show_scons": self.scons_switch.isChecked(),
            "assume_yes": self.download_switch.isChecked(),
            "compiler": self.compiler_combox.currentText(),
            "jobs": self.jobs_input.text().strip(),
            "other_args": self.other_args_input.text().strip(),
        })
        # 动态字段
        for field in ["plugins", "packages", "modules", "files", "dirs"]:
            container = getattr(self, f"{field}_container")
            items = []
            for i in range(container.count()):
                row = container.itemAt(i).layout()
                if row:
                    input_widget = row.itemAt(0).widget()
                    if isinstance(input_widget, LineEdit):
                        text = input_widget.text().strip()
                        if text: items.append(text)
            nuitka_config[field] = items
        config_util.save_config(config)
    
    def start_packaging(self) -> None:
        """执行打包命令"""
        self.save_ui_to_config()
        python_path: Path = Path.cwd() / f"{config_util.load_config().get("name")}/python"
        # 构建命令
        nuitka_args: List = [
            "-m",
            "nuitka",
            self.entry_input.text().strip(),
        ]
        # 添加选项参数
        OPTIONS: Dict[str, Any] = {
            "console": "--windows-console-mode=disable",
            "remove": "--remove-output",
            "scons": "--show-scons",
            "download": "--assume-yes-for-downloads",
        }
        for attr, flag in OPTIONS.items():
            if getattr(self, f"{attr}_switch").isChecked():
                nuitka_args.append(flag)
        
        # 添加构建模式参数
        BUILD_MODE: Dict[str, str] = {
            "独立模式": "--standalone",
            "单文件模式": "--onefile",
            "模块模式": "--module"
        }
        build_mode = self.build_mode_combo.currentText()
        if build_mode in BUILD_MODE:
            nuitka_args.append(BUILD_MODE[build_mode])
        # 添加其他参数
        if output_name := self.output_name_input.text().strip():
            nuitka_args.append(f"--output-filename={output_name}")
        if output_dir := self.output_dir_input.text().strip():
            nuitka_args.append(f"--output-dir={output_dir}")
        if jobs := self.jobs_input.text().strip():
            nuitka_args.append(f"--jobs={jobs}")
        # 编译器选项
        compiler_map: Dict[str, str] = {
            "MSVC": "--msvc",
            "MinGW64": "--mingw64",
            "Clang": "--clang"
        }
        if compiler := compiler_map.get(self.compiler_combox.currentText()):
            nuitka_args.append(compiler)
        # 添加插件/包/模块等
        for field, flag in [
            ("plugins", "--enable-plugin"),
            ("packages", "--include-package"),
            ("modules", "--include-module"),
            ("files", "--include-data-files"),
            ("dirs", "--include-data-dir"),
        ]:
            for item in self.collect_dynamic_items(field):
                nuitka_args.append(f"{flag}={item}")
        # 其他参数
        if other_args := self.other_args_input.text().strip():
            nuitka_args.extend(other_args.split())
        # 执行命令
        command: str = f"start \"NuitkaBuild\" cmd /k \"{str(python_path)}\" {" ".join(nuitka_args)}"
        gui_util.show_info(self, f"开始编译打包: {command}")
        subprocess.run(command, shell=True)
    
    def collect_dynamic_items(self, field: str) -> list:
        """收集动态字段内容"""
        items = []
        container = getattr(self, f"{field}_container")
        for i in range(container.count()):
            row = container.itemAt(i).layout()
            if row:
                input_widget = row.itemAt(0).widget()
                if isinstance(input_widget, LineEdit):
                    if text := input_widget.text().strip():
                        items.append(text)
        return items
