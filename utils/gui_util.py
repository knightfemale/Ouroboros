# utils/gui_util.py
from PySide6.QtCore import Qt
from typing import Any, Self, List, Optional, Callable
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLayout,
    QLayoutItem,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QGroupBox,
)
from qfluentwidgets import (
    InfoBar,
    InfoBarPosition,
    LineEdit,
    PushButton,
    PrimaryPushButton,
    LineEdit,
    PushButton,
    SwitchButton,
    ModelComboBox,
)

from utils.style_util import red_style, TITLE_STYLE


class GroupBuilder:
    """区域构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        title: str,
        style: str = "",
    ) -> QGroupBox:
        group = QGroupBox(title, parent)
        group.setStyleSheet(style)
        layout.addWidget(group)
        return group


class LabelBuilder:
    """标签构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        content: str = "",
        style: str = TITLE_STYLE,
    ) -> QLabel:
        label: QLabel = QLabel(content, parent)
        label.setStyleSheet(style)
        layout.addWidget(label)
        return label


class ButtonBuilder:
    """按钮构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        text: str,
        slot: Callable,
        width: int = 100,
        style: str = "",
    ) -> PushButton:
        """创建按钮"""
        btn_layout: QHBoxLayout = QHBoxLayout()
        btn = PushButton(text, parent)
        btn.setStyleSheet(style)
        btn.setFixedWidth(width)
        btn.clicked.connect(slot)
        btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        return btn


class PrimaryButtonBuilder:
    """主要按钮构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        text: str,
        slot: Callable,
        height: int = 40,
        style: str = "",
    ) -> PrimaryPushButton:
        """创建按钮"""
        btn: PrimaryPushButton = PrimaryPushButton(text, parent)
        btn.setStyleSheet(style)
        btn.setMinimumHeight(height)
        btn.clicked.connect(slot)
        layout.addWidget(btn)
        return btn


class InputBuilder:
    """输入框构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        label_text: str,
        placeholder: str,
        style: str = "",
        lable_style: str = "",
    ) -> LineEdit:
        """创建输入框"""
        len_layout: QVBoxLayout = QVBoxLayout()
        label: QLabel = QLabel(label_text, parent)
        label.setStyleSheet(lable_style)
        input_widget: LineEdit = LineEdit(parent)
        input_widget.setPlaceholderText(placeholder)
        len_layout.addWidget(label)
        len_layout.addWidget(input_widget)
        layout.addLayout(len_layout)
        return input_widget


class SwitchBuilder:
    """开关构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        label_text: str,
        checked: bool = True,
        style: str = "",
        lable_style: str = "",
    ) -> SwitchButton:
        """创建开关行"""
        len_layout: QHBoxLayout = QHBoxLayout()
        label: QLabel = QLabel(label_text, parent)
        label.setStyleSheet(lable_style)
        switch = SwitchButton(parent)
        switch.setChecked(checked)
        len_layout.addWidget(label)
        len_layout.addWidget(switch)
        layout.addLayout(len_layout)
        return switch


class ComboBoxBuilder:
    """下拉框构建器"""

    @staticmethod
    def create(
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        label_text: str,
        items: list[str],
        current_text: Optional[str] = None,
        style: str = "",
        lable_style: str = "",
    ) -> ModelComboBox:
        """创建下拉框行"""
        len_layout: QHBoxLayout = QHBoxLayout()
        label: QLabel = QLabel(label_text, parent)
        label.setStyleSheet(lable_style)
        combo: ModelComboBox = ModelComboBox(parent)
        combo.addItems(items)
        if current_text:
            combo.setCurrentText(current_text)
        len_layout.addWidget(label)
        len_layout.addWidget(combo)
        layout.addLayout(len_layout)
        return combo


class DynamicInputContainer:
    def __init__(
        self: Self,
        parent: QWidget,
        layout: QVBoxLayout | QHBoxLayout,
        placeholder: str,
    ) -> None:
        self.parent: QWidget = parent
        self.placeholder: str = placeholder
        self.container_layout: QVBoxLayout = QVBoxLayout()
        self.rows: List[QHBoxLayout] = []
        layout.addLayout(self.container_layout)

    def add_row(self: Self, text: str = "") -> None:
        """添加一行输入框"""
        row_layout: QHBoxLayout = self._create_row_layout(text)
        self.container_layout.addLayout(row_layout)
        self.rows.append(row_layout)

    def _create_row_layout(self: Self, text: str) -> QHBoxLayout:
        """创建单行布局"""
        row_layout: QHBoxLayout = QHBoxLayout()
        input_widget: LineEdit = LineEdit(self.parent)
        input_widget.setPlaceholderText(self.placeholder)
        input_widget.setText(text)
        remove_btn: PushButton = PushButton("移除", self.parent)
        remove_btn.setStyleSheet(red_style.get_button_style())
        remove_btn.clicked.connect(lambda: self.remove_row(row_layout))
        row_layout.addWidget(input_widget)
        row_layout.addWidget(remove_btn)
        return row_layout

    def remove_row(self: Self, row_layout: QHBoxLayout) -> None:
        """移除指定行"""
        self.container_layout.removeItem(row_layout)
        self._clear_layout(row_layout)
        self.rows.remove(row_layout)

    def clear_all(self: Self) -> None:
        """清空所有行"""
        while self.rows:
            row: QHBoxLayout = self.rows.pop()
            self.container_layout.removeItem(row)
            self._clear_layout(row)

    def _clear_layout(self: Self, layout: QLayout) -> None:
        """递归清除布局中的所有部件"""
        while layout.count():
            item: QLayoutItem = layout.takeAt(0)
            if widget := item.widget():
                if widget:
                    widget.deleteLater()
                else:
                    sub_layout: QLayout = item.layout()
                    if sub_layout:
                        self._clear_layout(sub_layout)

    def set_items(self: Self, items: list[str]) -> None:
        """设置容器内容"""
        self.clear_all()
        for item in items:
            self.add_row(item)

    def get_items(self: Self) -> list[str]:
        """获取所有行的文本内容"""
        items: List[str] = []
        for row in self.rows:
            input_widget = row.itemAt(0).widget()
            if isinstance(input_widget, LineEdit):
                text = input_widget.text().strip()
                if text:
                    items.append(text)
        return items


class MessageDisplay:
    """消息显示工具类"""

    @staticmethod
    def info(parent: Any, message: str) -> None:
        """显示信息提示"""
        InfoBar.info(
            title="信息",
            content=message,
            orient=Qt.Horizontal,  # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent,
        )

    @staticmethod
    def error(parent: Any, message: str) -> None:
        """显示错误提示"""
        InfoBar.error(
            title="错误",
            content=message,
            orient=Qt.Horizontal,  # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent,
        )

    @staticmethod
    def success(parent: Any, message: str) -> None:
        """显示成功提示"""
        InfoBar.success(
            title="成功",
            content=message,
            orient=Qt.Horizontal,  # pyright: ignore[reportAttributeAccessIssue]
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent,
        )
