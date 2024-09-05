'''

    @Author: Shivraj Yelave
    @Date: 05-09-24
    @Last modified by: Shivraj Yelave
    @Last modified time: 
    @Title: Logger Code


'''

# logger_config.py

import logging


def setup_logger(name, level):

    """

    Description: 
    Set up and return a logger instance with the specified name and logging level.
    
    Parameters:
    name (str): The name of the logger instance.
    level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
    
    Returns:
    logging.Logger: Configured logger instance.

    """
    
    # Create a logger
    logger = logging.getLogger(name)
    
    # Check if the logger is already configured to avoid duplicate handlers
    if not logger.hasHandlers():
        # Description: 
        # Create a formatter for the log messages
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

        # Description: 
        # Create a file handler and set the formatter
        file_handler = logging.FileHandler('sample.log')
        file_handler.setFormatter(formatter)

        # Description: 
        # Set the logging level for the logger and add the handler
        logger.setLevel(level)
        logger.addHandler(file_handler)

    return logger

def get_debug_logger(name):

    """
    
    Description: 
    Get a logger instance configured for DEBUG level.

    Parameters:
    name (str): The name of the logger instance.

    Returns:
    logging.Logger: Logger instance set to DEBUG level.
    
    """
    
    return setup_logger(name, logging.DEBUG)

def get_info_logger(name):
    
    """
    
    Description: 
    Get a logger instance configured for INFO level.

    Parameters:
    name (str): The name of the logger instance.

    Returns:
    logging.Logger: Logger instance set to INFO level.
    
    """
    return setup_logger(name, logging.INFO)

def get_warning_logger(name):
    
    """
    
    Description: 
    Get a logger instance configured for WARNING level.

    Parameters:
    name (str): The name of the logger instance.

    Returns:
    logging.Logger: Logger instance set to WARNING level.
    
    """
    
    return setup_logger(name, logging.WARNING)

def get_error_logger(name):
    
    """
    
    Description: 
    Get a logger instance configured for ERROR level.

    Parameters:
    name (str): The name of the logger instance.

    Returns:
    logging.Logger: Logger instance set to ERROR level.
    
    """
    
    return setup_logger(name, logging.ERROR)

def get_critical_logger(name):
    
    """
    
    Description: 
    Get a logger instance configured for CRITICAL level.

    Parameters:
    name (str): The name of the logger instance.

    Returns:
    logging.Logger: Logger instance set to CRITICAL level.
    
    """
    
    return setup_logger(name, logging.CRITICAL)
