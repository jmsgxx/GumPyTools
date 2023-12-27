# -*- coding: utf-8 -*-

__title__ = 'Room->Sheet->Xlsx'
__doc__ = """
This script will export out the data to what sheets
does the Room belong.

Parameters to export out:
 - Element Id
 - Room Name
 - Room Number
 - Sheet Number
 - Sheet Name
 - Department
 - Associated Level
 
 HOW TO:
 
 1. Click and commit to run.
 2. Select the destination folder of output file.
 3. Select the level of the rooms you're looking for.
 4. Select desired department.
 5. Confirmation of exportation with number of items will be
 confirmed at the end of the script.
__________________________________
v2. 22 Dec 2023
v1. 21 Dec 2023
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
# ======================================================================================================
ask_user = forms.ask_for_one_item(
    ['Yes', 'No'],
    prompt='Export rooms on sheets?',
    title='Export Rooms')
if not ask_user:
    sys.exit()
# ---------------------------------------------------------------------------------------------------
# ⭕ PREPARE EXCEL FILE
file_path = forms.save_excel_file(title='Select destination file')
if not file_path:
    forms.alert("No path chosen. Command will exit", exitscript=True)
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
headings = ['Element Id',
            'Room Name',
            'Room Number',
            'Sheet Number',
            'Sheet Name',
            'Sheet Department',
            'Sheet Group',
            'Associated Level'
            ]
for i, heading in enumerate(headings):
    worksheet.write(0, i, heading)
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 20)
worksheet.set_column('D:D', 20)
worksheet.set_column('E:E', 100)
worksheet.set_column('F:F', 30)
worksheet.set_column('G:G', 30)
worksheet.set_column('H:H', 20)

# ---------------------------------------------------------------------------------------------------
# 1️⃣ COLLECT ELEMENTS
sheet_collection = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()

# 🟦 LEVEL SELECTION
# GET ALL LEVEL
level_collector = FilteredElementCollector(doc).OfClass(Level).ToElements()
all_levels_id = [level.Id for level in level_collector]

all_levels = [doc.GetElement(el_id) for el_id in all_levels_id]
sel_level = forms.SelectFromList.show(sorted(all_levels), multiselect=False, name_attr='Name',
                                      button_name='Select Level',
                                      title='Select Level')
if not sel_level:
    sys.exit()
# ----------------------------------------------------------------------------------------------------
sheet_dept_list     = []

for el in sheet_collection:
    # sheet department
    view_sheet_dept = el.LookupParameter('Sheet Department')
    if view_sheet_dept:
        view_dept = view_sheet_dept.AsString()
        if view_dept:
            sheet_dept_list.append(view_dept)

# -----------------------------------------------------------------------------------------
"""
create a unique list to choose from
"""
sheet_dept_list = list(set(sheet_dept_list))
sel_dept = forms.SelectFromList.show(sorted(sheet_dept_list), multiselect=False, button_name='Select Department',
                                     title="Select Department")
if not sel_dept:
    forms.alert("No department selected.\nCommand will exit", exitscript=True)
# -----------------------------------------------------------------------------------------
# 2️⃣ START BREAKING DOWN
# 🟢 FILTER DOWN
"""
ViewSheet >> ViewPort >> View >> ViewType >> Room
"""
collected_info = []     # info to be exported to excel
sheet_id_list = []      # not in use
# VIEW SHEET
for sheet in sheet_collection:  # type: ViewSheet
    sheet_dept      = sheet.LookupParameter('Sheet Department').AsString()
    sheet_dwg_type  = sheet.LookupParameter('Drawing Type').AsString()
    sheet_number    = sheet.SheetNumber
    sheet_name      = sheet.Name
    sheet_id_list.append(sheet.Id)  # not in use
    if sheet_dept == sel_dept:
        # VIEW PORT
        viewport_id = sheet.GetAllViewports()   # returns an id
        for ids in viewport_id:
            viewport = doc.GetElement(ids)  # type: Viewport
            viewport_sht_id = viewport.SheetId  # not in use
            # VIEW
            view_id = viewport.ViewId
            view = doc.GetElement(view_id)      # type: View
            # VIEW TYPE
            if view.ViewType == ViewType.FloorPlan:
                # GET THE ROOM
                level_filter    = ElementLevelFilter(sel_level.Id)
                # collect only the views that you need by getting view.Id
                room_collector = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_Rooms).\
                    WherePasses(level_filter).\
                    ToElements()

                for room in room_collector:  # type: Room
                    if room.Location:   # to make sure if all is placed room
                        room_id             = room.Id
                        room_class          = room.LookupParameter('Rooms_Classification_BLP').AsString()
                        room_name_blp       = room.LookupParameter('Room_Name_BLP').AsString()
                        room_number         = room.Number
                        assoc_level         = room.get_Parameter(BuiltInParameter.LEVEL_NAME).AsString()
                        if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                            if room_number:
                                collected_info.append((
                                    room_id,
                                    room_name_blp,
                                    room_number,
                                    sheet_number,
                                    sheet_name,
                                    sheet_dept,
                                    sheet_dwg_type,
                                    assoc_level
                                ))

# -----------------------------------------------------------------------------------------
# ⭕ EXPORT TO EXCEL
row = 1
for (room_id,
     room_name_blp,
     room_number,
     sheet_number,
     sheet_name,
     sheet_dept,
     sheet_dwg_type,
     assoc_level
     ) in sorted(collected_info, key=lambda x: x[3]):

    worksheet.write(row, 0, str(room_id))
    worksheet.write(row, 1, room_name_blp)
    worksheet.write(row, 2, room_number)
    worksheet.write(row, 3, str(sheet_number))
    worksheet.write(row, 4, sheet_name)
    worksheet.write(row, 5, sheet_dept)
    worksheet.write(row, 6, sheet_dwg_type)
    worksheet.write(row, 7, assoc_level)
    row += 1

forms.alert("Exported {} items successfully".format(len(collected_info)), warn_icon=False, exitscript=False)
