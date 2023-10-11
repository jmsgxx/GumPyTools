# -*- coding: utf-8 -*-

__title__ = 'Count Room.Door'
__doc__ = """
DOESN'T WORK
This script will count doors from
the selected room and will assign
numbers on specified parameter.
__________________________________
v1: 05 Oct 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit

import clr
clr.AddReference("System")
from System.Collections.Generic import List



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc         = __revit__.ActiveUIDocument.Document
uidoc       = __revit__.ActiveUIDocument
app         = __revit__.Application
selection   = __revit__.ActiveUIDocument.Selection

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
# with Transaction(doc, __title__) as t:
#     t.Start()
#     # CHANGE HERE
#     t.Commit()

# 🟢 PICK THE ROOM
with forms.WarningBar(title='Pick an element:'):
    room_element = revit.pick_element()

element_category          = room_element.Category.Name

if element_category != 'Rooms':
    forms.alert('Please pick a Room', exitscript=True)


# ------------XXX get room XXX-------------------
phase_list = list(doc.Phases)

phase = phase_list[1]

room = room_element

doors_in_room = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

door_count = []

# Loop through all doors and check if they are in the room
for door in doors_in_room:
    # Get the rooms associated with the door
    to_room = door.ToRoom[phase]
    from_room = door.FromRoom[phase]

    # Check if either of the rooms is the selected room
    if to_room == room or from_room == room:
        door_count.append(door)


print(len(door_count))


