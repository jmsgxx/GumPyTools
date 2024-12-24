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
# ╔═╗╔═╗╦ ╦╔═╗╔╦╗╦ ╦╦  ╔═╗  ╔═╗╦╔═╗╦  ╔╦╗
# ╚═╗║  ╠═╣║╣  ║║║ ║║  ║╣   ╠╣ ║║╣ ║   ║║
# ╚═╝╚═╝╩ ╩╚═╝═╩╝╚═╝╩═╝╚═╝  ╚  ╩╚═╝╩═╝═╩╝
# --------------------------------------------------------------

# Define the key schedule parameter name
p_key_name = 'Room Type'
key_schedule = None
key_schedule_id = None

# Collect all schedules in the document
all_schedules = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).WhereElementIsNotElementType().ToElements()

# Find the key schedule based on the parameter name
for schedule in all_schedules:  # type: ViewSchedule
    try:
        if schedule.KeyScheduleParameterName == p_key_name:
            key_schedule = schedule
            key_schedule_id = schedule.Id
            break
    except:
        pass

if not key_schedule:
    print("Check the code. Can't find the key schedule you're looking for.")

# Collect key values from the key schedule
key_values = FilteredElementCollector(doc, key_schedule.Id).WhereElementIsNotElementType()

err_lst = []

with rvt_transaction(doc, __title__):
    for v in key_values:
        rm_soa = v.LookupParameter('Room SoA Ref Number')
        if rm_soa.HasValue:
            try:
                set_elem = rm_soa.Set("-")
            except:
                err_lst.append(v)

if len(err_lst) == 0:
    forms.alert("Success!", warn_icon=False)
else:
    forms.alert("Check the code.")

view_def = key_schedule.Definition
count = view_def.GetFieldCount()

f_params = []

for i in range(count):
    field = view_def.GetField(i)  # schedule field
    ele = doc.GetElement(field.ParameterId)
    f_params.append(ele)
#
#
# rm_soa = f_params[1]
#
#
# param_set = rm_soa.Parameters
#
# for param in param_set:
#     param_def = param.Definition
#     param_name = param_def.Name
#     param_value = param.AsString() if param.StorageType == StorageType.String \
#         else param.AsValueString() if param.StorageType == StorageType.Double \
#         else str(param.AsInteger()) if param.StorageType == StorageType.Integer \
#         else str(param.AsElementId().IntegerValue) if param.StorageType == StorageType.ElementId else 'N/A'
#     print("Parameter Name: {}, Parameter Value: {}".format(param_name, param_value))


