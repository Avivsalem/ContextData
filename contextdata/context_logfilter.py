from logging import Filter

from contextdata import Context


class ContextLogFilter(Filter):
    """
    Filter that adds context information to log messages.
    """

    def __init__(self,
                 context: Context,
                 context_attribute_name: str = "Context",
                 include_empty_context: bool = False,
                 name=''):

        super().__init__(name=name)
        self._context = context
        self._context_attribute_name = context_attribute_name
        self._include_empty_context = include_empty_context

    def filter(self, record):
        result = super().filter(record)
        if result:
            context_dict = self._context.get_current_context()
            if context_dict or self._include_empty_context:
                setattr(record, self._context_attribute_name, context_dict)

        return result
