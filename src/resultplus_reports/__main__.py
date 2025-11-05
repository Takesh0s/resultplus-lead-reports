"""
Entry point for running ResultPlus Reports as a module.
Example:
    python -m resultplus_reports
"""

from . import fetch_result

if __name__ == "__main__":
    print("Running ResultPlus Reports...")
    fetch_result()