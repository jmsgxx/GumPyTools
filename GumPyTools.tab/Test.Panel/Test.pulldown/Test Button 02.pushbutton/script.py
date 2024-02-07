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
    all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()


    for index, sheet in enumerate(all_sheets, start=1):    # type: ViewSheet
        sheet_name = sheet.get_Parameter(BuiltInParameter.SHEET_NAME).AsString()
        sheet_number = sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
        for view in all_views:  # type: View
            view_name = Element.Name.GetValue(view)
            if view_name.startswith("SS_DOC_L16"):
                v_num = view_name.split("_")[2][-2:]
                s_num = sheet_number[-2:]

                if "SUNKEN SLAB" in sheet_name and v_num == s_num:
                    # print(v_num, s_num)
                    sht_outline = sheet.Outline
                    x = sht_outline.Max.U - sht_outline.Min.U
                    y = sht_outline.Max.V - sht_outline.Min.V

                    origin_pt = XYZ(x / 2.2, y / 2, 0)
                    Viewport.Create(doc, sheet.Id, view.Id, origin_pt)





    # selected_sheets = get_multiple_elements()
    # selected_sheets.sort(key=lambda s: s.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString())
    #
    # for index, sheet in enumerate(selected_sheets, start=1):
    #     sheet_name = sheet.get_Parameter(BuiltInParameter.SHEET_NAME)
    #     sheet_name.Set("BASEMENT 2 DETAIL LAYOUT PLAN (SHEET {} OF {})".format(index, len(selected_sheets)))

