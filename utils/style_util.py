# styles/default.py
from typing import Dict, Self

# =============== 模板 ===============

BACKGROUND_STYLE: str = """
    background-color: white;
"""

TITLE_STYLE: str = """
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333333;
"""

LABLE_STYLE: str = """
    color: {text};
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
DEFAULT_THEME: Dict[str, str] = {
    "light": "#00bbc9",
    "dark": "#009faa",
    "darker": "#00868f",
}

RED_THEME: Dict[str, str] = {
    "light": "#f44336",
    "dark": "#d32f2f",
    "darker": "#b71c1c",
}

ORANGE_THEME: Dict[str, str] = {
    "light": "#ff9800",
    "dark": "#f57c00",
    "darker": "#ef6c00",
}

YELLOW_THEME: Dict[str, str] = {
    "light": "#ffc107",
    "dark": "#ffb300",
    "darker": "#ffa000",
}

GREEN_THEME: Dict[str, str] = {
    "light": "#4caf50",
    "dark": "#388e3c",
    "darker": "#1b5e20",
}

BLUE_THEME: Dict[str, str] = {

    "light": "#42A5F5",
    "dark": "#1976D2",
    "darker": "#0D47A1",
}

INDIGO_THEME: Dict[str, str] = {
    "light": "#5C6BC0",
    "dark": "#3949AB",
    "darker": "#1A237E",
}

PURPLE_THEME: Dict[str, str] = {
    "light": "#a855f7",
    "dark": "#9c27b0",
    "darker": "#7b1fa2",
}

# =============== 单例 ===============

class Style():
    def __init__(self: Self, theme: Dict[str, str]) -> None:
        self.theme: Dict[str, str] = theme
    
    def get_lable_style(self: Self) -> str:
        lable_style: str = LABLE_STYLE.format(
            text = self.theme["dark"],
        )
        return lable_style
    
    def get_groupbox_style(self: Self) -> str:
        groupbox_style: str = GROUPBOX_STYLE.format(
            groupbox = self.theme["dark"],
        )
        return groupbox_style

    def get_button_style(self: Self) -> str:
        button_style: str = BUTTON_STYLE.format(
            button_normal = self.theme["dark"],
            button_hover = self.theme["light"],
            button_pressed = self.theme["darker"],
        )
        return button_style

default_style: Style = Style(DEFAULT_THEME)
red_style: Style = Style(RED_THEME)
orange_style: Style = Style(ORANGE_THEME)
yellow_style: Style = Style(YELLOW_THEME)
green_style: Style = Style(GREEN_THEME)
blue_style: Style = Style(BLUE_THEME)
indigo_style: Style = Style(INDIGO_THEME)
purple_style: Style = Style(PURPLE_THEME)
