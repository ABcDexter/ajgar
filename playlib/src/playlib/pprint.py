import pprint
from typing import Any
##################################################################
# This is a playlib module for pretty printing data in Python.
##################################################################

class PPrinter(object):
    """
    A class for pretty printing data structures in Python.
    """

    def __init__(self, indent=4, width=80):
        """
        Initializes the PrettyPrinter with specified indentation and width.

        :param indent: Number of spaces to use for indentation.
        :param width : Maximum width of the output.
        """
        assert isinstance(indent, int) and indent >= 0, "Indent must be a non-negative integer."
        assert isinstance(width, int) and width > 0, "Width must be a positive integer."

        self.indent = indent
        self.width = width

    def pretty_print(self, data: Any) -> None:
        """
        Pretty prints the given data structure.

        :param data: The data structure to be pretty printed.
        """
        pp = pprint.PrettyPrinter(indent=self.indent, width=self.width)
        pp.pprint(data)