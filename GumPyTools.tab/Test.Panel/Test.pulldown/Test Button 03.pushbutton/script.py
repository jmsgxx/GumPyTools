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
from System.Collections.Generic import List

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

# 🟡 select walls
selected_walls = get_multiple_elements()

if not selected_walls:
    with try_except():
        filter_type = ISelectionFilter_Classes([Wall])
        wall_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_walls = [doc.GetElement(wl) for wl in wall_list]

    if not selected_walls:
        forms.alert('No wall selected', exitscript=True)

# -----------------------------------------------------------------------------------
# 1️⃣ get the intersection of spline and walls, put in tuple
intersect_pts = []

for wall in selected_walls:
    wall_curve = wall.Location.Curve
    results = clr.Reference[IntersectionResultArray]()
    intersection_line = wall_curve.Intersect(selected_spline, results)
    if intersection_line == SetComparisonResult.Overlap:
        for result in results.Value:
            intersect_pts.append((result.XYZPoint, wall))

# 2️⃣ get the parameter by Project. will return a geometry, .Parameter is the position of point on the spline
pt_at_spline = []
for el in intersect_pts:
    projected_pt = selected_spline.Project(el[0])
    param_val = projected_pt.Parameter      # position of point in spline
    pt_at_spline.append((param_val, el[1]))     # el[1] is wall element

print(pt_at_spline)

pt_at_spline.sort(key=lambda x: x[0])

# 3️⃣ set the parameter
with rvt_transaction(doc, "Renumber Walls"):
    for i, (_, wall) in enumerate(pt_at_spline, start=1):
        wall_param = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
        wall_param.Set('WL-{}'.format(str(i).zfill(3)))
