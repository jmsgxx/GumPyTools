# -*- coding: utf-8 -*-

__title__ = 'AR Wall info Export'
__doc__ = """
This script will export information
of walls on current Level such as:
- Element ID
- Wall Type
- Room Number
- Start X, Y, Z
- End X, Y, Z
- Instance Mark
__________________________________
HOW TO:
- Open desired View level before running
the script
- Just run the script and select
destination file. It will export out in a few
seconds
==================================
v1: 13 Nov 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import script, forms, revit
from System.Collections.Generic import List
from datetime import datetime
import xlsxwriter

import clr
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


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ======================================================================================================


def get_rooms(wall_x):
    """
    This will return the room location
    of walls.
    """
    wall_bb = wall_x.get_BoundingBox(None)
    outline = Outline(wall_bb.Min, wall_bb.Max)
    bb_filter = BoundingBoxIntersectsFilter(outline)
    rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).\
        WherePasses(bb_filter).ToElements()
    return rooms


# ======================================================================================================
output = script.get_output()
output.center()

# ⭕ PREPARE EXCEL EXPORT
file_path = forms.save_excel_file(title='Select destination file')
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
headings = ['Element ID', 'Wall Type', 'Room', 'Start X', 'Start Y', 'Start z', 'End X', 'End Y', 'End Z', 'Mark']
for i, heading in enumerate(headings):
    worksheet.write(0, i, heading)
worksheet.set_column(0, len(headings), 15)

# phase
all_phase = list(doc.Phases)
phase = (all_phase[1])

# collect walls
current_level = active_level.Id
level_filter = ElementLevelFilter(current_level)

all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WherePasses(level_filter).WhereElementIsNotElementType().ToElements()

row = 1
for wall in all_walls:
    room_number = None
    if wall.Location:
        room = get_rooms(wall)  # type:List[Reference]
        for r in room:
            room_id = ElementId(r.Id.IntegerValue)
            room_el = doc.GetElement(room_id)
            room_number = room_el.Number

        wall_type_id = wall.GetTypeId()
        type_wall = doc.GetElement(wall_type_id)
        type_wall_name = type_wall.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsValueString()
        wall_id = wall.Id   # wall instance ID
        wall_mark = wall.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsValueString()    # wall instance mark
        # 🔴 GET POINTS
        wall_start = wall.Location.Curve.GetEndPoint(0)
        wall_end = wall.Location.Curve.GetEndPoint(1)
        wall_start_x    = wall_start.X
        wall_start_y    = wall_start.Y
        wall_start_z    = wall_start.Z
        wall_end_x      = wall_start.X
        wall_end_y      = wall_start.Y
        wall_end_z      = wall_start.Z

        # 🆗 WRITE TO EXCEL
        worksheet.write('A' + str(row + 1), int((str(wall_id))))
        worksheet.write('B' + str(row + 1), type_wall_name)
        worksheet.write('C' + str(row + 1), room_number)
        worksheet.write('D' + str(row + 1), wall_start_x)
        worksheet.write('E' + str(row + 1), wall_start_y)
        worksheet.write('F' + str(row + 1), wall_start_x)
        worksheet.write('G' + str(row + 1), wall_end_x)
        worksheet.write('H' + str(row + 1), wall_end_y)
        worksheet.write('I' + str(row + 1), wall_end_z)
        worksheet.write('J' + str(row + 1), wall_mark)

        row += 1  # increment row at the end of the loop

workbook.close()

current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')
forms.alert('Excel exported!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)