"""
The main function for the Gamera_mei Gamera toolkit

This is a good place for top-level functions, such as things
that would be called from the command line.

This module is not strictly necessary.
"""

from time import sleep
from sys import stdout

def main():
    """This is a top-level function for the toolkit.  It doesn't
really do anything..."""
    stdout.write("Processing (well, not really...)")
    for i in range(5):
        stdout.write(".")
        stdout.flush()
        sleep(1)

