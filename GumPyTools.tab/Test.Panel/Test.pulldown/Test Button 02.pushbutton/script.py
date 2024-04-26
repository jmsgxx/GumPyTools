# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets._x_selection import get_multiple_elements
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
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
with rvt_transaction(doc, __title__):
    all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()
    all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

    view_plans = []

    for view in all_views:  # type: View
        if view.ViewType == ViewType.CeilingPlan:
            view_name = view.Name
            parts = view_name.split("_")
            # if view_name.startswith("DOC_FP_FFL_01M_50"):
            if view_name == "RCP_L1M_200":
                view_plans.append(view)

    collected_sheets = []

    for sheet in all_sheets:    # type: ViewSheet
        sheet_name = sheet.Name
        sheet_number = sheet.SheetNumber
        # if sheet_number == 'DL1001M-00':
        #     continue
        # elif sheet_number.startswith("DL1001M"):
        if sheet_number == "CF101M":
            collected_sheets.append(sheet)

    # view_plans.pop(0)

    for s, v in zip(collected_sheets, view_plans):
        s_number = s.SheetNumber
        s_name = s.Name
        v_name = v.Name
        # print("{} - {}".format(s_number, v_name))

        # if s_number.split("-")[1] == v_name.split("_")[5]:
        try:
            if s_number == "CF101M" and v_name == "RCP_L1M_200":
                sht_outline = s.Outline
                x = sht_outline.Max.U - sht_outline.Min.U
                y = sht_outline.Max.V - sht_outline.Min.V

                origin_pt = XYZ(x/2.2, y/2, 0)
                Viewport.Create(doc, s.Id, v.Id, origin_pt)
        except Exception as e:
            forms.alert(str(e))
