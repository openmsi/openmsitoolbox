"""
Anything that should have associated command line arguments when anything extending it
also extends Runnable
"""

# imports
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any


class HasArguments(ABC):
    """
    Anything that has OpenMSIArgumentParser-format command line arguments
    """

    @classmethod
    @abstractmethod
    def get_command_line_arguments(cls) -> Tuple[List[str], Dict[str, Any]]:
        """
        Get the list of argument names and the dictionary of argument names/default values
        to add to the argument parser

        :return: args, a list of argument names recognized by the argument parser
        :rtype: list(str)
        :return: kwargs, a dictionary of default argument values keyed by argument names
            recognized by the argument parser
        :rtype: dict
        """
        return [], {}
