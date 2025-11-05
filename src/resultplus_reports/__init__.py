"""
ResultPlus Reports Package

Provides diagnostic scripts and utilities for interacting with the Helena CRM API,
including data fetching, endpoint discovery, and report generation.
"""

__version__ = "1.0.0"
__author__ = "Luiz Phillipe"
__email__ = "your.email@example.com"

from .fetch_result import main as fetch_result
from .generate_report import main as generate_report