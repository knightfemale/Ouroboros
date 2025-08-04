# styles/default.py
BACKGROUND_STYLE = """
    background-color: white;
"""

TITLE_STYLE = """
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333333;
"""

GROUPBOX_STYLE = """
    QGroupBox {
        border: 1px solid #c0c0c0;
        border-radius: 5px;
        margin-top: 1ex;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        padding-right: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 3px;
        color: #2196f3;
        font-weight: bold;
    }
"""

ENV_BUTTON_STYLE = """
    PushButton {
        background-color: #2196f3;
        color: white;
    }
    PushButton:hover {
        background-color: #1976d2;
    }
    PushButton:pressed {
        background-color: #0d47a1;
    }
"""

PACK_BUTTON_STYLE = """
    PushButton {
        background-color: #a855f7;
        color: white;
    }
    PushButton:hover {
        background-color: #9c27b0;
    }
    PushButton:pressed {
        background-color: #7b1fa2;
    }
"""

ADD_BUTTON_STYLE = """
    PushButton {
        background-color: #4caf50;
        color: white;
    }
    PushButton:hover {
        background-color: #388e3c;
    }
    PushButton:pressed {
        background-color: #1b5e20;
    }
"""

REMOVE_BUTTON_STYLE = """
    PushButton {
        background-color: #f44336;
        color: white;
    }
    PushButton:hover {
        background-color: #d32f2f;
    }
    PushButton:pressed {
        background-color: #b71c1c;
    }
"""
