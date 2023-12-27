import logging


class Logger():
    def __init__(self, log_file=None):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        self.log_file = log_file
        self.logger_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def set_logger(self, level):
        handlers=[ logging.StreamHandler() ]
        if self.log_file is not None:
            handlers.append(logging.FileHandler(self.log_file))

        logging.basicConfig(
            level=level,
            format=self.logger_formatter,
            handlers=handlers
        )

    def info(self, msg):
        self.set_logger(logging.INFO)

        logger = logging.getLogger()
        logger.info(msg)

    def error(self, msg):
        self.set_logger(logging.ERROR)

        logger = logging.getLogger()
        logger.error(msg)


    
