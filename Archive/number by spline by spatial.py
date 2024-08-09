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
from pyrevit import script
import codecs
import csv
from Snippets._convert import convert_internal_to_m2
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter
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
from System.Collections.Generic import List, HashSet

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
# 🟡 select spline
filter_type = ISelectionFilter_Classes([ModelNurbSpline, DetailNurbSpline])
spl = selection.PickObject(ObjectType.Element, filter_type, "Select Spline")
selected_spline = doc.GetElement(spl).GeometryCurve

all_phase = list(doc.Phases)
phase = all_phase[-1]

windows_on_level = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Windows)\
    .WherePasses(ElementLevelFilter(active_level.Id)).WhereElementIsNotElementType().ToElements()

pt_at_spline = []
win_list = []

for win in windows_on_level:
    win_geo = win.get_Geometry(Options())
    win_bb = win_geo.GetBoundingBox()
    win_bb_mid = (win_bb.Min + win_bb.Max) / 2
    spl_pt = selected_spline.Project(win_bb_mid)
    intersection_pt = spl_pt.Parameter      # intersection of mid pt of window and spline
    pt_at_spline.append(intersection_pt)
    win_list.append(win)

combined_lst = list(zip(pt_at_spline, win_list))
combined_lst.sort(key=lambda x: x[0])

with rvt_transaction(doc, __title__):
    for index, (i, win) in enumerate(combined_lst, start=1):
        win_com_param = win.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
        room = win.FromRoom[phase]
        level_name = active_level.Name.split('-')[0]
        if room:
            room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
            room_number = room.Number
            zone_number = room.LookupParameter('Zone Number').AsValueString()
            win_com_param.Set('{}{}-{}-{}'.format('W', level_name, zone_number, str(index).zfill(3)))


