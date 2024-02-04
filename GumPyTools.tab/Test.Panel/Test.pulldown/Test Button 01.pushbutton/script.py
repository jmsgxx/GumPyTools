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


with rvt_transaction(doc, __title__):
    with try_except():
        for sheet in all_sheets:    # type: ViewSheet
            sheet_number = sheet.SheetNumber
            sheet_name = sheet.Name
            for view in all_views:
                view_name = view.Name

                # Extract the last two digits from the sheet number and view name
                sheet_num = sheet_number[-2:]
                view_num = view_name[-2:]

                if "CONTENT PAGE" in sheet_name:
                    continue
                elif "LOWER GROUND DETAIL" in sheet_name and "LG" in view_name and sheet_num == view_num:
                    # vp_ids = sheet.GetAllViewports()
                    # for id in vp_ids:
                    #     vp_el = doc.GetElement(id)
                    #     sheet.DeleteViewport(vp_el)
                    # print("{} : {}".format(sheet_name, view_name))
                    sht_outline = sheet.Outline
                    x = sht_outline.Max.U - sht_outline.Min.U
                    y = sht_outline.Max.V - sht_outline.Min.U

                    origin_pt = XYZ(x/2, y/1.8, 0)
                    Viewport.Create(doc, sheet.Id, view.Id, origin_pt)




