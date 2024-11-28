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
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from Snippets._x_selection import ISelectionFilter_Classes, ParkingFilter, RailingFilter
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

all_fam_instance = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()

for fam in all_fam_instance:
    fam_name = fam.Name
    if fam_name == "001_BREAKLINE":
        hor_val = fam.LookupParameter("HOR_VALUE")
        ver_val = fam.LookupParameter("VER_VALUE")
        el_view_id = fam.OwnerViewId
        el_view = doc.GetElement(el_view_id)
        el_view_scale = el_view.Scale

        scale_factor = el_view_scale / 100.0

        new_hor_value = scale_factor * 400
        new_ver_value = scale_factor * 200
        hor_conv_val = convert_internal_units(new_hor_value, True, 'mm')
        ver_conv_val = convert_internal_units(new_ver_value, True, 'mm')

        with rvt_transaction(doc, __title__):
            hor_val.Set(hor_conv_val)
            ver_val.Set(ver_conv_val)

