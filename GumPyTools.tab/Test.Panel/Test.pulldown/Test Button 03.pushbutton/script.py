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
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from Snippets._x_selection import ISelectionFilter_Classes, ParkingFilter
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



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
🟡 select spline
# with try_except(False):
#     filter_type = ParkingFilter()
#     parking = selection.PickObjects(ObjectType.Element, filter_type, "Select Parking")
#     selected_parking = [doc.GetElement(el).Id for el in parking]
#
#     selection.SetElementIds(List[ElementId](selected_parking))


filter_type = ISelectionFilter_Classes([Viewport])
vport = selection.PickObjects(ObjectType.Element, filter_type, "Select ViewPort")
selected_vport = [doc.GetElement(el).Id for el in vport]

selection.SetElementIds(List[ElementId](selected_vport))

