# -*- coding: utf-8 -*-

__title__ = 'Door Param to Room'
__doc__ = """
Transfer door parameters to made up
door parameters for RIL. No need to
select room, just click and it will
update the entire model.
__________________________________
v1: 27 Oct 2023
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

# 🟢 GET THE DOORS IN VIEW
all_phase = list(doc.Phases)
phase = (all_phase[1])


all_doors = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
active_doors = [door for door in all_doors if door.Name != 'STANDARD']
# selected_room = forms.select_views(title="Select Room")
with forms.WarningBar(title='Pick an element:'):
    selected_room = revit.pick_element()

el_cat          = selected_room.Category.Name

if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)
door_list = forms.SelectFromList.show(active_doors, multiselect=True, name_attr='Name', button_name='Select Doors')

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    for door in active_doors:

        # room = door.ToRoom[phase]

        # if room is not None:
        #     room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME)
        #     if room_name is not None:
        #         room_name_value = room_name.AsValueString()
        #         print(room_name_value)

        # 🟦 GET DOOR PARAMETERS TO COPY
        if door:
            # -------xxx get the type first xxx------
            dr_type_id      = door.GetTypeId()
            door_symbol     = doc.GetElement(dr_type_id)
            # parameter
            door_mark_param = door.LookupParameter('Door Number')
            door_height_param = door_symbol.LookupParameter('Door Designated Clear Height')
            door_width1_param = door_symbol.LookupParameter('Door Designated Clear Width 1')
            door_width2_param = door_symbol.LookupParameter('Door Designated Clear Width 2')
            door_remarks_param = door_symbol.LookupParameter('Door Remarks')

            if door_mark_param is not None:
                door_mark = door_mark_param.AsValueString()
            if door_height_param is not None:
                door_height = door_height_param.AsValueString()
            if door_width1_param is not None:
                door_width1 = door_width1_param.AsValueString()
            if door_width2_param is not None:
                door_width2 = door_width2_param.AsValueString()
            if door_remarks_param is not None:
                door_remarks = door_remarks_param.AsValueString()

        # 🟪 ROOM PARAMETERS
        room = selected_room
        if room is not None:
            room_door_marks = room.LookupParameter('Room Door Marks')
            room_door_clear_widths = room.LookupParameter('Room Door Clear Widths')
            room_door_clear_heights = room.LookupParameter('Room Door Clear Heights')
            room_door_remarks = room.LookupParameter('Room Door Description')

            # SET
            if room_door_marks is not None and door_mark is not None:
                current_marks = room_door_marks.AsString()
                if current_marks is not None:
                    room_door_marks.Set(current_marks + door_mark + "\n\n")
                else:
                    room_door_marks.Set(door_mark + "\n\n")

            if room_door_clear_widths is not None and door_width1 is not None:
                current_widths = room_door_clear_widths.AsString()
                try:
                    if current_widths is not None:
                        if door_width2:
                            room_door_clear_widths.Set(current_widths + door_width1 + "+" + door_width2 + "\n\n")
                        else:
                            room_door_clear_widths.Set(current_widths + door_width1 + "\n\n")
                    else:
                        if door_width2:
                            room_door_clear_widths.Set(door_width1 + "+" + door_width2 + "\n\n")
                        else:
                            room_door_clear_widths.Set(door_width1 + "\n\n")
                except:
                    continue


            if room_door_clear_heights is not None and door_height is not None:
                current_heights = room_door_clear_heights.AsString()
                try:
                    room_door_clear_heights.Set(current_heights + door_height + "\n\n")
                except:
                    continue

            if room_door_remarks is not None and door_remarks is not None:
                current_remarks = room_door_remarks.AsString()
                room_door_remarks.Set(current_remarks + door_remarks + "\n")

    t.Commit()





