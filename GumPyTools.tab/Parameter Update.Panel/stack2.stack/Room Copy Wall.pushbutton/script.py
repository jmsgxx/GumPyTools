# -*- coding: utf-8 -*-

__title__ = 'Room Copy Wall'
__doc__ = """
This script will collect the the wall data
that was generated beforehand. This is a stand
alone command since some walls shares multiple
rooms

HOW TO:
1. Run Command.
2. A prompt will let you know the command is
executed
-----------------------------------------
v1. 22 Nov 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
import clr
from datetime import datetime
import pyrevit
from Autodesk.Revit.UI.Selection import ObjectType
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

# room selection
with forms.WarningBar(title='Pick an element:'):
    selected_room = revit.pick_element()

el_cat = selected_room.Category.Name
if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)

calculator = SpatialElementGeometryCalculator(doc)
results = calculator.CalculateSpatialElementGeometry(selected_room)
space_solid = results.GetGeometry()

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

        # type element
        wall_type_id = wall.GetTypeId()
        wall_type = doc.GetElement(wall_type_id)
        wall_type_mark = wall_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
        wall_type_description = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)

        # append to list as string
        mark_wall.append(wall_mark.AsValueString())
        type_mark_wall.append(wall_type_mark.AsValueString())
        desc_wall.append(wall_type_description.AsValueString())

    room_wall_data = list(zip(mark_wall, type_mark_wall, desc_wall))
    try:
        room_wall_data_sorted = sorted(room_wall_data, key=lambda x: int(x[0][1:]))
    except TypeError as e:
        forms.alert("{}. Means wall has no data.\nPlease use 'Number Wall' or 'Room Bound Wall'".format(e), warn_icon=True, exitscript=True)


    # initialize an empty string
    room_data_string = ""
    for item in room_wall_data_sorted:
        room_data_string += "{}\t{}\t{}\n".format(item[0], item[1], item[2])

    room_data_set_param.Set(room_data_string)

    t.Commit()
# =============================================================================================
current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')

output = pyrevit.output.get_output()
output.add_style('background {color: yellow}')
output.center()
output.resize(300, 500)
output.print_md('### Parameters Updated: {}'.format(time_stamp))

room_name = selected_room.LookupParameter('Name')

print("ROOM NAME  : {}".format(room_name.AsValueString().upper()))
print("ROOM NUMBER: {}".format(selected_room.Number))
print('=' * 50)
print("WALL DATA TRANSFERRED: \n {}".format(room_data_set_param.AsString()))
print('=' * 50)



