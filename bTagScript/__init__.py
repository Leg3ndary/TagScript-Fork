"""
This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license,
visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

This fork was made by _Leg3ndary and contains everything he thought should be added to tagscript. Hope you enjoy!
"""

from collections import namedtuple

from .adapter import *
from .block import *
from .exceptions import *
from .interface import *
from .interpreter import *
from .utils import *
from .verb import Verb

__version__ = "4.0.0"


class VersionInfo(namedtuple("VersionInfo", "major minor micro")):
    """
    Version information.

    Attributes
    ----------
    major: int
        Major version number.
    minor: int
        Minor version number.
    micro: int
        Micro version number.
    """

    __slots__ = ()

    def __str__(self):
        """
        Returns a string representation of the version information.

        Returns
        -------
        str
            String representation of the version information.
        """
        return "{major}.{minor}.{micro}".format(**self._asdict())

    @classmethod
    def from_str(cls, version):
        """
        Returns a VersionInfo instance from a string.

        Parameters
        ----------
        version: str
            String representation of the version information.

        Returns
        -------
        VersionInfo
            Version information.
        """
        return cls(*map(int, version.split(".")))


version_info = VersionInfo.from_str(__version__)
