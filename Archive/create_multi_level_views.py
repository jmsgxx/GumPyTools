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
from Snippets._x_selection import get_multiple_elements
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import clr
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection
# ======================================================================================================

all_vft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

vft_types = [i for i in all_vft if i.ViewFamily == ViewFamily.FloorPlan]

view_fam_types = []

for item in vft_types:
    vf_type_id = item.Id
    vf_type_element = doc.GetElement(vf_type_id)
    view_fam_types.append(vf_type_element)

# --------------------------------------------------------------------------------------------

all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()

ffl_level = []

for level in all_levels:
    level_name = level.Name
    if level_name.startswith("N") and level_name.endswith("FFL") and len(level_name) == 8:
        ffl_level.append(level)

b2_lev14_ffl = []

for lev in ffl_level:
    lev_name = lev.Name
    lev_name_part = lev_name.split("_")
    if lev_name_part[1].isdigit():
        lev_name_num = int(lev_name_part[1])
        if 0 < lev_name_num < 15:
            b2_lev14_ffl.append(lev)
    elif lev_name.startswith("N_B") or lev_name.startswith("N_L"):
        b2_lev14_ffl.append(lev)


with rvt_transaction(doc, __title__):
    with try_except():
        for levels in b2_lev14_ffl:
            levels_n = levels.Name
            num = levels_n.split("_")[1]
            for v_fam_t in view_fam_types:
                vft_name = v_fam_t.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
                if vft_name == "FFL":
                    vft_id = v_fam_t.Id
                    new_views = ViewPlan.Create(doc, vft_id, levels.Id)
                    new_views.Name = "MIC_{}_200".format(str(num).zfill(2))





all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()

for view in all_views:
    if view.ViewType == ViewType.FloorPlan:
        view_name = view.Name
        print(view_name)