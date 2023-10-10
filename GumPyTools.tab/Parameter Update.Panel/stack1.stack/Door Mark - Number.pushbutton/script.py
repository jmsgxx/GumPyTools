# -*- coding: utf-8 -*-

__title__ = 'Door Mark-Number'
__doc__ = """
This script will update the Door Mark
and Door Number based on the number
of instances inside the room.
__________________________________
v1 = 10 Oct 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms

import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================




# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

all_phase = list(doc.Phases)
phase = (all_phase[1])
all_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # Group doors by room
    doors_by_room = {}
    for door in all_doors:
        room = door.ToRoom[phase]
        if room:
            room_number = room.Number
            if room_number not in doors_by_room:
                doors_by_room[room_number] = []
            doors_by_room[room_number].append(door)

    # Generate a sequence for each group of doors and assign door numbers
    for room_number, doors in doors_by_room.items():
        for i, door in enumerate(doors):
            door_sequence = str(i + 1).zfill(2)
            door_mark = "{}-{}".format(room_number, door_sequence)
            door_number = "D{}".format(door_sequence)
            door.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set(door_mark)
            door.LookupParameter('Door Number').Set(door_number)

    t.Commit()