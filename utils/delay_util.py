# utils/delay_util.py
import threading
from typing import Callable, Any
from PySide6.QtCore import QObject, Signal

class DelayedLoader(QObject):
    """
    延迟加载工具类 - 在后台线程中执行加载任务并缓存结果
    
    参数:
        load_function: 执行加载任务的函数
        cache_key: 用于标识缓存数据的键名
    """
    # 信号: 当数据加载完成时发出
    data_loaded = Signal(str, object)
    
    def __init__(self, load_function: Callable[[], Any], cache_key: str) -> None:
        super().__init__()
        self.load_function: Callable[[], Any] = load_function
        self.cache_key: str = cache_key
        self.cached_data: Any = None
    
    def get_data(self) -> Any:
        """获取数据 - 如果已缓存则直接返回，否则启动后台加载"""
        if self.cached_data is not None:
            return self.cached_data
        # 启动后台线程加载数据
        threading.Thread(target=self._load_data, daemon=True).start()
        return None
    
    def _load_data(self) -> None:
        """在后台线程中加载数据"""
        try:
            result = self.load_function()
            self.cached_data = result
        except Exception as e:
            self.cached_data = f"加载失败: {str(e)}"
        # 发出加载完成信号
        self.data_loaded.emit(self.cache_key, self.cached_data)
