# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.UI import Selection
from Autodesk.Revit.UI.Selection import ObjectType
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes
from pyrevit import forms, script

import clr
clr.AddReference("System")


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝  variables
# ======================================================================================================

doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection

# ==========================================================x============================================
selected_elem = get_multiple_elements()

# filter_type = ISelectionFilter_Classes([FamilyInstance])
# fam_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Lines")
# selected_elem = [doc.GetElement(el) for el in fam_list]



def get_host_link(el):
    host_rvt = el.Host
    if isinstance(host_rvt, RevitLinkInstance):
        link_doc = host_rvt.GetLinkDocument()
        host_elem_id = el.HostFace.ElementId
        host_elem = link_doc.GetElement(host_elem_id)
        return host_elem
    else:
        return host_rvt


lst_host = []

for elem in selected_elem:
    host = get_host_link(elem)
    lst_host.append(host)

for i in lst_host:
    print(i)


