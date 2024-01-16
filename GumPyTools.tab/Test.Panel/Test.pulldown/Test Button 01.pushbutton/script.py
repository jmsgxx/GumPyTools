# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.UI.Selection import ISelectionFilter, Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
from Snippets._x_selection import DoorCustomFilter, get_multiple_elements
from Snippets._context_manager import try_except, rvt_transaction
from Autodesk.Revit.DB import *
import pyrevit
from pyrevit import forms

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
all_rooms = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

# rooms_list_bi = []
# rm_list_blp = []
room_dict = {}

for room in all_rooms:  # type: Room
    if room.Area > 0:
        room_name_bi = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
        rm_name_blp = room.LookupParameter('Room_Name_BLP').AsString()
        room_dict[room_name_bi] = rm_name_blp
        # if room_name_bi not in rooms_list_bi:
        #     rooms_list_bi.append(room_name_bi)

for i, rm in enumerate(sorted(room_dict)):
    print("{}. (SKA_NAME){} :\n\t\t (BLP_NAME){}".format(str(i).zfill(3), rm, room_dict[rm]))
    print('\n\n')
    # print(rm)

