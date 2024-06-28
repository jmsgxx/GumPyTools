# -*- coding: utf-8 -*-

"""
Document Opening Log
__________________________________
Author: Joven Mark Gumana
"""
from pyrevit import revit, EXEC_PARAMS
from Snippets.doc_event_log import doc_event_logger
from Snippets.notion_docop_logger import notion_doc_open_logger
import time

sender = __eventsender__
arg = __eventargs__
doc = revit.doc

filepath = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\log_info\doc_open_log.csv'
notion_doc_open_logger(filepath)


# TODO: currently its only getting the opened doc log from csv, might change it to get the synced file itself
