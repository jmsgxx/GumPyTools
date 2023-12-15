# -*- coding: utf-8 -*-

__title__ = 'Door from Room'
__doc__ = """
This script transfers the Door parameters to Room.
It will also create the Door Mark and Door Number
by counting all the selected doors it will update
it's parameter automatically.

HOW TO:
- Click the command
- Select the desired room. Confirmation will pop up.
- Select the door/s that you want.
- A print statement will confirm that the
  selected doors was included on the list.
  If not it will give an error print statement.
----------------------------------------------------
v3: 22 Nov 2023 - picked doors instead of checkbox
v2: 29 Oct 2023
v1: 27 Oct 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from pyrevit import forms, revit
import clr
from datetime import datetime
import pyrevit
import sys
from Snippets import _x_selection

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
selection = uidoc.Selection     # type:Selection

current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')

# =============================================================================================================
# 🔵 ROOM

filter_type = _x_selection.ISelectionFilter_Classes([Room])
selected_element = selection.PickObject(ObjectType.Element, filter_type, "Select Room")

if not selected_element:
    selected_element = selection.PickObject(ObjectType.Element, filter_type, "Select Room")
    if not selected_element:
        forms.alert("Select Room. Try again", exitscript=True)

selected_room = doc.GetElement(selected_element)
forms.alert("Select door and press finish", title="Door Selection", warn_icon=False, exitscript=False, ok=True)
# ===========================================================================================================
# 🔵 DOOR

try:
    door_filter = _x_selection.ISelectionFilterCatName(['Doors'])
    door_elements = selection.PickObjects(ObjectType.Element, door_filter, 'Select Doors')
except Exception as e:
    forms.alert(str(e), exitscript=True)

door_list = [doc.GetElement(el) for el in door_elements]

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
# with revit.Transaction(doc, __title__):
with Transaction(doc, __title__) as t:
    t.Start()

    # 🟨 ASSIGN DOOR MARK AND NUMBERS
    doors_by_room = {}
    for door in door_list:
        room = selected_room
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

    # 🟡 COPYING DOORS PARAM TO ROOM
    # GET THE LIST TO BE SET
    room_door_marks_list = []
    room_door_clear_heights_list = []
    room_door_clear_widths_list = []
    room_door_remarks_list = []

    for door in door_list:
        # 🟦 GET DOOR PARAMETERS TO COPY
        # -------xxx get the type first xxx------
        dr_type_id      = door.GetTypeId()
        door_symbol     = doc.GetElement(dr_type_id)
        # parameter
        door_mark_param                = door.LookupParameter('Door Number')
        door_height_param       = door_symbol.LookupParameter('Door Designated Clear Height')
        door_width1_param       = door_symbol.LookupParameter('Door Designated Clear Width 1')
        door_width2_param       = door_symbol.LookupParameter('Door Designated Clear Width 2')
        door_remarks_param      = door_symbol.LookupParameter('Door Remarks')

        # 🟨 add string method
        door_mark           = door_mark_param.AsValueString()
        door_height         = door_height_param.AsValueString()
        if door_width1_param and door_width2_param:
            door_width1     = door_width1_param.AsValueString()
            door_width2     = door_width2_param.AsValueString()
            # append
            room_door_clear_widths_list.append(door_width1 + "+" + door_width2)
        else:
            door_width1     = door_width1_param.AsValueString()
            # append
            room_door_clear_widths_list.append(door_width1)
        door_remarks        = door_remarks_param.AsValueString()

        # Append door parameters to lists
        room_door_marks_list.append(door_mark)
        room_door_clear_heights_list.append(door_height)
        room_door_remarks_list.append(door_remarks)

    # Convert lists to strings
    room_door_marks_str                 = '\n\n'.join(room_door_marks_list)
    room_door_clear_heights_str         = '\n\n'.join(room_door_clear_heights_list)
    room_door_clear_widths_str          = '\n\n'.join(room_door_clear_widths_list)
    room_door_remarks_str               = '\n\n'.join(room_door_remarks_list)

    # 🟪 ROOM PARAMETERS
    room                        = selected_room
    room_door_marks             = room.LookupParameter('Room Door Marks')
    room_door_clear_widths      = room.LookupParameter('Room Door Clear Widths')
    room_door_clear_heights     = room.LookupParameter('Room Door Clear Heights')
    room_door_remarks           = room.LookupParameter('Room Door Description')

    # ⭕SET
    # ---------------XXX--------------------
    # DOOR MARKS
    room_door_marks.Set(room_door_marks_str)
    room_door_clear_heights.Set(room_door_clear_heights_str)
    room_door_clear_widths.Set(room_door_clear_widths_str)
    room_door_remarks.Set(room_door_remarks_str)

    t.Commit()
# =====================================================================================================================
output = pyrevit.output.get_output()
output.center()
output.resize(300, 500)
# output.print_md('### Parameters Updated: {}'.format(time_stamp))

room_name = selected_room.LookupParameter('Name')
# print("ROOM NAME: {}".format(room_name.AsValueString().upper()))
# print("ROOM NUMBER: {}".format(room_number))
# print('=' * 50)
# print("DOOR NUMBER: \n" + '\n'.join(room_door_marks_list))
# print('=' * 50)
# print("DOOR CLEAR HEIGHT: \n" + '\n'.join(room_door_clear_heights_list))
# print('=' * 50)
# print("DOOR CLEAR WIDTH: \n" + '\n'.join(room_door_clear_widths_list))
# print('=' * 50)
# print("DOOR DESCRIPTION: \n" + '\n' + '\n\n'.join(room_door_remarks_list))
forms.alert("Parameters Updated", exitscript=False, warn_icon=False)





