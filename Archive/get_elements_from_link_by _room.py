# -*- coding: utf-8 -*-

__title__ = 'Test Button 03'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets._convert import convert_internal_to_sqm, convert_m_to_feet
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter, StairsFilter
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import sys
import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection


# ======================================================================================================

all_links_view = FilteredElementCollector(doc, active_view.Id).OfClass(RevitLinkInstance).ToElements()

architectural_link = None
for link in all_links_view:
    link_name = link.Name
    parts_link = link_name.split(':')
    new_sel_link = parts_link[0]
    if "Architectural" in new_sel_link:
        architectural_link = link

link_model = architectural_link.GetLinkDocument()

all_rooms_in_link = FilteredElementCollector(link_model).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

with Transaction(doc, __title__) as t:
    t.Start()

    data_dict = {}
    for room in all_rooms_in_link:
        if room and room.Location:  # exclude the unplaced rooms
            room_loc = room.Location.Point

            room_copy = doc.Create.NewRoom(active_level, UV(room_loc.X, room_loc.Y))
            room_copy_name = room_copy.get_Parameter(BuiltInParameter.ROOM_NAME)

            rm_link_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
            if room_copy_name:
                room_copy_name.Set(str(rm_link_name.upper()))
            # 🟩 new rooms attribute
            room_name = room_copy_name.AsValueString()
            room_number = room.Number

            # 🟡 for filter
            room_geo = room.ClosedShell
            room_bb = room_geo.GetBoundingBox()
            bb_min = room_bb.Min
            bb_max = room_bb.Max
            room_outline = Outline(bb_min, bb_max)
            bb_filter = BoundingBoxIsInsideFilter(room_outline)

            get_cat = [BuiltInCategory.OST_ElectricalFixtures,
                       BuiltInCategory.OST_LightingFixtures]

            collector = FilteredElementCollector(doc).WherePasses(bb_filter).WhereElementIsNotElementType().ToElements()

            elec_fix = []
            light_fix = []
            for el in collector:
                try:
                    if el.Category.Id.IntegerValue in [int(cat) for cat in get_cat]:
                        if el.Category.Name == 'Electrical Fixtures':
                            elec_fix.append(el)
                        else:
                            light_fix.append(el)
                except:
                    pass
            key_list = (room_name, room_number)
            val_list = [len(elec_fix), len(light_fix)]
            data_dict[key_list] = val_list

    if t.GetStatus() == TransactionStatus.Started:
        t.RollBack()

for room_name_num, counts in data_dict.items():
    print("Name:{}-Number:{}: [Electrical: {}, Lighting: {}]".format(room_name_num[0], room_name_num[1], counts[0], counts[1]))
