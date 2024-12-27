# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
__________________________________
Author: Joven Mark Gumana

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import csv
from Snippets._convert import convert_m_to_feet
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, StairsFilter, SectionMarkFilter
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum

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

all_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

picked_rm = None
for rm in all_rooms:
    if rm.Location:
        picked_rm = rm
        break


param_set = picked_rm.Parameters

for param in param_set:
    print(param.Definition.BuiltInParameter)
    # print(param)

