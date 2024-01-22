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
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._x_selection import DoorCustomFilter, get_multiple_elements
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
# door_selection = get_multiple_elements()
#
# if not door_selection:
#     with try_except():
#         filter_type = DoorCustomFilter()
#         door_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Doors")
#         door_selection = [doc.GetElement(dr) for dr in door_list]
#
#         if not door_selection:
#             forms.alert("No doors selected. Exiting command.", exitscript=True, warn_icon=False)

door_selection = FilteredElementCollector(doc, active_view.Id) \
    .OfCategory(BuiltInCategory.OST_Doors) \
    .WhereElementIsNotElementType() \
    .ToElements()

# =================================================================================================================
door_count = 0

for door in door_selection:  # type: FamilyInstance
    door_type_id = door.GetTypeId()
    door_type = doc.GetElement(door_type_id)

    dr_pull_wl_ht   = door_type.LookupParameter('Door Protection Pull or Wall Height Code')
    dr_pull_wl      = door_type.LookupParameter('Door Protection Pull or Wall Code')
    dr_push_tr_ht   = door_type.LookupParameter('Door Protection Push or Track Height Code')
    dr_push_tr      = door_type.LookupParameter('Door Protection Push or Track Code')

    dr_prot_pl_wl_yes = door_type.LookupParameter('Door Protection Pull or Wall Yes')
    dr_prot_ph_tk_yes = door_type.LookupParameter('Door Protection Push or Track Yes')

    door_type_name = door_type.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()

    with rvt_transaction(doc, __title__):
        # if dr_push_tr.AsString() and dr_push_tr_ht.AsString() \
        #         and dr_pull_wl.AsString() and dr_pull_wl_ht.AsString():
        #     dr_prot_pl_wl_yes.Set(1)
        #     dr_prot_ph_tk_yes.Set(1)

        if not dr_push_tr.AsString() and not dr_push_tr_ht.AsString() \
                and not dr_pull_wl.AsString() and not dr_pull_wl_ht.AsString():
            dr_push_tr.Set('--')

        # elif dr_push_tr.AsString() and dr_push_tr_ht.AsString() \
        #         and not dr_pull_wl.AsString() and not dr_pull_wl_ht.AsString():
        #     dr_prot_pl_wl_yes.Set(1)
        #     dr_prot_ph_tk_yes.Set(0)


