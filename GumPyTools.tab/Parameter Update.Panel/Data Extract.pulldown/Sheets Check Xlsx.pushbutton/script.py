# -*- coding: utf-8 -*-

__title__ = 'Sheet Check Xlsx'
__doc__ = """
This script will export out sheets in excel format.
Parameters included:
- Room Number
- Room Name
- Titleblock Name
- Department

HOW TO:
1. Run the command.
2. Confirm if you're committed to export out.
3. Select destination folder.
4. Select desired Department.
5. Confirmation will be shown at the end.
__________________________________
v1. 20 Dec 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import xlsxwriter
from Autodesk.Revit.DB import *
from pyrevit import forms
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

ask_user = forms.ask_for_one_item(
    ['Yes', 'No'],
    prompt='Export titleblock names?',
    title='Export titleblock info'
)

if not ask_user:
    sys.exit()

# 🔴 PREPARE EXCEL
file_path = forms.save_excel_file(title='Select destination file')
if not file_path:
    forms.alert("No path chosen. Command will exit", exitscript=True)
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
headings = ['Sheet Number',
            'Sheet Name',
            'TitleBlock Name',
            'Sheet Department',
            'Sheet Group 1',
            'Sheet Group 2'
            ]
for i, heading in enumerate(headings):
    worksheet.write(0, i, heading)
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 100)
worksheet.set_column('C:C', 20)
worksheet.set_column('D:D', 20)
worksheet.set_column('E:E', 40)
worksheet.set_column('F:F', 30)
# -----------------------------------------------------------------------------------------
#  1️⃣ COLLECT ELEMENTS NEEDED
view_sheet = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
tblock_cat_id = ElementId(BuiltInCategory.OST_TitleBlocks)

# -----------------------------------------------------------------------------------------
#  2️⃣ GET THE LIST
sheet_dept_list     = []

for el in view_sheet:
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
sel_dept_list = forms.SelectFromList.show(sorted(sheet_dept_list), multiselect=False, button_name='Select Department',
                                          title="Select Department")
if not sel_dept_list:
    forms.alert("No department selected.\nCommand will exit", exitscript=True)


# -----------------------------------------------------------------------------------------
# 3️⃣ MAKE A CONDITION
collected_info = []

for view in view_sheet:     # type: ViewSheet
    sheet_department    = view.LookupParameter('Sheet Department').AsString()
    if sheet_department == sel_dept_list:
        sheet_number    = view.SheetNumber
        sheet_name      = view.Name
        col_sheet_dept  = view.LookupParameter('Sheet Department').AsString()
        col_room_dept   = view.LookupParameter('Room Department').AsString()
        dwg_type        = view.LookupParameter('Drawing Type').AsString()
        all_tblock_id = FilteredElementCollector(doc, view.Id).OfCategoryId(tblock_cat_id).ToElementIds()      # get the tblock of filtered view sheet by id
        tblock_name     = None
        for tblock_id in all_tblock_id:
            t_block_el = doc.GetElement(tblock_id)
            tblock_name = t_block_el.Name
        collected_info.append((sheet_number, sheet_name, tblock_name, col_sheet_dept, col_room_dept, dwg_type))

# -----------------------------------------------------------------------------------------
# 🔴 WRITE EXCEL
row = 1
for sheet_number, sheet_name, tblock_name, col_sheet_dept, col_room_dept, dwg_type in sorted(collected_info):
    worksheet.write(row, 0, str(sheet_number))
    worksheet.write(row, 1, sheet_name)
    worksheet.write(row, 2, tblock_name)
    worksheet.write(row, 3, col_sheet_dept)
    worksheet.write(row, 4, col_room_dept)
    worksheet.write(row, 5, dwg_type)
    row += 1

forms.alert("Exported {} items successfully".format(len(collected_info)), warn_icon=False, exitscript=False)

