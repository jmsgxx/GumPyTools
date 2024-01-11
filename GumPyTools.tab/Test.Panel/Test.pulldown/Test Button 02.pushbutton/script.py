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
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
import pyrevit
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

all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()

sheet_collection = get_multiple_elements()

views_to_delete = []

with rvt_transaction(doc, __title__):
    for sheet in sheet_collection:  # type: ViewSheet
        if isinstance(sheet, ViewSheet):
            viewports  = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
            for vp in viewports:    # type: Viewport
                if vp.SheetId == sheet.Id:
                    vp_id = vp.ViewId
                    view = doc.GetElement(vp_id)
                    doc.Delete(view.Id)

            schedule_graph = FilteredElementCollector(doc).OfClass(ScheduleSheetInstance).ToElements()
            for schedule in schedule_graph:
                if schedule.OwnerViewId == sheet.Id:
                    schedule_view = doc.GetElement(schedule.Id)
                    doc.Delete(schedule_view.Id)

        with try_except():
            doc.Delete(sheet.Id)
