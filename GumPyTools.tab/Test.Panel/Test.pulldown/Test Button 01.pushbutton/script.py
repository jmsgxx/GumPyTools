# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button, TextBox)
from Snippets._context_manager import rvt_transaction
from Autodesk.Revit.DB import *
from Snippets._x_selection import get_multiple_elements
from pyrevit import forms

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


def count_items(item_list, keyword, level):
    collected_lst = []
    for item in item_list:
        sheet_number = item.SheetNumber
        sheet_name = item.Name
        if 'CONTENT PAGE' not in sheet_name and sheet_number.startswith(str(keyword)):
            collected_lst.append(item)

    return "All sheets in {}: is {}.".format(str(level), len(collected_lst))


all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType()\
    .ToElements()

b2 = count_items(all_sheets, 'DL0001', 'B2')
b1 = count_items(all_sheets, 'DL0002', 'B1')
lg = count_items(all_sheets, 'DL0003', 'LG')

print(b2)
print(b1)
print(lg)

for count in range(15):
    items = count_items(all_sheets, "DL10{}".format(str(count).zfill(2)), "L{}".format(count))
    print(items)


