# -*- coding: utf-8 -*-

__title__ = 'Delete Sheets'
__doc__ = """
***ENSURE THE SHEETS ARE 100% UNUSABLE***

Ensure that the sheets are already redundant and will
not be used in the future.

WHAT THIS SCRIPT DOES:
This script will not only delete the sheets, but also
the views in the sheet on the entire model.

WHY USE THIS SCRIPT?
Since models are already segregated at each level, sheets at a
specified level, apart from the current model, 
are already irrelevant. Hence, this script performs 
deletion on the entire model.

HOW TO USE THIS SCRIPT:
1. Select the sheet/s in the project browser
and click the button.
If in doubt, contact the developer.
__________________________________
v1. 11 Jan 2024
Author: Joven Mark Gumana
"""

import sys

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets._x_selection import get_multiple_elements
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from pyrevit import forms
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
current_view    = active_view.Id
selection = uidoc.Selection     # type: Selection

ask_user = forms.ask_for_one_item(['Yes', 'No'],
                                  "Do you want to delete?",
                                  "View deletion cannot be undone. Are you sure?",
                                  title="Delete Sheets")

if not ask_user:
    forms.alert("No selection. Exiting command", exitscript=True)

if ask_user == 'No':
    sys.exit()

else:
    sheet_collection = get_multiple_elements()

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
                    deleted_sheet = doc.Delete(sheet.Id)

                forms.alert("{} sheet/s deleted.\nIf it is a mistake immediately close the file and do not save." \
                            .format(len(sheet_collection)))

