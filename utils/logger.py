import logging

def setup_logger(name, level=logging.INFO):
    """
    Sets up a logger with the specified name and level.
    
    Args:
        name (str): Name of the logger.
        level: Logging level (e.g., logging.INFO, logging.DEBUG).
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger