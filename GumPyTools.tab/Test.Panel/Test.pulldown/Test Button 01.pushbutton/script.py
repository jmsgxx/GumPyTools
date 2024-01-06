# -*- coding: utf-8 -*-

__title__ = 'Room Docs'
__doc__ = """
***MUST RUN ON THE LEVEL YOU WANT TO CHECK***

This script will check if the selected rooms to have an RLS
has sheets.

NOTE 1: RLS Sheets to have either DEPARTMENTAL  - BLP or 
REPEATABLE - BLP as value for Rooms_Classification_BLP.

NOTE 2: Print statement may show the Rooms even though they
already have sheets for 2 reasons.

    1. Room Name is different in Sheet Name or
    2. Room Name doesn't exist in Sheet Name

HOW TO:
1. Got to the level view where you want to check the rooms.
Click the command.
2. Interface will pop up. Select parameters based on the organization
of sheets.
3. Print statement will be shown in the end.
__________________________________
v1. 31 Dec 2023

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================

from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Autodesk.Revit.DB import *
import pyrevit
from pyrevit import forms
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# ===============================================================================
# 🟠 COLLECT ALL SHEETS

user_parameter = 'Sheet Department'
all_shared_param = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()

param_element = None

for shared_param in all_shared_param:
    if shared_param.Name == user_parameter:
        param_element = shared_param
        break

f_param         = ParameterValueProvider(param_element.Id)
evaluator       = FilterStringEquals()
f_param_value   = "RADIOLOGY"

f_rule = FilterStringRule(f_param, evaluator, f_param_value)
filter_name = ElementParameterFilter(f_rule)

all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets)\
            .WherePasses(filter_name)\
            .ToElements()

# 🟠 COLLECT ALL ROOMS
level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_Rooms)\
            .WherePasses(ElementLevelFilter(level_filter))\
            .ToElements()

# 3️⃣ MAIN CODE
# =================================================================================


room_id_sht = []

for sheet in all_sheets:    # type: ViewSheet
    sht_sheet_dept = sheet.LookupParameter('Sheet Department').AsString()
    if sht_sheet_dept == 'RADIOLOGY':
        viewport_id = sheet.GetAllViewports()
        for ids in viewport_id:
            viewport = doc.GetElement(ids)      # type: Viewport
            view_id = viewport.ViewId
            view = doc.GetElement(view_id)      # type: View

            if view.ViewType == ViewType.FloorPlan:
                level_filter = ElementLevelFilter(active_level.Id)
                room_collector = FilteredElementCollector(doc, view.Id)\
                    .OfCategory(BuiltInCategory.OST_Rooms)\
                    .WherePasses(level_filter)\
                    .ToElements()

                for room in room_collector:
                    sht_room_id = room.Id
                    room_id_sht.append(sht_room_id)

rooms_lst   = []

for room in rooms:
    room_class          = room.LookupParameter('Rooms_Classification_BLP').AsString()
    room_dept_param     = room.LookupParameter('Department_BLP')
    if room_dept_param:
        room_dept = room_dept_param.AsString()
        if room_dept == 'RADIOLOGY':
            if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                # room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                room_id         = room.Id.IntegerValue
                room_name       = room.LookupParameter('Room_Name_BLP').AsString()
                room_number     = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                rooms_lst.append({room_name: room_id})


rooms_dict = {}
for room_dict in rooms_lst:
    for room_name, room_id in room_dict.items():
        rooms_dict[room_name] = room_id

missing_rm = []

for k, v in rooms_dict.items():
    if k not in room_id_sht:
        missing_rm.append("{} - {}".format(k, v))
# -------------------------------------------------------------------------------------
# print statement

output = pyrevit.output.get_output()
output.center()
output.resize(300, 500)

if len(missing_rm) == 0:
    print('All rooms are covered.')
else:
    print('=' * 50)
    print("Rooms not documented:")
    print('=' * 50)
    for index, i in enumerate(missing_rm, start=1):
        num = str(index)
        print("{}. {}".format(num.zfill(3), i))

