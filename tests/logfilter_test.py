import asyncio
import logging
import uuid

from contextdata import ContextLogFilter, global_context, thread_local_context, asyncio_context


class TestHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


async def log_async(logger: logging.Logger):
    with asyncio_context.start_context(test=3):
        logger.debug('test log')


def test_sanity():
    global_context_attr_name = 'global_context'
    thread_local_context_attr_name = 'thread_local_context'
    asyncio_context_attr_name = 'asyncio_context'
    handler = TestHandler()
    logger = logging.getLogger(str(uuid.uuid4()))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    handler.addFilter(ContextLogFilter(context=global_context, context_attribute_name=global_context_attr_name))
    handler.addFilter(
        ContextLogFilter(context=thread_local_context, context_attribute_name=thread_local_context_attr_name))
    handler.addFilter(ContextLogFilter(context=asyncio_context, context_attribute_name=asyncio_context_attr_name))
    with global_context.start_context(test=1):
        with thread_local_context.start_context(test=2):
            asyncio.run(log_async(logger))

    assert len(handler.records) == 1
    record = handler.records[0]
    global_dict = getattr(record, global_context_attr_name)
    thread_local_dict = getattr(record, thread_local_context_attr_name)

    assert global_dict['test'] == 1
    assert thread_local_dict['test'] == 2


def test_empty_context():
    global_context_attr_name = 'global_context'
    thread_local_context_attr_name = 'thread_local_context'
    handler = TestHandler()
    logger = logging.getLogger(str(uuid.uuid4()))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    handler.addFilter(ContextLogFilter(context=global_context,
                                       context_attribute_name=global_context_attr_name))
    handler.addFilter(ContextLogFilter(context=thread_local_context,
                                       context_attribute_name=thread_local_context_attr_name,
                                       include_empty_context=True))

    logger.debug("test log")

    assert len(handler.records) == 1
    record = handler.records[0]
    assert not hasattr(record, global_context_attr_name)
    thread_local_dict = getattr(record, thread_local_context_attr_name)
    assert not thread_local_dict
