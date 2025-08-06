# utils/gui_util.py
from typing import Any
from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition, LineEdit, PushButton
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout, QLayoutItem

from styles.default import red_style

def show_error(parent: Any, message: str) -> None:
    """显示错误提示"""
    InfoBar.error(
        title="错误",
        content=message,
        orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent
    )

def show_success(parent: Any, message: str) -> None:
    """显示成功提示"""
    InfoBar.success(
        title="成功",
        content=message,
        orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=parent
    )

def show_info(parent: Any, message: str) -> None:
    """显示信息提示"""
    InfoBar.info(
        title="信息",
        content=message,
        orient=Qt.Horizontal, # pyright: ignore[reportAttributeAccessIssue]
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1500,
        parent=parent
    )

def create_removable_input_row(parent: QWidget, placeholder: str,default_text: str) -> QHBoxLayout:
    """创建可移除的输入行"""
    row_layout: QHBoxLayout = QHBoxLayout()
    input_widget: LineEdit = LineEdit(parent)
    input_widget.setPlaceholderText(placeholder)
    
    if default_text:
        input_widget.setText(default_text)
    
    remove_btn: PushButton = PushButton("移除", parent)
    remove_btn.setStyleSheet(red_style.get_button_style())
    
    row_layout.addWidget(input_widget)
    row_layout.addWidget(remove_btn)
    
    return row_layout

def clear_layout(layout: QLayout) -> None:
    """递归清除布局中的所有部件"""
    while layout.count():
        item: QLayoutItem = layout.takeAt(0)
        widget: QWidget = item.widget()
        if widget:
            widget.deleteLater()
        else:
            sub_layout: QLayout = item.layout()
            if sub_layout:
                clear_layout(sub_layout)

def clear_input_container(container: QVBoxLayout) -> None:
    """清空输入容器中的所有行"""
    while container.count():
        item: QLayoutItem = container.takeAt(0)
        layout: QLayout = item.layout()
        if layout:
            clear_layout(layout)
        container.removeItem(item)
