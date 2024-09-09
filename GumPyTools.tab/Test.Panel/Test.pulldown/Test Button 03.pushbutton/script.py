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
from Snippets._x_selection import ISelectionFilter_Classes
from pyrevit import forms
from Snippets._context_manager import rvt_transaction
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
# 🟡 select spline
filter_type = ISelectionFilter_Classes([ModelNurbSpline, DetailNurbSpline])
spl = selection.PickObject(ObjectType.Element, filter_type, "Select Spline")
selected_spline = doc.GetElement(spl).GeometryCurve

all_phase = list(doc.Phases)
phase = all_phase[-1]

rooms_on_level = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Rooms)\
    .WherePasses(ElementLevelFilter(active_level.Id)).WhereElementIsNotElementType().ToElements()

pt_at_spline = []
rm_list = []

for rm in rooms_on_level:
    rm_geo = rm.get_Geometry(Options())
    rm_bb = rm_geo.GetBoundingBox()
    rm_bb_mid = (rm_bb.Min + rm_bb.Max) / 2
    spl_pt = selected_spline.Project(rm_bb_mid)
    intersection_pt = spl_pt.Parameter      # intersection of mid pt of window and spline
    pt_at_spline.append(intersection_pt)
    rm_list.append(rm)

combined_lst = list(zip(pt_at_spline, rm_list))
combined_lst.sort(key=lambda x: x[0])

with rvt_transaction(doc, __title__):
    try:
        for index, (i, rm) in enumerate(combined_lst, start=1):
            level_name = active_level.Name.split('-')[0]
            if rm:
                room_name = rm.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                room_number = rm.get_Parameter(BuiltInParameter.ROOM_NUMBER)
                room_number.Set('{}{}-{}'.format('R', level_name, str(index).zfill(3)))
    except Exception as e:
        print(e)
