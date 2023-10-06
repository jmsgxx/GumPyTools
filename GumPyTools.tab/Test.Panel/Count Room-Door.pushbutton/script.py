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


# ------------XXX get boundary of rooms XXX--------------------
# selected_room = doc.GetElement(room_element.Id)
#
# rm_boundary_segments = selected_room.GetBoundarySegments(SpatialElementBoundaryOptions())
#
# doors_in_room = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
#
#
#
# rm_curve_lst = []
#
# for segment in rm_boundary_segments:
#     for curve in segment:
#         rm_curve_lst.append(curve.GetCurve())

boundary_segments = room_element.GetBoundarySegments(SpatialElementBoundaryOptions())
curve_lst = []
for segment in boundary_segments:
    for line in segment:
        curve = line.GetCurve()
        curve_lst.append(curve)

# Retrieve doors within the room
doors_in_room = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# Check for intersection between curves and doors
door_lst = []
for segment in boundary_segments:
    for line in segment:
        curve = line.GetCurve()
    for door in doors_in_room:
        door_location = door.Location
        if isinstance(door_location, LocationCurve):
            door_curve = door_location.Curve
            intersection_result = curve.Intersect(door_curve)
            if intersection_result:
                door_lst.append(door)

print(len(door_lst))
"""

TODO not fixed figure out how to intersect the rooms and doors

"""










