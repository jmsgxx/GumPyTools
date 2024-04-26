# -*- coding: utf-8 -*-

__title__ = 'Create Sheets'
__doc__ = """
Create sheet by:
1. Select excel file to get the file names.
2. Select title block.
3. Confirmation will be shown if creation
 was done successfully.
__________________________________
v1. 31 Jan 2024
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import clr
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection
# ======================================================================================================
xcl_file = forms.pick_excel_file(title="Select Excel File")
if not xcl_file:
    sys.exit()

wb = xlrd.open_workbook(filename=xcl_file)

sheet_data = {}
sheet = wb.sheet_by_index(0)

all_t_blocks = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_TitleBlocks)\
    .WhereElementIsElementType()\
    .ToElements()

t_block = forms.SelectFromList.show(all_t_blocks,
                                    multiselect=False,
                                    name_attr='FamilyName',
                                    button_name='Select Titleblock')
if not t_block:
    forms.alert("No titleblock selected. Exiting Command", warn_icon=True, exitscript=True)

with rvt_transaction(doc, __title__):
    for row in range(1, sheet.nrows):
        s_number             = sheet.cell_value(row, 0)  # 0 is the column
        s_name               = sheet.cell_value(row, 1)
        new_sheet = ViewSheet.Create(doc, t_block.Id)
        new_sheet.SheetNumber = s_number
        new_sheet.Name = s_name
        # dict no use for now
        sheet_data[s_number] = s_name


# for k, v in sorted(sheet_data.items()):
#     print("{}:{}".format(k, v))

forms.alert("New sheets created!", exitscript=False, warn_icon=False)






