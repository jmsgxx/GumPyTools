# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB.Architecture import Room
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Autodesk.Revit.DB import *
import pyrevit
from pyrevit import forms
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List
from Snippets._context_manager import rvt_transaction, try_except

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# all_phases  = [doc.Phases]
# phase = all_phases[-1]


# Get all doors in the selection
doors = get_multiple_elements()

# Get the phase (you'll need to replace 'Phase Name' with the name of the phase you're interested in)
phases = FilteredElementCollector(doc).OfClass(Phase).ToElements()
phase = next((x for x in phases if x.Name == 'MWP2'), None)
if not phase:
    forms.alert("No Phase input. Check the phase of the object and try again.", exitscript=True)


to_rm       = []
from_rm     = []

# Iterate over doors
for door in doors:
    # if hasattr(door, "FromRoom") and isinstance(phase, Phase):
    #     with try_except():
    to_rm.append(door.ToRoom[phase])
    from_rm.append(door.FromRoom[phase])

for rm in to_rm:
    room_name = rm.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    print(room_name)
print("-" * 50)
for rm in from_rm:
    if rm:
        room_name = rm.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
        print(room_name)
