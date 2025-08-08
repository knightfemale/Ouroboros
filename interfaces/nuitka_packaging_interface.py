# interfaces/nuitka_packaging_interface.py
import subprocess
from pathlib import Path
from PySide6.QtCore import Qt
from typing import Any, Self, List, Dict, Optional
from qfluentwidgets import SingleDirectionScrollArea
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGroupBox

from utils import config_util, gui_util
from styles.default import TITLE_STYLE, BACKGROUND_STYLE, green_style, purple_style

button_style: str = purple_style.get_button_style()

class NuitkaPackagingInterface(QWidget):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("NuitkaPackagingInterface")
        # 初始化 UI
        self.init_ui()
        # 加载配置到 UI
        self.load_config_to_ui()
    
    def init_ui(self: Self) -> None:
        """初始化 UI"""
        # 创建主滚动区域
        scroll_area: SingleDirectionScrollArea = SingleDirectionScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame) # pyright: ignore[reportAttributeAccessIssue]
        scroll_area.setStyleSheet(BACKGROUND_STYLE)
        # 创建内容容器
        content_widget: QWidget = QWidget()
        main_layout: QVBoxLayout = QVBoxLayout(content_widget)
        main_layout.setAlignment(Qt.AlignTop) # pyright: ignore[reportAttributeAccessIssue]
        # 标题区域
        title: QLabel = QLabel("Nuitka 打包工具", self)
        title.setStyleSheet(TITLE_STYLE)
        main_layout.addWidget(title)
        # 操作区域
        action_group: QGroupBox = QGroupBox("操作", self)
        action_group.setStyleSheet(purple_style.get_groupbox_style())
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        self.build_btn = gui_util.PrimaryButtonBuilder.create(self, action_layout, "编译打包", slot=self.start_packaging, style=button_style)
        # 添加到主布局
        main_layout.addWidget(action_group)
        # 基本选项区域
        options_group: QGroupBox = QGroupBox("基本选项", self)
        options_group.setStyleSheet(purple_style.get_groupbox_style())
        options_layout: QVBoxLayout = QVBoxLayout(options_group)
        self.entry_input = gui_util.InputBuilder.create(self, options_layout, "输入 Python 入口文件(例如: ./main.py)")
        self.output_name_input = gui_util.InputBuilder.create(self, options_layout, "输出文件名(默认: 入口文件名)")
        self.output_dir_input = gui_util.InputBuilder.create(self, options_layout, "输出目录(默认: 根目录)")
        self.build_mode_combo = gui_util.ComboBoxBuilder.create(self, options_layout, "构建模式", ["独立模式", "单文件模式", "模块模式"])
        self.console_switch = gui_util.SwitchBuilder.create(self, options_layout, "禁用控制台")
        self.remove_switch = gui_util.SwitchBuilder.create(self, options_layout, "删除构建文件夹")
        self.jobs_input = gui_util.InputBuilder.create(self, options_layout, "输入并行任务数(默认: all)")
        # 添加到主布局
        main_layout.addWidget(options_group)
        # 显式导入区域
        import_group: QGroupBox = QGroupBox("显式导入", self)
        import_group.setStyleSheet(purple_style.get_groupbox_style())
        import_layout: QVBoxLayout = QVBoxLayout(import_group)
        # 启用包
        package_group: QGroupBox = QGroupBox("启用包", self)
        package_group.setStyleSheet(purple_style.get_groupbox_style())
        package_layout: QVBoxLayout = QVBoxLayout(package_group)
        self.packages_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, "输入包名(例如: numpy)")
        package_layout.addLayout(self.packages_container.container_layout)
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, package_layout, "添加包", slot=lambda: self.packages_container.add_row(""), style=green_style.get_button_style())
        import_layout.addWidget(package_group)
        # 启用模块
        module_group: QGroupBox = QGroupBox("启用包", self)
        module_group.setStyleSheet(purple_style.get_groupbox_style())
        module_layout: QVBoxLayout = QVBoxLayout(module_group)
        self.modules_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, "输入模块名(例如: sys)")
        module_layout.addLayout(self.modules_container.container_layout)
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, module_layout, "添加模块", slot=lambda: self.modules_container.add_row(""), style=green_style.get_button_style())
        import_layout.addWidget(module_group)
        # 启用插件
        plugin_group: QGroupBox = QGroupBox("启用插件", self)
        plugin_group.setStyleSheet(purple_style.get_groupbox_style())
        plugin_layout: QVBoxLayout = QVBoxLayout(plugin_group)
        self.plugins_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, "输入插件名(例如: pyside6)")
        plugin_layout.addLayout(self.plugins_container.container_layout)
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, plugin_layout, "添加插件", slot=lambda: self.plugins_container.add_row(""), style=green_style.get_button_style())
        import_layout.addWidget(plugin_group)
        # 包含文件
        file_group: QGroupBox = QGroupBox("包含文件", self)
        file_group.setStyleSheet(purple_style.get_groupbox_style())
        file_layout: QVBoxLayout = QVBoxLayout(file_group)
        self.files_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, "输入文件路径(格式: 源文件=目标路径)")
        file_layout.addLayout(self.files_container.container_layout)
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, file_layout, "添加文件", slot=lambda: self.files_container.add_row(""), style=green_style.get_button_style())
        import_layout.addWidget(file_group)
        # 包含目录
        dir_group: QGroupBox = QGroupBox("包含目录", self)
        dir_group.setStyleSheet(purple_style.get_groupbox_style())
        dir_layout: QVBoxLayout = QVBoxLayout(dir_group)
        self.dirs_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, "输入目录路径(格式: 源目录=目标路径)")
        dir_layout.addLayout(self.dirs_container.container_layout)
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, dir_layout, "添加目录", slot=lambda: self.dirs_container.add_row(""), style=green_style.get_button_style())
        import_layout.addWidget(dir_group)
        # 添加到主布局
        main_layout.addWidget(import_group)
        # 高级选项区域
        advanced_group: QGroupBox = QGroupBox("高级选项", self)
        advanced_group.setStyleSheet(purple_style.get_groupbox_style())
        advanced_layout: QVBoxLayout = QVBoxLayout(advanced_group)
        self.scons_switch = gui_util.SwitchBuilder.create(self, advanced_layout, "显示 Scons 命令")
        self.download_switch = gui_util.SwitchBuilder.create(self, advanced_layout, "自动同意下载")
        self.compiler_combo = gui_util.ComboBoxBuilder.create(self, advanced_layout, "编译器", ["Auto", "MSVC", "MinGW64", "Clang"])
        # 额外参数
        extra_args_group: QGroupBox = QGroupBox("额外参数", self)
        extra_args_group.setStyleSheet(purple_style.get_groupbox_style())
        extra_args_layout: QVBoxLayout = QVBoxLayout(extra_args_group)
        self.extra_args_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, "输入额外参数(例如: --lto=yes)")
        extra_args_layout.addLayout(self.extra_args_container.container_layout)
        self.pip_add_btn = gui_util.ButtonBuilder.create(self, extra_args_layout, "添加参数", slot=lambda: self.extra_args_container.add_row(""), style=green_style.get_button_style())
        advanced_layout.addWidget(extra_args_group)
        # 添加到主布局
        main_layout.addWidget(advanced_group)
        # 将内容容器设置到滚动区域
        scroll_area.setWidget(content_widget)
        # 设置主布局为滚动区域
        outer_layout: QVBoxLayout = QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(outer_layout)
    
    def load_config_to_ui(self: Self) -> None:
        """从配置文件加载数据到 UI"""
        config: Dict[str, Any] = config_util.load_config().get("nuitka", {})
        # 固定字段
        self.entry_input.setText(config.get("entry", ""))
        self.output_name_input.setText(config.get("output_name", ""))
        self.output_dir_input.setText(config.get("output_dir", ""))
        build_mode: str = config.get("build_mode", "独立模式")
        self.build_mode_combo.setCurrentText(build_mode)
        self.console_switch.setChecked(config.get("disable_console", False))
        self.remove_switch.setChecked(config.get("remove", True))
        self.scons_switch.setChecked(config.get("scons", False))
        self.download_switch.setChecked(config.get("download", True))
        self.compiler_combo.setCurrentText(config.get("compiler", "Auto"))
        self.jobs_input.setText(config.get("jobs", ""))
        # 动态字段
        for field in ["plugins", "packages", "modules", "files", "dirs", "extra_args"]:
            container: gui_util.DynamicInputContainer = getattr(self, f"{field}_container")
            container.set_items(config.get(field, []))
    
    def save_ui_to_config(self: Self) -> None:
        """保存UI状态到配置文件"""
        config: Dict[str, Any] = config_util.load_config()
        nuitka_config: Dict[str, Any] = config.setdefault("nuitka", {})
        # 固定字段
        nuitka_config.update({
            "entry": self.entry_input.text().strip(),
            "output_name": self.output_name_input.text().strip(),
            "output_dir": self.output_dir_input.text().strip(),
            "build_mode": self.build_mode_combo.currentText(),
            "disable_console": self.console_switch.isChecked(),
            "remove_output": self.remove_switch.isChecked(),
            "show_scons": self.scons_switch.isChecked(),
            "assume_yes": self.download_switch.isChecked(),
            "compiler": self.compiler_combo.currentText(),
            "jobs": self.jobs_input.text().strip(),
        })
        # 动态字段
        for field in ["plugins", "packages", "modules", "files", "dirs", "extra_args"]:
            container: gui_util.DynamicInputContainer = getattr(self, f"{field}_container")
            nuitka_config[field] = container.get_items()
        config_util.save_config(config)
    
    def start_packaging(self: Self) -> None:
        """执行打包命令"""
        # 保存到配置
        self.save_ui_to_config()
        # 解释器路径
        python_path: Path = Path.cwd() / f"{config_util.load_config().get("name")}/python"
        # 参数列表
        nuitka_args: List = ["-m", "nuitka"]
        # 添加输入框参数
        INPUT_FIELDS = {
            "entry_input": "",
            "output_name_input": "--output-filename=",
            "output_dir_input": "--output-dir=",
            "jobs_input": "--jobs="
        }
        for attr, flag in INPUT_FIELDS.items():
            if value := getattr(self, attr).text().strip():
                nuitka_args.append(f"{flag}{value}")
        # 添加开关参数
        STITCH: Dict[str, Any] = {
            "console": "--windows-console-mode=disable",
            "remove": "--remove-output",
            "scons": "--show-scons",
            "download": "--assume-yes-for-downloads",
        }
        for attr, flag in STITCH.items():
            if getattr(self, f"{attr}_switch").isChecked():
                nuitka_args.append(flag)
        # 添加下拉框参数
        COMBO_PARAMS = {
            "build_mode_combo": {
                "独立模式": "--standalone",
                "单文件模式": "--onefile",
                "模块模式": "--module"
            },
            "compiler_combo": {
                "MSVC": "--msvc=latest",
                "MinGW64": "--mingw64",
                "Clang": "--clang"
            },
        }
        for combo_name, mapping in COMBO_PARAMS.items():
            combo = getattr(self, combo_name)
            current_text = combo.currentText()
            if current_text in mapping:
                nuitka_args.append(mapping[current_text])
        # 添加动态输入框参数
        for field, flag in [
            ("plugins", "--enable-plugin="),
            ("packages", "--include-package="),
            ("modules", "--include-module="),
            ("files", "--include-data-files="),
            ("dirs", "--include-data-dir="),
            ("extra_args", ""),
        ]:
            container: gui_util.DynamicInputContainer = getattr(self, f"{field}_container")
            for item in container.get_items():
                nuitka_args.append(f"{flag}{item}")
        # 执行命令
        command: str = f"start \"NuitkaBuild\" cmd /k \"{str(python_path)}\" {" ".join(nuitka_args)}"
        gui_util.MessageDisplay.info(self, f"开始编译打包: {command}")
        subprocess.run(command, shell=True)
