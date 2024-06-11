# -*- coding: utf-8 -*-

"""
Document Changed
__________________________________
Author: Joven Mark Gumana
"""
from Autodesk.Revit.DB import *
import sys
import csv
import os
from datetime import datetime
from Snippets.doc_event_log import add_element_log, mod_element_log, del_element_log
from pyrevit import revit, EXEC_PARAMS
import clr
clr.AddReference("System")
from System.Collections.Generic import List

sender = __eventsender__
arg = __eventargs__
doc = revit.doc

add_file_path = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\add_el_log.csv'
mod_file_path = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\mod_el_log.csv'
del_file_path = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\del_el_log.csv'

add_element_log(add_file_path)
mod_element_log(mod_file_path)
del_element_log(del_file_path)


