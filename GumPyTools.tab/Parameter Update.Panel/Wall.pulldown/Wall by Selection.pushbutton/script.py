# -*- coding: utf-8 -*-

__title__ = 'Wall by Selection'
__doc__ = """
This script will renumber the selected
walls.
__________________________________
HOW TO:
1. Run the command.
2. Select the walls. If it happened
that you selected a wall that shouldn't
be included, as long as the wall has "FIN"
to it's name it will number itself.
==================================
v1: 22 Nov 2023
Author: Joven Mark Gumana
"""

import sys

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Snippets import _x_selection
from pyrevit import forms, revit
import time
import clr
from datetime import datetime
import pyrevit
from Autodesk.Revit.UI.Selection import ObjectType, Selection
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
selection = uidoc.Selection     # type: Selection
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
    mark_wall           = []
    type_mark_wall      = []
    desc_wall           = []
    wall_number_list    = []

    wall_pick = [doc.GetElement(el_id) for el_id in selection.GetElementIds()]
    if not wall_pick:
        try:
            filter_type = _x_selection.WallSelectionFilterSTR([Wall], "FIN")
            wall_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Walls")
            wall_pick = [doc.GetElement(el) for el in wall_list]
            if not wall_pick:
                forms.alert("Select walls.\nTry again.", exitscript=True)
        except Exception as e:
            forms.alert(str(e), exitscript=True)

    for number, wall in enumerate(wall_pick, start=1):
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



