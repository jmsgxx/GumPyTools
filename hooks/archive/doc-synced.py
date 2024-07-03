# -*- coding: utf-8 -*-

"""
Document Syncing Log
__________________________________
Author: Joven Mark Gumana
"""
from pyrevit import revit, EXEC_PARAMS
from Snippets.doc_event_log import doc_event_logger
from Snippets.notion_sync_logger import notion_sync_logger
import time

sender = __eventsender__
arg = __eventargs__
doc = revit.doc



