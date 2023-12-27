# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import xlsxwriter
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
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

all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_Rooms)\
            .WherePasses(ElementLevelFilter(level_filter))\
            .ToElements()

sheets_in_rad = []
rooms_lst = []

for sheet in all_sheets:    # type: ViewSheet
    sheet_dept  = sheet.LookupParameter('Sheet Department').AsString()
    room_dept   = sheet.LookupParameter('Room Department').AsString()
    dwg_type    = sheet.LookupParameter('Drawing Type').AsString()
    if sheet_dept == 'RADIOLOGY':
        if room_dept == 'RADIOLOGY SESSION 3 LG NM & PET CT':
            if dwg_type == 'ROOM LAYOUT SHEET':
                sheet_number    = sheet.SheetNumber
                sheet_name      = sheet.Name
                sheets_in_rad.append(sheet_name)

for room in rooms:
    room_class = room.LookupParameter('Rooms_Classification_BLP').AsString()
    room_dept_param = room.LookupParameter('Department_BLP')
    if room_dept_param:
        _room_dept = room_dept_param.AsString()
        if _room_dept == 'RADIOLOGY':
            if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                # room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                room_name = room.LookupParameter('Room_Name_BLP').AsString()
                room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                rooms_lst.append(room_name)

unique_sheet = set(sheets_in_rad)
unique_room = set(rooms_lst)

missing_rm = [item for item in sorted(unique_room) if item not in unique_sheet]

for i in missing_rm:
    print(i)