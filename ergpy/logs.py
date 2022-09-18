"""
Logging utility
===============

Utility functions to simplify logging

AUTHOR
    rafidini@GitHub

CREATED AT
    Sun. 18 Sep. 2022
"""
# External packages
import logging

# Constants
LOG_FORMAT: str = '%(asctime)s %(levelname)s - [ergpy] - %(message)s'

# Functions
def setup_logs_env():
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(format=LOG_FORMAT)
