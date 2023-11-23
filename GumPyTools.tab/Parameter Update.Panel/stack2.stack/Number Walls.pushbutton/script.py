# -*- coding: utf-8 -*-

__title__ = 'Number Walls'
__doc__ = """
This script will just number wall.
A stand alone command because some
walls shares multiple rooms.
It has to be done manually disascco-
ciated with the Room command.
__________________________________
HOW TO:
1. Run the command.
2. Select the walls. If it happened
that you selected wall that shouldn't
be included, as long as the wall has "FIN"
to it's name it will number itself.
==================================
v1: 22 Nov 2023
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
    wall_list           = []  # list of wall that has "FIN" on wall.Name
    mark_wall           = []
    type_mark_wall      = []
    desc_wall           = []
    wall_number_list    = []

    selection = uidoc.Selection
    wall_pick = selection.PickObjects(ObjectType.Element, 'Select Finish Walls')   # pickobject"S" prompts to select multiple objects

    element_ids = []
    for picked_walls in wall_pick:
        element_id = picked_walls.ElementId
        element_ids.append(element_id)

    elements = [doc.GetElement(element_id) for element_id in element_ids]

    for wall_element in elements:
        if wall_element:
            if "FIN" in wall_element.Name:
                wall_list.append(wall_element)

    for number, wall in enumerate(wall_list, start=1):
        # number the wall mark based on the number of the walls in the room
        wall_mark       = wall.get_Parameter(BuiltInParameter.DOOR_NUMBER)
        wall_number     = wall.LookupParameter('Wall Number')
        wall_mark.Set("w{}".format(number))
        wall_number.Set(wall_mark.AsValueString())
        wall_number_list.append(wall_number)

    t.Commit()
# =============================================================================================
current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')

# forms.alert('Parameters updated!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)
output = pyrevit.output.get_output()
output.center()
output.resize(300, 500)

output.print_md('### Parameters Updated: {}'.format(time_stamp))

print("Wall numbers generated:")
print('=' * 23)
for index, wall_num in enumerate(wall_number_list, start=1):
    pad_index = str(index).zfill(2)
    print("WALL {}: {}".format(pad_index, wall_num.AsValueString()))
print('=' * 23)



