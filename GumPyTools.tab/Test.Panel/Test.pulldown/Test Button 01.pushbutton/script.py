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
from Autodesk.Revit.DB import *
from pyrevit import forms
from datetime import datetime
import os
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application


active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

rooms = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Rooms)\
    .WhereElementIsNotElementType()\
    .ToElements()

# Dictionary to store rooms by location
room_locations = {}

# Iterate through rooms and check for redundancy
for room in rooms:
    room_location = room.Location
    if room_location and hasattr(room_location, 'Point'):
        # Convert location point to a tuple for dictionary key
        loc_key = (room_location.Point.X, room_location.Point.Y)
        if loc_key in room_locations:
            # If the location already exists, it's a redundant room
            print("Redundant room found: {}".format(room.Id))
        else:
            room_locations[loc_key] = room.Id
