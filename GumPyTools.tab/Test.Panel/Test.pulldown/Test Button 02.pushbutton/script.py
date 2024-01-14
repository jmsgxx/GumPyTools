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

phase_name = "MWP2"
phases = FilteredElementCollector(doc).OfClass(Phase).ToElements()
phase = next((x for x in phases if x.Name == phase_name), None)
if not phase:
    forms.alert("No phase named '{}'. Check the phase of the object and try again.".format(phase_name),
                exitscript=True)

# =====================================================================================================

all_doors = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors)\
    .WhereElementIsNotElementType()\
    .ToElements()

# =====================================================================================================

selected_rooms = get_multiple_elements()
if not selected_rooms:
    try:
        filter_type = ISelectionFilter_Classes([Room])
        room_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Rooms")
        selected_rooms = [doc.GetElement(el) for el in room_list]
        if not selected_rooms:
            forms.alert("No selected rooms. Exiting command", exitscript=True)
    except Exception as e:
        forms.alert("{} Exiting Command.".format(str(e)), exitscript=True)

# =====================================================================================================

for room in selected_rooms:
    if room.Area > 0:
        room_id = room.Id
        for door in all_doors:  # type: FamilyInstance
            door_type_id = door.GetTypeId()
            door_type = doc.GetElement(door_type_id)

            dr_pull_wl_ht   = door_type.LookupParameter('Door Protection Pull or Wall Height Code')
            dr_pull_wl      = door_type.LookupParameter('Door Protection Pull or Wall Code')
            dr_push_tr_ht   = door_type.LookupParameter('Door Protection Push or Track Height Code')
            dr_push_tr      = door_type.LookupParameter('Door Protection Push or Track Code')

            door_type_name = door_type.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()

            if door.Location:
                if hasattr(door, "FromRoom") and isinstance(phase, Phase):
                    with try_except():
                        to_room = door.ToRoom[phase]
                        if to_room:
                            if room_id == to_room.Id:
                                with rvt_transaction(doc, __title__):
                                    # for swing doors
                                    if 'SWG' in door_type_name:
                                        dr_pull_wl_ht.Set(str("2"))
                                        dr_pull_wl.Set(str("PL"))
                                        dr_push_tr_ht.Set(str("2"))
                                        dr_push_tr.Set(str("PH"))
                                    # for sliding doors
                                    elif 'SLID' in door_type_name:
                                        dr_pull_wl_ht.Set(str("2"))
                                        dr_pull_wl.Set(str("WL"))
                                        dr_push_tr_ht.Set(str("2"))
                                        dr_push_tr.Set(str("TK"))


"""
TODO: Make a list of doors separately, change the params from there then create a print statement to how
many doors was changed, try to segregate swing and sliding.
"""
