# -*- coding: utf-8 -*-

__title__ = 'Export Sheets'
__doc__ = """
Export all Sheet Number and Sheet Names.
No extra parameter rule.
===============================================
v1. 31 Jan 204
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
import xlsxwriter
from Autodesk.Revit.DB import *
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import sys
import clr
clr.AddReference("System")


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝  variables
# ======================================================================================================

doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection

# ==========================================================x============================================
file_path = forms.save_excel_file(title="Select destination folder")
if not file_path:
    sys.exit()
workbook = xlsxwriter.Workbook(file_path)
ws = workbook.add_worksheet()
headings = ['Sheet Number', 'Sheet Name', 'Element Id']

for i, heading in enumerate(headings):
    ws.write(0, i, heading)
ws.set_column('A:A', 20)
ws.set_column('B:B', 40)
ws.set_column('C:C', 20)

# --------------------------------------------------------------------------------------------------------
try:
    components = [Label('Choose option:'),
                  CheckBox('opt_1', "Export All", default=True),
                  Label('Uncheck = "DL", "GP", "PE"'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Export Sheets', components)
    form.show()

    user_input = form.values
    option  = user_input['opt_1']
except KeyError:
    sys.exit()
# --------------------------------------------------------------------------------------------------------
all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

row = 1
for i, sheet in enumerate(sorted(all_sheets, key=lambda x: x.SheetNumber), start=1):    # type: ViewSheet
    sheet_number    = sheet.SheetNumber
    sheet_name      = sheet.Name
    sheet_id        = sheet.Id
    if option:
        ws.write(i, 0, sheet_number)
        ws.write(i, 1, sheet_name)
        ws.write(i, 2, str(sheet_id))
    else:
        if sheet_number.startswith("DL") or \
                sheet_number.startswith("GP") or \
                sheet_number.startswith("PE"):
            ws.write(row, 0, sheet_number)
            ws.write(row, 1, sheet_name)
            ws.write(row, 2, str(sheet_id))
            row += 1

workbook.close()

forms.alert("Sheets Exported!", warn_icon=False, exitscript=False)







