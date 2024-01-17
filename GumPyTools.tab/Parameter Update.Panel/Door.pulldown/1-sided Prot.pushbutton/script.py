# -*- coding: utf-8 -*-

__title__ = '1-sided Protection'
__doc__ = """
This script will populate the parameters for
door protection.

SWING DOOR = PH2
SLIDING DOor = TK2

HOW TO:
1. You can select the element/s first or:
2. Click the command.
3. Select the desired doors. Parameters will be 
updated automatically.
4. Print statement will confirm the changes.
-----------------------------------------------
v1. 15 Jan 2024
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.UI.Selection import ISelectionFilter, Selection, ObjectType
from Snippets._x_selection import DoorCustomFilter, get_multiple_elements
from Snippets._context_manager import try_except, rvt_transaction
from Autodesk.Revit.DB import *
from pyrevit import forms
import math

import clr
clr.AddReference("System")
from System.Collections.Generic import List
from Snippets._context_manager import rvt_transaction, try_except

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application
selection = uidoc.Selection  # type: Selection

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =================================================================================================================
door_selection = get_multiple_elements()

if not door_selection:
    with try_except():
        filter_type = DoorCustomFilter()
        door_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Doors")
        door_selection = [doc.GetElement(dr) for dr in door_list]

        if not door_selection:
            forms.alert("No doors selected. Exiting command.", exitscript=True, warn_icon=False)

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
        if 'SWG' in door_type_name:
            dr_pull_wl_ht.Set(str(""))
            dr_pull_wl.Set(str(""))
            dr_push_tr_ht.Set(str("2"))
            dr_push_tr.Set(str("PH"))
            dr_prot_pl_wl_yes.Set(0)
            dr_prot_ph_tk_yes.Set(0)
            door_count += 1
        if 'SLID' in door_type_name:
            dr_pull_wl_ht.Set(str(""))
            dr_pull_wl.Set(str(""))
            dr_push_tr_ht.Set(str("2"))
            dr_push_tr.Set(str("TK"))
            dr_prot_pl_wl_yes.Set(0)
            dr_prot_ph_tk_yes.Set(0)
            door_count += 1
        # put a mark on the finished door
        el_id = door.Id
        door_xyz = door.Location.Point
        normal = XYZ.BasisZ
        if door_xyz:
            plane = Plane.CreateByNormalAndOrigin(normal, door_xyz)
            radius = 3
            start_angle = 0.0
            end_angle = 2.0 * math.pi
            arc = Arc.Create(plane, radius, start_angle, end_angle)
            circ_elements = [doc.Create.NewDetailCurve(active_view, arc)]

        for el in circ_elements:
            color = Color(255, 0, 255)
            ogs = OverrideGraphicSettings().SetProjectionLineColor(color)
            active_view.SetElementOverrides(el.Id, ogs)


if door_count == 1:
    forms.alert("{} door is updated".format(door_count))
else:
    forms.alert("{} doors are updated".format(door_count))

