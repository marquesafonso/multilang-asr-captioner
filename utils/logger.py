import logging

# https://signoz.io/guides/python-logging-best-practices/
# Create and configure a named logger
def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger