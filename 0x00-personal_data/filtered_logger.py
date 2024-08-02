#!/usr/bin/env python3
"""
filter-datum
"""


import re


def filter_datum(fields, redaction, message, separator):
    """
    filter datum
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
