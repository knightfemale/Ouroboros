# interfaces/nuitka_build_interface.py
import subprocess
import multiprocessing
from pathlib import Path
from typing import Any, Self, List, Dict, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from qfluentwidgets import LineEdit, ModelComboBox, SwitchButton, PushButton

from interfaces.interface import Interface
from utils import config_util, gui_util, delay_util
from utils.style_util import yellow_style, green_style

group_style: str = yellow_style.get_groupbox_style()
button_style: str = yellow_style.get_button_style()
lable_style: str = yellow_style.get_lable_style()

config_path: Path = config_util.config_path

class NuitkaBuildInterface(Interface):
    def __init__(self: Self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # 设置对象名
        self.setObjectName("NuitkaBuildInterface")
        # 初始化 UI
        self.init_ui()
        # 加载配置到 UI
        self.load_config_to_ui()
        # 延时变量
        self.delay_variables: Dict[str, Any] = {
            "nuitka_version": {
                "var": None,
                "object": self.nuitka_version_label,
                "command": ["", "-m", "nuitka", "--version"],
                "prefix": "Nuitka Version: ",
                "err": "未找到, 请确保 Nuitka 已安装",
                "operate": delay_util.set_label_text,
            },
        }
    
    def init_ui(self: Self) -> None:
        """初始化 UI"""
        # 标题区域
        self.title_label: QLabel = gui_util.LabelBuilder.create(self.content_widget, self.main_layout, content="Nuitka 编译打包")
        # 信息区域
        info_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "信息", style=group_style)
        info_layout: QVBoxLayout = QVBoxLayout(info_group)
        self.nuitka_version_label: QLabel = gui_util.LabelBuilder.create(self, info_layout, style=lable_style)
        # 操作区域
        action_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "操作", style=group_style)
        action_layout: QVBoxLayout = QVBoxLayout(action_group)
        self.build_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_layout, "编译打包", slot=self.start_packaging, style=button_style)
        self.save_btn: PushButton = gui_util.PrimaryButtonBuilder.create(self, action_layout, "保存配置", slot=self.save_ui_to_config, style=button_style)
        # 基本选项区域
        options_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "基本选项", style=group_style)
        options_layout: QVBoxLayout = QVBoxLayout(options_group)
        self.entry_input: LineEdit = gui_util.InputBuilder.create(self, options_layout, "Python 入口文件", "输入 Python 入口文件(例如: ./main.py)", lable_style=lable_style)
        self.output_name_input: LineEdit = gui_util.InputBuilder.create(self, options_layout, "输出文件名", "输出文件名(默认: 入口文件名)", lable_style=lable_style)
        self.output_dir_input: LineEdit = gui_util.InputBuilder.create(self, options_layout, "输出目录", "输出目录(默认: 根目录)", lable_style=lable_style)
        cpu_count = multiprocessing.cpu_count()
        jobs_options = [str(i) for i in range(1, cpu_count + 1)]
        self.default_job = str(cpu_count - 1) if cpu_count > 1 else "1"
        self.jobs_combo: ModelComboBox = gui_util.ComboBoxBuilder.create(self, options_layout, "并行任务数", jobs_options, current_text=self.default_job, lable_style=lable_style)
        self.build_mode_combo: ModelComboBox = gui_util.ComboBoxBuilder.create(self, options_layout, "构建模式", ["独立模式", "单文件模式", "模块模式"], lable_style=lable_style)
        self.disable_console_switch: SwitchButton = gui_util.SwitchBuilder.create(self, options_layout, "禁用控制台", lable_style=lable_style)
        self.remove_output_switch: SwitchButton = gui_util.SwitchBuilder.create(self, options_layout, "删除构建文件夹", lable_style=lable_style)
        # 显式导入区域
        import_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "显式导入", style=group_style)
        import_layout: QVBoxLayout = QVBoxLayout(import_group)
        # 启用包区域
        package_group: QGroupBox = gui_util.GroupBuilder.create(self, import_layout, "启用包", style=group_style)
        package_layout: QVBoxLayout = QVBoxLayout(package_group)
        self.packages_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, package_layout, "输入包名(例如: numpy)")
        self.add_package_btn: PushButton = gui_util.ButtonBuilder.create(self, package_layout, "添加包", slot=lambda: self.packages_container.add_row(""), style=green_style.get_button_style())
        # 启用模块区域
        module_group: QGroupBox = gui_util.GroupBuilder.create(self, import_layout, "启用模块", style=group_style)
        module_layout: QVBoxLayout = QVBoxLayout(module_group)
        self.modules_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, module_layout, "输入模块名(例如: sys)")
        self.add_module_btn = gui_util.ButtonBuilder.create(self, module_layout, "添加模块", slot=lambda: self.modules_container.add_row(""), style=green_style.get_button_style())
        # 启用插件区域
        plugin_group: QGroupBox = gui_util.GroupBuilder.create(self, import_layout, "启用插件", style=group_style)
        plugin_layout: QVBoxLayout = QVBoxLayout(plugin_group)
        self.plugins_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, plugin_layout, "输入插件名(例如: pyside6)")
        self.add_plugin_btn: PushButton = gui_util.ButtonBuilder.create(self, plugin_layout, "添加插件", slot=lambda: self.plugins_container.add_row(""), style=green_style.get_button_style())
        # 禁用导入项区域
        no_import_group: QGroupBox = gui_util.GroupBuilder.create(self, import_layout, "禁用导入项", style=group_style)
        no_import_layout: QVBoxLayout = QVBoxLayout(no_import_group)
        self.no_imports_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, no_import_layout, "输入导入项名(例如: *.tests)")
        self.add_no_import_btn: PushButton = gui_util.ButtonBuilder.create(self, no_import_layout, "添加导入项", slot=lambda: self.no_imports_container.add_row(""), style=green_style.get_button_style())
        # 包含文件区域
        file_group: QGroupBox = gui_util.GroupBuilder.create(self, import_layout, "包含文件", style=group_style)
        file_layout: QVBoxLayout = QVBoxLayout(file_group)
        self.files_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, file_layout, "输入文件路径(格式: 源文件=目标路径)")
        self.add_file_btn: PushButton = gui_util.ButtonBuilder.create(self, file_layout, "添加文件", slot=lambda: self.files_container.add_row(""), style=green_style.get_button_style())
        # 包含目录区域
        dir_group: QGroupBox = gui_util.GroupBuilder.create(self, import_layout, "包含目录", style=group_style)
        dir_layout: QVBoxLayout = QVBoxLayout(dir_group)
        self.dirs_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, dir_layout, "输入目录路径(格式: 源目录=目标路径)")
        self.add_dir_btn: PushButton = gui_util.ButtonBuilder.create(self, dir_layout, "添加目录", slot=lambda: self.dirs_container.add_row(""), style=green_style.get_button_style())
        # 高级选项区域
        advanced_group: QGroupBox = gui_util.GroupBuilder.create(self, self.main_layout, "高级选项", style=group_style)
        advanced_layout: QVBoxLayout = QVBoxLayout(advanced_group)
        self.compiler_combo: ModelComboBox = gui_util.ComboBoxBuilder.create(self, advanced_layout, "编译器", ["Auto", "MSVC", "MinGW64", "Clang"], lable_style=lable_style)
        self.show_scons_switch: SwitchButton = gui_util.SwitchBuilder.create(self, advanced_layout, "显示 Scons 命令", lable_style=lable_style)
        self.assume_yes_switch: SwitchButton = gui_util.SwitchBuilder.create(self, advanced_layout, "自动同意下载", lable_style=lable_style)
        # 额外参数区域
        extra_args_group: QGroupBox = gui_util.GroupBuilder.create(self, advanced_layout, "额外参数", style=group_style)
        extra_args_layout: QVBoxLayout = QVBoxLayout(extra_args_group)
        self.extra_args_container: gui_util.DynamicInputContainer = gui_util.DynamicInputContainer(self, extra_args_layout, "输入额外参数(例如: --lto=yes)")
        self.add_arg_btn: PushButton = gui_util.ButtonBuilder.create(self, extra_args_layout, "添加参数", slot=lambda: self.extra_args_container.add_row(""), style=green_style.get_button_style())
    
    def load_config_to_ui(self: Self) -> None:
        """从配置文件加载数据到 UI"""
        config: Dict[str, Any] = config_util.load_yaml(config_path).get("nuitka", {})
        # 固定字段
        self.entry_input.setText(config.get("entry", ""))
        self.output_name_input.setText(config.get("output_name", ""))
        self.output_dir_input.setText(config.get("output_dir", ""))
        build_mode: str = config.get("build_mode", "独立模式")
        self.build_mode_combo.setCurrentText(build_mode)
        self.disable_console_switch.setChecked(config.get("disable_console", False))
        self.remove_output_switch.setChecked(config.get("remove_output", True))
        self.show_scons_switch.setChecked(config.get("show_scons", False))
        self.assume_yes_switch.setChecked(config.get("assume_yes", True))
        self.compiler_combo.setCurrentText(config.get("compiler", "Auto"))
        self.jobs_combo.setCurrentText(config.get("jobs", self.default_job))
        # 动态字段
        for field in ["plugins", "packages", "modules", "no_imports", "files", "dirs", "extra_args"]:
            container: gui_util.DynamicInputContainer = getattr(self, f"{field}_container")
            container.set_items(config.get(field, []))
    
    def showEvent(self: Self, event: Any) -> None:
        """当界面显示时触发"""
        self.delay_variables["nuitka_version"]["command"][0] = self.get_python_path()
        super().showEvent(event)
    
    def save_ui_to_config(self: Self) -> None:
        """保存UI状态到配置文件"""
        config: Dict[str, Any] = config_util.load_yaml(config_path)
        nuitka_config: Dict[str, Any] = config.setdefault("nuitka", {})
        # 固定字段
        nuitka_config.update({
            "entry": self.entry_input.text().strip(),
            "output_name": self.output_name_input.text().strip(),
            "output_dir": self.output_dir_input.text().strip(),
            "build_mode": self.build_mode_combo.currentText(),
            "disable_console": self.disable_console_switch.isChecked(),
            "remove_output": self.remove_output_switch.isChecked(),
            "show_scons": self.show_scons_switch.isChecked(),
            "assume_yes": self.assume_yes_switch.isChecked(),
            "compiler": self.compiler_combo.currentText(),
            "jobs": self.jobs_combo.currentText(),
        })
        # 动态字段
        for field in ["plugins", "packages", "modules", "no_imports", "files", "dirs", "extra_args"]:
            container: gui_util.DynamicInputContainer = getattr(self, f"{field}_container")
            nuitka_config[field] = container.get_items()
        config_util.save_yaml(config, config_path)
        gui_util.MessageDisplay.success(self, "保存配置成功")
    
    def start_packaging(self: Self) -> None:
        """执行打包命令"""
        # 保存到配置
        self.save_ui_to_config()
        # 参数列表
        nuitka_args: List[str] = ["-m", "nuitka"]
        # 添加输入框参数
        INPUT_FIELDS = {
            "entry_input": "",
            "output_name_input": "--output-filename=",
            "output_dir_input": "--output-dir=",
        }
        for attr, flag in INPUT_FIELDS.items():
            if value := getattr(self, attr).text().strip():
                nuitka_args.append(f"{flag}{value}")
        # 添加开关参数
        STITCH: Dict[str, Any] = {
            "disable_console": "--windows-console-mode=disable",
            "remove_output": "--remove-output",
            "show_scons": "--show-scons",
            "assume_yes": "--assume-yes-for-downloads",
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
        if jobs := self.jobs_combo.currentText().strip():
            nuitka_args.append(f"--jobs={jobs}")
        # 添加动态输入框参数
        for field, flag in [
            ("plugins", "--enable-plugin="),
            ("packages", "--include-package="),
            ("modules", "--include-module="),
            ("files", "--include-data-files="),
            ("dirs", "--include-data-dir="),
            ("no_imports", "--nofollow-import-to="),
            ("extra_args", ""),
        ]:
            container: gui_util.DynamicInputContainer = getattr(self, f"{field}_container")
            for item in container.get_items():
                nuitka_args.append(f"{flag}{item}")
        # 执行命令
        if python_path := self.get_python_path():
            command: str = f"start \"NuitkaBuild\" cmd /k \"{python_path}\" {" ".join(nuitka_args)}"
            gui_util.MessageDisplay.info(self, f"开始编译打包: {command}")
            subprocess.run(command, shell=True)
    
    def get_python_path(self: Self) -> str:
        """获取可能的 Python 解释器路径"""
        possible_paths = [
            # conda 路径
            Path.cwd() / f"{config_util.load_yaml(config_path).get('name')}/python.exe",
            # uv 路径
            Path.cwd() / ".venv/Scripts/python.exe",
        ]
        # 检查路径是否存在
        for path in possible_paths:
            if path.exists():
                return str(path)
        gui_util.MessageDisplay.error(self, "未找到可用解释器")
        return ""
