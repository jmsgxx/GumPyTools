# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._x_selection import ISelectionFilter_Classes
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from pyrevit import forms
import pyrevit
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List


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
selection = uidoc.Selection     # type: Selection

# 1️⃣ COLLECT ALL SHEETS
sheet_collection = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()

# -------------------------------------------------------------------------------
# 🟢 PREPARE ROOM SELECTION
selected_rooms = [doc.GetElement(el_id) for el_id in selection.GetElementIds()]
if not selected_rooms:
    filter_type = ISelectionFilter_Classes([Room])
    selected_element = selection.PickObjects(ObjectType.Element, filter_type, "Select Room")
    selected_rooms = [doc.GetElement(el) for el in selected_element]
    if not selected_rooms:
        forms.alert("Select room.", exitscript=True)

room_name = None
room_number = None

# VIEW SHEET
room_sheets = {}
for sheet in sheet_collection:  # type: ViewSheet
    sheet_number = sheet.SheetNumber
    sheet_name = sheet.Name
    viewport_id = sheet.GetAllViewports()  # returns an id
    for ids in viewport_id:
        viewport = doc.GetElement(ids)  # type: Viewport
        view_id = viewport.ViewId

        view = doc.GetElement(view_id)  # type: View
        if view.ViewType == ViewType.FloorPlan:
            # GET THE ROOM
            for room in selected_rooms:     # type: Room
                room_name = room.LookupParameter('Room_Name_BLP').AsString()
                room_number = room.Number
                room_key = "{} - {}".format(room_name, room_number)
                if room_key not in room_sheets:
                    room_sheets[room_key] = []  # Initialize list for the room
                room_sheets[room_key].append((sheet_number, sheet_name))


output = pyrevit.output.get_output()
output.center()
output.resize(600, 750)

for room, sheets in room_sheets.items():
    print('-' * 50)
    print(room)
    print('-' * 50)
    for item in sorted(sheets):
        print("{} - {}".format(*item))
    print("\n")
    print('=' * 50)

