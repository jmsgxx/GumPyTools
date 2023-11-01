# -*- coding: utf-8 -*-

__title__ = 'Test Button'
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
import pyrevit
from pyrevit import script, forms, revit
from System.Collections.Generic import List
from datetime import datetime

import clr
clr.AddReference("System")


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

with forms.WarningBar(title='Pick an element:'):
    selected_room = revit.pick_element()

el_cat          = selected_room.Category.Name

if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)

calculator      = SpatialElementGeometryCalculator(doc)
results         = calculator.CalculateSpatialElementGeometry(selected_room)
space_solid     = results.GetGeometry()
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
    wall_list = []  # list of wall that has "FIN" on wall.Name
    mark_wall = []
    type_mark_wall = []
    desc_wall = []

    for face in space_solid.Faces:
        spatial_sub_face_list = results.GetBoundaryFaceInfo(face)
        if len(spatial_sub_face_list) == 0:
            continue

        for sub_face in spatial_sub_face_list:
            host_id = sub_face.SpatialBoundaryElement.HostElementId
            wall = doc.GetElement(host_id)
            if "FIN" in wall.Name:
                wall_list.append(wall)

    # room parameter
    room_data_set_param = selected_room.LookupParameter('Room Wall Data Set 1')

    for number, wall in enumerate(wall_list, start=1):
        # number the wall mark based on the number of the walls in the room
        wall_mark = wall.get_Parameter(BuiltInParameter.DOOR_NUMBER)
        wall_number = wall.LookupParameter('Wall Number')
        wall_mark.Set("")

    t.Commit()
# =============================================================================================




