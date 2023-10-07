# -*- coding: utf-8 -*-

__title__ = 'Count Room.Door'
__doc__ = """
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


# ------------XXX get room XXX--------------------
selected_room = doc.GetElement(room_element.Id)

doors_in_room = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# Retrieve doors within the room


def is_inside(b1, b2):
    # Check if bounding box b1 is inside bounding box b2
    return (b2.Min.X <= b1.Min.X and
            b2.Min.Y <= b1.Min.Y and
            b2.Min.Z <= b1.Min.Z and
            b2.Max.X >= b1.Max.X and
            b2.Max.Y >= b1.Max.Y and
            b2.Max.Z >= b1.Max.Z)


retrieved_doors = []

for door in doors_in_room:
    # Check if the FamilyInstance is a door
    if door.Category.Name == 'Doors':
        # Get the BoundingBox of the DoorInstance
        door_bounding_box = door.get_BoundingBox(None)

        # Check if the door's bounding box is inside the room's bounding box
        if is_inside(door_bounding_box, selected_room.BoundingBox):
            retrieved_doors.append(door)


print(retrieved_doors)

"""

TODO not fixed figure out how to intersect the rooms and doors

"""










