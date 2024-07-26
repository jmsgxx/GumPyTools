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
# all_room_tags = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_RoomTags).\
#     WhereElementIsNotElementType().ToElements()
#
# with rvt_transaction(doc, __title__):
#
#     for tag in all_room_tags:
#         room = tag.Room
#         room_bb = room.get_BoundingBox(doc.ActiveView)
#         room_center = (room_bb.Max - room_bb.Min) / 2
#
#         if room.IsPointInRoom(room_center):
#             room.Location.Point = room_center
#             tag.Location.Point = room_center

all_pipe_tags = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_PipeTags).WhereElementIsNotElementType().ToElements()

for pipe in all_pipe_tags:
    tagged_el = pipe.GetTaggedLocalElements()
    for i in tagged_el:
        print(i.Name)
