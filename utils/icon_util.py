from enum import Enum
from typing import LiteralString
from qfluentwidgets import Theme, FluentIconBase

class FluentIcon(FluentIconBase, Enum):
    CONDA = "Conda"
    NUITKA = "Nuitka"
    UV = "UV"
    
    def path(self, theme=Theme.AUTO) -> LiteralString:
        return f':/icons/{self.value}.svg'
