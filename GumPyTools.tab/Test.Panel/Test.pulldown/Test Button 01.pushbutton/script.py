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
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
from Snippets._x_selection import get_multiple_elements
from pyrevit import forms, script

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

all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
all_views = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
all_viewports = FilteredElementCollector(doc).OfClass(Viewport).ToElements()

# with rvt_transaction(doc, __title__):
#     for sheet in all_sheets:    # type: ViewSheet
#         sheet_name = sheet.Name
#         sheet_number = sheet.SheetNumber
#         if sheet_number.startswith('DL0') and 'CONTENT PAGE' not in sheet_name:
#             part_s_num = sheet_number.split("-")
#             for view in all_views:
#                 view_name = view.Name
#                 if "DOC_FP_FFL_B2_50" in view_name or \
#                         "DOC_FP_FFL_B1_50" in view_name or \
#                         "DOC_FP_FFL_LG_50" in view_name:
#                     view_num = view_name.split("_")[-1]
#                     if part_s_num[1] == view_num:
#                         print(sheet_number + "-" + sheet_name + ":" + view_name)
#                         origin_pt = XYZ(0, 0, 0)
#                         with try_except():
#                             Viewport.Create(doc, sheet.Id, view.Id, origin_pt)

with rvt_transaction(doc, __title__):
    with try_except():
        x_offset = 0  # Initialize x offset for view placement
        for sheet in all_sheets:    # type: ViewSheet
            sheet_number = sheet.SheetNumber
            sheet_name = sheet.Name
            for view in all_views:
                view_name = view.Name

                # Extract the last two digits from the sheet number and view name
                sheet_num = sheet_number[-2:]
                view_num = view_name[-2:]

                if "BASEMENT 2" in sheet_name and "B2" in view_name and sheet_num == view_num:
                    print("{} : {}".format(sheet_number, view_name))
                    print("{} : {}".format(type(sheet.Id), type(view.Id)))
                    origin_pt = XYZ(x_offset, 0, 0)  # Use x offset for view placement
                    Viewport.Create(doc, sheet.Id, view.Id, origin_pt)



