__version__ = "1.2.1"
__author__ = "Nyaundi Brian"

from Constants import Constants
from Instagram import Instagram
from InstagramException import InstagramException
from InstagramRegistration import InstagramRegistration
from SignatureUtils import SignatureUtils
from Utils import *
from http import *

__all__ = ["Constants", "Instagram", "InstagramException", "InstagramRegistration", "http", "Utils"]
