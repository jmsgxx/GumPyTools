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
# TODO 1: get all the windows
# TODO 2: get all the rooms FromRoom to ToRoom
# TODO 3: prepare the parameters to write on syntax
# TODO 4: integrate spline


# 🟡 select spline
filter_type = ISelectionFilter_Classes([ModelNurbSpline, DetailNurbSpline])
spl = selection.PickObject(ObjectType.Element, filter_type, "Select Spline")
selected_spline = doc.GetElement(spl).GeometryCurve


all_phase = list(doc.Phases)
phase = all_phase[-1]

windows_on_level = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Windows)\
    .WherePasses(ElementLevelFilter(active_level.Id)).WhereElementIsNotElementType().ToElements()

# selection.SetElementIds(List[ElementId]([i.Id for i in windows_on_level]))

for win in windows_on_level:
    win_curve = win.Geometry.Curve
    print(win_curve)

    # results = clr.Reference[IntersectionResultArray]()
    # intersection_pt = win_curve.Intersect(selected_spline, results)
    # if intersection_pt == SetComparisonResult.Overlap:
    #     print('Found intersection')
    # room = win.FromRoom[phase]
    # if room:
    #     room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    #     room_number = room.Number
    #     zone_number = room.LookupParameter('Zone Number').AsValueString()

