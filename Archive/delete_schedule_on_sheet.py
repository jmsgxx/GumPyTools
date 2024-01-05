# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================

from Snippets._x_selection import get_multiple_element
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

all_schedules = FilteredElementCollector(doc).OfClass(ScheduleSheetInstance).ToElements()

sheet_collection = get_multiple_element()

schedule_to_delete = []

with Transaction(doc, __title__) as t:
    t.Start()
    try:
        for sheet in sheet_collection:  # type: ViewSheet
            sheet_id = sheet.Id
            for schedule in all_schedules:   # type: ScheduleSheetInstance
                if schedule.OwnerViewId == sheet_id:
                    sch_id = schedule.ScheduleId
                    if schedule.Pinned:
                        schedule.Pinned = False
                    schedule_to_delete.append(sch_id)

    except Exception:
        pass

    for item in schedule_to_delete:
        try:
            # print(item)
            doc.Delete(item)
        except Exception:
            pass



    t.Commit()


