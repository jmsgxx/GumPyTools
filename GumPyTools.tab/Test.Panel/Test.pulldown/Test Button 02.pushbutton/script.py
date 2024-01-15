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

door_selection = FilteredElementCollector(doc, active_view.Id)\
    .OfCategory(BuiltInCategory.OST_Doors)\
    .WhereElementIsNotElementType()\
    .ToElements()

# =================================================================================================================

pull_wall   = ['PL', 'WL', 'PLS', 'WLS']
push_track  = ['PH', 'TK', 'PHS', 'TKS']


for door in door_selection:  # type: FamilyInstance
    if door.Location:
        door_type_id = door.GetTypeId()
        door_type = doc.GetElement(door_type_id)

        dr_pull_wl_ht       = door_type.LookupParameter('Door Protection Pull or Wall Height Code')
        dr_pull_wl          = door_type.LookupParameter('Door Protection Pull or Wall Code')
        dr_push_tr_ht       = door_type.LookupParameter('Door Protection Push or Track Height Code')
        dr_push_tr          = door_type.LookupParameter('Door Protection Push or Track Code')

        door_type_name      = door_type.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()

        dr_prot_pl_wl_yes      = door_type.LookupParameter('Door Protection Pull or Wall Yes')
        dr_prot_ph_tk_yes      = door_type.LookupParameter('Door Protection Push or Track Yes')


        with rvt_transaction(doc, __title__):
            if dr_pull_wl.AsString() not in pull_wall:
                dr_pull_wl.Set("")
            if dr_push_tr.AsString() not in push_track:
                dr_push_tr.Set("")
            if not dr_pull_wl_ht and not dr_pull_wl and not dr_push_tr_ht and not dr_push_tr:
                dr_prot_pl_wl_yes.Set(1)

            #     dr_prot_ph_tk_yes.Set(0)
            # dr_prot_pl_wl_yes.Set(0)
            # dr_prot_ph_tk_yes.Set(0)

