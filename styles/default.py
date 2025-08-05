# styles/default.py
from typing import Dict, Self

# =============== 模板 ===============

BACKGROUND_STYLE = """
    background-color: white;
"""

TITLE_STYLE: str = """
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333333;
"""

GROUPBOX_STYLE: str = """
    QGroupBox {{
        border: 1px solid #c0c0c0;
        border-radius: 5px;
        margin-top: 1ex;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        padding-right: 10px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 3px;
        color: {groupbox};
        font-weight: bold;
    }}
"""

BUTTON_STYLE: str = """
    PushButton {{
        background-color: {button_normal};
        color: white;
    }}
    PushButton:hover {{
        background-color: {button_hover};
    }}
    PushButton:pressed {{
        background-color: {button_pressed};
    }}
"""

# =============== 主题 ===============

RED_THEME: Dict[str, str] = {
    "groupbox": "#f44336",
    "button_normal": "#f44336",
    "button_hover": "#d32f2f",
    "button_pressed": "#b71c1c",
}

ORANGE_THEME: Dict[str, str] = {
    "groupbox": "#ff9800",
    "button_normal": "#ff9800",
    "button_hover": "#f57c00",
    "button_pressed": "#ef6c00",
}

YELLOW_THEME: Dict[str, str] = {
    "groupbox": "#ffc107",
    "button_normal": "#ffc107",
    "button_hover": "#ffb300",
    "button_pressed": "#ffa000",
}

GREEN_THEME: Dict[str, str] = {
    "groupbox": "#4caf50",
    "button_normal": "#4caf50",
    "button_hover": "#388e3c",
    "button_pressed": "#1b5e20",
}

BLUE_THEME: Dict[str, str] = {
    "groupbox": "#2196f3",
    "button_normal": "#2196f3",
    "button_hover": "#1976d2",
    "button_pressed": "#0d47a1",
}

INDIGO_THEME: Dict[str, str] = {
    "groupbox": "#3f51b5",
    "button_normal": "#3f51b5",
    "button_hover": "#303f9f",
    "button_pressed": "#1a237e",
}

PURPLE_THEME: Dict[str, str] = {
    "groupbox": "#a855f7",
    "button_normal": "#a855f7",
    "button_hover": "#9c27b0",
    "button_pressed": "#7b1fa2",
}

# =============== 单例 ===============

class Style():
    def __init__(self: Self, theme: Dict[str, str]) -> None:
        self.theme: Dict[str, str] = theme
    
    def get_groupbox_style(self: Self) -> str:
        groupbox_style: str = GROUPBOX_STYLE.format(
            groupbox = self.theme["groupbox"],
        )
        return groupbox_style

    def get_button_style(self: Self) -> str:
        button_style: str = BUTTON_STYLE.format(
            button_normal = self.theme["button_normal"],
            button_hover = self.theme["button_hover"],
            button_pressed = self.theme["button_pressed"],
        )
        return button_style

red_style: Style = Style(RED_THEME)
orange_style: Style = Style(ORANGE_THEME)
yellow_style: Style = Style(YELLOW_THEME)
green_style: Style = Style(GREEN_THEME)
blue_style: Style = Style(BLUE_THEME)
indigo_style: Style = Style(INDIGO_THEME)
purple_style: Style = Style(PURPLE_THEME)
