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
from System.Collections.Generic import List, HashSet

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
current_level = active_level.Id
level_filter = ElementLevelFilter(current_level)

all_phase = list(doc.Phases)
phase = all_phase[-1]
# phase = None
# for i in all_phase:
#     if i.Name == 'MWP2':
#         phase = i

all_doors_on_level = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WherePasses(level_filter).WhereElementIsNotElementType().ToElements()

# with rvt_transaction(doc, __title__):
#     for index, door in enumerate(all_doors_on_level, start=1):
#         room = door.FromRoom[phase]
#         mark_param = door.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
#         if room:
#             room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
#             if room_name:
#                 mark_param.Set('{}-{}'.format('A', str(index).zfill(2)))
#                 print(mark_param.AsString())

sorted_doors = sorted(all_doors_on_level, key=lambda x: x.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString())

with rvt_transaction(doc, __title__):
    for index, value in enumerate(sorted_doors, start=1):
        comment_param = value.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
        new_value = '{}-{}'.format('AA', str(index).zfill(2))
        comment_param.Set(new_value)
