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
import math
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
selected_rooms = get_multiple_elements()

if not selected_rooms:
    with try_except():
        filter_type = ISelectionFilter_Classes([Room])
        room_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_rooms = [doc.GetElement(wall) for wall in room_list]

    if not selected_rooms:
        forms.alert('No wall selected', exitscript=True)

with rvt_transaction(doc, __title__):
    for rm in selected_rooms:
        ceil_fin = rm.LookupParameter('Ceiling Finish').Set('C10')
        base_fin = rm.LookupParameter('Base Finish').Set('S04')
        flr_fin  = rm.LookupParameter('Floor Finish').Set('F14')
        wall_1   = rm.LookupParameter('Wall 1 Finish Tagged').Set('W03')
        wall_2   = rm.LookupParameter('Wall 2 Finish Tagged').Set('W03')
        wall_3   = rm.LookupParameter('Wall 3 Finish Tagged').Set('W03')
        wall_4   = rm.LookupParameter('Wall 4 Finish Tagged').Set('W03')
