# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Snippets import _x_selection
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._convert import convert_internal_units
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes
from Snippets._context_manager import rvt_transaction, try_except
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
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================

filter_type = _x_selection.CurtainPanelFilter()
selected_element = selection.PickObjects(ObjectType.Element, filter_type, 'Select Panels')

if not selected_element:
    selected_element = selection.PickObjects(ObjectType.Element, filter_type, 'Select Panels')
    if not selected_element:
        forms.alert('Select curtain panels.', exitscript=True, warn_icon=True)

for el in selected_element:
    selected_panels = doc.GetElement(el)

    cp_ht = selected_panels.get_Parameter(BuiltInParameter.CURTAIN_WALL_PANELS_HEIGHT).AsDouble()
    cp_ht_mm = convert_internal_units(cp_ht, False, 'mm')

    panel_ht_param = selected_panels.LookupParameter('Panel Height')

    with rvt_transaction(doc, __title__):
        panel_ht_param.Set(cp_ht)


