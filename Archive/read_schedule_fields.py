# -*- coding: utf-8 -*-

__title__ = "Test Button 03"
__doc__ = """

__________________________________
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import math
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Snippets._x_selection import (ISelectionFilter_Classes, ParkingFilter, RailingFilter, get_multiple_elements,
                                   SupressWarnings)
from pyrevit import forms
from Snippets._context_manager import rvt_transaction, try_except
from Snippets._convert import convert_internal_units
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝ function



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection

# --------------------------------------------------------------
all_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

p_key_name = 'Room Type'
key_schedule = None
key_schedule_id = None

all_schedules = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).ToElements()

for schedule in all_schedules:  # type: ViewSchedule
    try:
        if schedule.KeyScheduleParameterName == p_key_name:
            key_schedule = schedule
            key_schedule_id = schedule.Id
            break
    except:
        pass

# READING FIELDS ON SCHEDULE

if key_schedule is not None:

    # Iterate through the fields to find the index of the desired column
    column_index = None

    view_def = key_schedule.Definition
    count = view_def.GetFieldCount()
    p_names = []


    for i in range(0, count):
        field = view_def.GetField(i)        # schedule field
        ele = doc.GetElement(field.ParameterId)
        try:
            if ele.Name == 'Room SoA Ref Number':
                column_index = i
                break
        except:
            pass

    if column_index:
        # Get the table data
        table_data = key_schedule.GetTableData()
        table_section = table_data.GetSectionData(SectionType.Body)

        # Loop through each row (skipping the header row) and get the parameter values
        with rvt_transaction(doc, __title__):
            for row in range(2, table_section.NumberOfRows):  # Start from 1 to skip the header row
                cell = table_section.GetCellText(row, column_index)



if not key_schedule:
    print("Check the code. Can't find the key schedule you're looking for.")

key_values = FilteredElementCollector(doc, key_schedule.Id).ToElements()

view_def = key_schedule.Definition
count = view_def.GetFieldCount()

f_params = []
p_ids = []
p_names = []

for i in range(0, count, 1):
    field = view_def.GetField(i)        # schedule field
    ele = doc.GetElement(field.ParameterId)
    f_params.append(ele)
    try:
        p_names.append(ele.Name)
    except:
        p_names.append(None)

# for i in p_names:
#     print(i)

# for i in f_params:
#     print(i)

for i in key_values:
    print(i.Name)