# -*- coding: utf-8 -*-

__title__ = 'Door Param to Room'
__doc__ = """
This script transfers the Door parameters to Room.
It will also create the Door Mark and Door Number
by counting all the selected doors in the seleceted
room and assigning numbers.

HOW TO:
- Click the command
- Select the room you'd want the information
  to be pasted
- Select the doors that you want
- A print statement will confirm that the
  selected doors was included on the list.
----------------------------------------------------
v2: 29 Oct 2023
v1: 27 Oct 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import forms, revit
import clr
from datetime import datetime
import pyrevit
from pyrevit import script

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

current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')
output = pyrevit.output.get_output()
output.center()
output.resize(300, 500)

all_doors = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
active_doors = [door for door in all_doors if door.Name != 'STANDARD']

# 🔵 ROOM
# =============================================================================================================
with forms.WarningBar(title='Pick an element:'):
    selected_room = revit.pick_element()

el_cat          = selected_room.Category.Name

if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)

# ===========================================================================================================
# 🔵 DOOR
# door_list = forms.SelectFromList.show(active_doors, multiselect=True, name_attr='Name', button_name='Select Doors')

door_pick = uidoc.Selection.PickObjects(ObjectType.Element, 'Select Doors')

door_ids = []
for single_door in door_pick:
    door_el_id = single_door.ElementId
    door_ids.append(door_el_id)

door_list = [doc.GetElement(dr_id) for dr_id in door_ids]

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
    #
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

output.print_md('### Parameters Updated: {}'.format(time_stamp))

room_name = selected_room.LookupParameter('Name')

print("ROOM NAME: {}".format(room_name.AsValueString().upper()))
print('=' * 50)
print("DOOR NUMBER: \n" + '\n'.join(room_door_marks_list))
print('=' * 50)
print("DOOR CLEAR HEIGHT: \n" + '\n'.join(room_door_clear_heights_list))
print('=' * 50)
print("DOOR CLEAR WIDTH: \n" + '\n'.join(room_door_clear_widths_list))
print('=' * 50)
print("DOOR DESCRIPTION: \n" + '\n' + '\n\n'.join(room_door_remarks_list))





