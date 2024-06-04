# -*- coding: utf-8 -*-

"""
Document Changed
__________________________________
Author: Joven Mark Gumana
"""
from Snippets.doc_event_log import add_element_log
from pyrevit import revit, EXEC_PARAMS
import clr
clr.AddReference("System")
from System.Collections.Generic import List

sender = __eventsender__
arg = __eventargs__
doc = revit.doc

add_file_path = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\add_el_log.csv'
add_element_log(add_file_path)




