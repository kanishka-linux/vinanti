import logging

def log_function(name):
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    #fmt = '%(asctime)-15s::%(module)s:%(funcName)s: %(levelname)-7s - %(message)s'
    #formatter_ch = logging.Formatter(fmt)
    fmt = '%(levelname)s::%(module)s::%(funcName)s: %(message)s'
    formatter_ch = logging.Formatter(fmt)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter_ch)
    logger = logging.getLogger(name)
    logger.addHandler(ch)
    return logger
