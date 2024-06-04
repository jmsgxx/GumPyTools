# -*- coding: utf-8 -*-

"""
Document Opening Log
__________________________________
Author: Joven Mark Gumana
"""

from pyrevit import revit, EXEC_PARAMS
from Snippets.doc_event_log import doc_event_logger

sender = __eventsender__
arg = __eventargs__
doc = revit.doc

filepath = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\doc_open_log.csv'
doc_event_logger(filepath)
