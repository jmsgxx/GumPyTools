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
try:
    all_sheets = FilteredElementCollector(doc).\
                OfClass(ViewSheet).\
                ToElements()

    # 🟠 COLLECT ALL ROOMS
    level_filter = active_level.Id

    rooms = FilteredElementCollector(doc)\
                .OfCategory(BuiltInCategory.OST_Rooms)\
                .WherePasses(ElementLevelFilter(level_filter))\
                .ToElements()

except AttributeError:
    forms.alert("Select desired level to execute the command.\nTry again.", exitscript=True)
# =================================================================================
# 1️⃣ GET RELEVANT PARAMETERS

# initiate an empty dictionary
sheet_dict = {}
sheet_rm_dept = {}
sheet_dwg_type = {}

# sheets
for sheet in all_sheets:    # type: ViewSheet
    sht_sheet_dept                  = sheet.LookupParameter('Sheet Department').AsString()
    room_dept                   = sheet.LookupParameter('Room Department').AsString()
    dwg_type                    = sheet.LookupParameter('Drawing Type').AsString()
    if sht_sheet_dept:
        sheet_dict[sht_sheet_dept]      = sht_sheet_dept
    if room_dept:
        sheet_rm_dept[room_dept]    = room_dept
    if dwg_type:
        sheet_dwg_type[dwg_type]    = dwg_type

room_class_dict = {}

# rooms
for room in rooms:
    room_class = room.LookupParameter('Department_BLP').AsString()
    if room_class:
        room_class_dict[room_class] = room_class


# 2️⃣ UI
# =================================================================================
try:     # catch the error
    components = [Label('Sheet Department:'),
                  ComboBox('sheet_dept', sheet_dict),
                  Label('Sheet Room Department:'),
                  ComboBox('room_dept', sheet_rm_dept),
                  Label('Sheet Drawing Department:'),
                  ComboBox('dwg_type', sheet_dwg_type),
                  Separator(),
                  Label('Room Department:'),
                  ComboBox('rm_class', room_class_dict),
                  Separator(),
                  Button('Select')]

    form = FlexForm('Check Rooms if on Sheet', components)

    form.show()
    user_inputs = form.values
    # sheets
    sht_depart      = user_inputs['sheet_dept']
    rm_dept         = user_inputs['room_dept']
    dwg_t_dept      = user_inputs['dwg_type']
    # rooms
    room_rm_class      = user_inputs['rm_class']

# 3️⃣ MAIN CODE
# =================================================================================

    sheets_in_rad = []
    rooms_lst = []

    for sheet in all_sheets:    # type: ViewSheet
        sht_sheet_dept          = sheet.LookupParameter('Sheet Department').AsString()
        room_dept               = sheet.LookupParameter('Room Department').AsString()
        dwg_type                = sheet.LookupParameter('Drawing Type').AsString()
        if sht_sheet_dept   == sht_depart:
            if room_dept    == rm_dept:
                if dwg_type == dwg_t_dept:
                    sheet_number    = sheet.SheetNumber
                    sheet_name      = sheet.Name
                    sheets_in_rad.append(sheet_name)

    for room in rooms:
        room_class          = room.LookupParameter('Rooms_Classification_BLP').AsString()
        room_dept_param     = room.LookupParameter('Department_BLP')
        if room_dept_param:
            _room_dept = room_dept_param.AsString()
            if _room_dept == room_rm_class:
                if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                    # room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                    room_name       = room.LookupParameter('Room_Name_BLP').AsString()
                    room_number     = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                    rooms_lst.append(room_name)

    unique_sheet = set(sheets_in_rad)
    unique_room = set(rooms_lst)

    missing_rm = [item for item in sorted(unique_room) if item not in unique_sheet]

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

except KeyError:
    forms.alert("No parameter selected.\nExiting Command.", exitscript=True, warn_icon=True)
