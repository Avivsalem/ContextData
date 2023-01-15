import os
import threading
import time
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Dict, Any, List, Optional

_context_var: ContextVar = ContextVar('__asyncio_context__', default={})


def get_context_id() -> str:
    """
    generates a random 16 bytes hex string
    """
    return os.urandom(8).hex() + hex(time.time_ns())[2:]


class Context(metaclass=ABCMeta):
    """
    an abstract class that represents a context
    """
    _ROOT_CONTEXT_ID_KEY = '__ROOT_CONTEXT_ID__'
    _PARENT_CONTEXT_ID_KEY = '__PARENT_CONTEXT_ID__'
    _CONTEXT_ID_KEY = '__CONTEXT_ID__'

    @abstractmethod
    def _get_current_context(self) -> Dict[str, Any]:
        """
        gets the current context dict

        :return: the current context
        """
        pass

    @abstractmethod
    def _push_context(self, new_context: Dict[str, Any]) -> Any:
        """
        pushes a new context dictionary.

        :param new_context: the new context to push
        :return: a token, used to pop the stack
        """
        pass

    @abstractmethod
    def _pop_context(self, token: Any):
        """
        pops the current context, and returns it to its former state

        :param token: the toked returned by '_push_context'
        """
        pass

    def get(self, key: str, default=None) -> Any:
        """
        gets a single key from the context

        :param key: the key to get
        :param default: a default value to return if the key doesn't exist
        :return: the value for this key in the current context or 'default' if no value exist
        """
        return self._get_current_context().get(key, default)

    @property
    def context_id(self) -> Optional[str]:
        """
        the id for this context
        """
        return self.get(self._CONTEXT_ID_KEY)

    @property
    def parent_context_id(self) -> Optional[str]:
        """
        the id of the parent of this context
        """
        return self.get(self._PARENT_CONTEXT_ID_KEY)

    @property
    def root_context_id(self) -> Optional[str]:
        """
        the id of the root context for this context
        """
        return self.get(self._ROOT_CONTEXT_ID_KEY)

    @contextmanager
    def start_context(self, **kwargs):
        """
        starts a context with some keys.
        existing keys will be overriden, new keys will be added
        :param kwargs: the key/value pairs to add to context
        """
        old_context = self._get_current_context()
        new_context = old_context.copy()
        new_context.update(kwargs)

        new_context_id = get_context_id()
        new_context[self._CONTEXT_ID_KEY] = new_context_id
        new_context[self._PARENT_CONTEXT_ID_KEY] = old_context.get(self._CONTEXT_ID_KEY, None)
        new_context.setdefault(self._ROOT_CONTEXT_ID_KEY, new_context_id)

        token = self._push_context(new_context=new_context)
        try:
            yield self
        finally:
            self._pop_context(token)

    def get_current_context(self) -> Dict[str, Any]:
        """
        returns a shallow copy of the entire current context

        :return: a shallow copy of the entire current context
        """
        return self._get_current_context().copy()


class _GlobalContext(Context):
    def __init__(self):
        self._context_stack: List[Dict[str, Any]] = []

    def _get_current_context(self):
        if not self._context_stack:
            return {}
        else:
            return self._context_stack[-1]

    def _push_context(self, new_context: Dict[str, Any]) -> Any:
        self._context_stack.append(new_context)
        return None

    def _pop_context(self, token: Any):
        if self._context_stack:
            self._context_stack.pop()


class _ThreadLocalContext(threading.local, _GlobalContext):
    pass


class _AsyncioContext(Context):
    def _get_current_context(self) -> Dict[str, Any]:
        return _context_var.get()

    def _push_context(self, new_context: Dict[str, Any]) -> Any:
        token = _context_var.set(new_context)
        return token

    def _pop_context(self, token: Any):
        _context_var.reset(token)


global_context: Context = _GlobalContext()
thread_local_context: Context = _ThreadLocalContext()
asyncio_context: Context = _AsyncioContext()
