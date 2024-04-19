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
from Snippets._convert import convert_internal_units
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._x_selection import ISelectionFilter_Classes, get_multiple_elements
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
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================

all_casework = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Casework).WhereElementIsNotElementType().\
    ToElements()

ips_basin = []

for case in all_casework:
    if case.Location:
        case_id = case.GetTypeId()
        case_el = doc.GetElement(case_id)

        case_type_name = case_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()

        if case_type_name == "IPS_Basin":
            ips_basin.append(case_el)

print(len(ips_basin))




