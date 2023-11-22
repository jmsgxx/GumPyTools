# -*- coding: utf-8 -*-

__title__ = 'Wall Param to Room'
__doc__ = """
This script will first generate a number that 
will be written as a Mark instance on a wall. 
It will then copy the 'Mark', 'Type Mark', 
and 'Description', which will be set as a
Room Parameter: Wall Data Set 1 - this is 
a concatenation of the 3 Wall Parameters.

HOW TO:
1. Run Command.
2. It will prompt you to select the finish
walls to be numbered.
3. Select Room to put the info.
-----------------------------------------
v2. 22 Nov 2023
v1: 30 Oct 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
import time
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
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
    wall_list       = []  # list of wall that has "FIN" on wall.Name
    mark_wall       = []
    type_mark_wall  = []
    desc_wall       = []

    selection = uidoc.Selection
    wall_pick = selection.PickObjects(ObjectType.Element, 'Select Finish Walls')   # pickobject"S" prompts to select multiple objects

    element_ids = []
    for picked_walls in wall_pick:
        element_id = picked_walls.ElementId
        element_ids.append(element_id)

    elements = [doc.GetElement(element_id) for element_id in element_ids]

    for wall_element in elements:
        if "FIN" in wall_element.Name:
            wall_list.append(wall_element)


    for number, wall in enumerate(wall_list, start=1):
        # number the wall mark based on the number of the walls in the room
        wall_mark       = wall.get_Parameter(BuiltInParameter.DOOR_NUMBER)
        wall_number     = wall.LookupParameter('Wall Number')
        wall_mark.Set("w{}".format(number))
        wall_number.Set(wall_mark.AsValueString())

        time.sleep(2)

        # type element
        wall_type_id            = wall.GetTypeId()
        wall_type               = doc.GetElement(wall_type_id)
        wall_type_mark          = wall_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
        wall_type_description   = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)

        # append to list as string
        mark_wall.append(wall_mark.AsValueString())
        type_mark_wall.append(wall_type_mark.AsValueString())
        desc_wall.append(wall_type_description.AsValueString())

    # room selection
    with forms.WarningBar(title='Pick an element:'):
        selected_room = revit.pick_element()

    el_cat = selected_room.Category.Name
    if el_cat != 'Rooms':
        forms.alert('Just pick a Room', exitscript=True)

    # room parameter
    room_data_set_param = selected_room.LookupParameter('Room Wall Data Set 1')
    room_wall_data          = list(zip(mark_wall, type_mark_wall, desc_wall))
    room_wall_data_sorted   = sorted(room_wall_data)

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

print("ROOM NAME: {}".format(room_name.AsValueString().upper()))
print('=' * 50)
print("WALL DATA TRANSFERRED: \n {}".format(room_data_set_param.AsString()))



