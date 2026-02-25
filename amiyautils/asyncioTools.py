import asyncio
import threading
import nest_asyncio

from typing import Optional, TypeVar, Coroutine, Any

T = TypeVar('T')
nest_asyncio.apply()


class EventLoop:
    _global_loop: Optional[asyncio.AbstractEventLoop] = None
    _lock = threading.Lock()

    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
            return loop
        except RuntimeError:
            if cls._global_loop is None:
                with cls._lock:
                    if cls._global_loop is None:
                        cls._global_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(cls._global_loop)
            return cls._global_loop

    @classmethod
    def run(cls, func: Coroutine[Any, Any, T]) -> T:
        return cls.event_loop().run_until_complete(func)
