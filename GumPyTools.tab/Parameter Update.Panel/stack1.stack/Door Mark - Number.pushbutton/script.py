# -*- coding: utf-8 -*-

__title__ = 'Wall Tag Update'
__doc__ = """
This script will update the wall.
Number will based from the room.
Change log:
Script logic came from Room.Boundaries
node of Archilab. 
__________________________________
v2: 17 Oct 2023
v1: 16 Oct 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import forms, revit

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

walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).ToElements()
rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

with forms.WarningBar(title='Pick an element:'):
    selected_room = revit.pick_element()

el_cat          = selected_room.Category.Name

if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    options = SpatialElementBoundaryOptions()

    # Get all the walls linked to the room
    linked_walls = []
    for boundary_lst in selected_room.GetBoundarySegments(options):
        for boundary in boundary_lst:
            wall = doc.GetElement(boundary.ElementId)
            if isinstance(wall, Wall):
                linked_walls.append(wall)

    # Assign a unique mark value to each wall
    for i, wall in enumerate(linked_walls):
        param = wall.get_Parameter(BuiltInParameter.DOOR_NUMBER)
        if param:
            param.Set('w{}'.format(i + 1))  # The mark values will be 'w1', 'w2', 'w3', etc.

    t.Commit()