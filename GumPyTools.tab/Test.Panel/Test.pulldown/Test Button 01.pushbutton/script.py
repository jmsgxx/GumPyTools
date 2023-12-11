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
from Autodesk.Revit.DB import *
import xlsxwriter
from pyrevit import forms
from datetime import datetime
import os
import sys
import clr
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
current_view    = [active_view.Id]

file_path = forms.save_excel_file(title='Select destination file')
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
headings = ['Room Name', 'Room Number']
for i, heading in enumerate(headings):
    worksheet.write(0, i, heading)
worksheet.set_column('A:A', 85)
worksheet.set_column('B:B', 15)

level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Rooms)\
    .WherePasses(ElementLevelFilter(level_filter))\
    .ToElements()


room_in_pharma = []

for room in rooms:
    room_dept = room.get_Parameter(BuiltInParameter.ROOM_DEPARTMENT).AsString()
    if room_dept == 'PHARMACY':
        room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
        room_number = room.Number
        room_in_pharma.append((room_name, room_number))

row = 1
for room_name, room_number in sorted(room_in_pharma, key=lambda x: x[0]):
    worksheet.write(row, 0, room_name)
    worksheet.write(row, 1, room_number)
    row += 1
