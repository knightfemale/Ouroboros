from enum import Enum
from typing import LiteralString
from qfluentwidgets import Theme, FluentIconBase

class FluentIcon(FluentIconBase, Enum):
    """ Custom icons """
    CONDA = "Conda"
    NUITKA = "Nuitka"
    
    def path(self, theme=Theme.AUTO) -> LiteralString:
        return f':/icons/{self.value}.svg'
