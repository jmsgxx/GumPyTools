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

with rvt_transaction(doc, __title__):
    for sheet in all_sheets:    # type: ViewSheet
        sheet_name = sheet.Name
        sheet_number = sheet.SheetNumber
        if sheet_number.startswith('DL0'):
            part_s_num = sheet_number.split("-")
            for view in all_views:
                view_name = Element.Name.GetValue(view)
                if part_s_num[1] == view_name[-2:]:
                    # Check if the view is already on a sheet
                    view_on_sheet = any(vp for vp in all_viewports if vp.OwnerViewId == view.Id)
                    if not view_on_sheet:
                        origin_pt = XYZ(0, 0, 0)
                        try:
                            Viewport.Create(doc, sheet.Id, view.Id, origin_pt)
                        except Exception as e:
                            print("Failed to create viewport for view '{}' on sheet '{}': {}".format(view_name, sheet_name, str(e)))



# TODO: EXCLUDE THE CONTENT PAGE
