# -*- coding: utf-8 -*-

__title__ = 'Test Button 03'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script
import codecs
import csv
from Snippets.notion_com_logger import notion_com_logger
from Snippets.notion_docop_logger import notion_doc_open_logger
from Snippets._convert import convert_internal_to_m2
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection


# ======================================================================================================
output = script.get_output()
output.center()

file_path = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\log_info\doc_sync_log.csv'
with open(file_path, 'r') as csvfile:
    data = [line.strip().split(',') for line in csvfile]


output.resize(800, 700)
output.print_table(table_data=data,
                   title='Document Sync Log',
                   columns=['User', 'Computer', 'Model', 'Date', 'Time'],
                   formats=['', '', '', '', ''])

# data = csvfile.readlines()[1:]
# for line in data:
#     part_item = line.strip().split(',')
#     formatted = ("User: {}\n"
#                  "Computer: {}\n"
#                  "Model: {}\n"
#                  "Date: {}\n"
#                  "Time: {}\n")\
#         .format(part_item[0], part_item[1], part_item[2], part_item[3], part_item[4])
#     print('=' * 20)
#     print(formatted)
