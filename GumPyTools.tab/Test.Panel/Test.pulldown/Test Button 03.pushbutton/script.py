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
# TODO: select spline

filter_type = ISelectionFilter_Classes([ModelNurbSpline, DetailNurbSpline])
spl = selection.PickObject(ObjectType.Element, filter_type, "Select Spline")
selected_spline = doc.GetElement(spl).GeometryCurve

# TODO: select walls
selected_walls = get_multiple_elements()

if not selected_walls:
    with try_except():
        filter_type = ISelectionFilter_Classes([Wall])
        wall_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_walls = [doc.GetElement(wl) for wl in wall_list]

    if not selected_walls:
        forms.alert('No wall selected', exitscript=True)

points = []
results = clr.Reference[IntersectionResultArray]()
param_wall = []

param_wall_pairs = []

for wall in selected_walls:
    wall_curve = wall.Location.Curve
    intersection_line = wall_curve.Intersect(selected_spline, results)
    if intersection_line == SetComparisonResult.Overlap:
        for result in results.Value:
            pt = result.XYZPoint
            points.append(pt)
            # -----------------------------------------------
            # how to get the parameter properly
            intersection_result = wall_curve.Project(pt)
            param = intersection_result.Parameter
            total_length = wall_curve.Length
            normalized_param = int(param) / total_length
            point_on_wall = wall_curve.Evaluate(normalized_param, True)
            param_wall_pairs.append((point_on_wall, wall))
            print(type(param))
            print('Param:{}'.format(param))
            print('Total Length:{}'.format(total_length))
            print('Normalized Param:{}'.format(normalized_param))
            print('Point on wall:{}'.format(point_on_wall))

# param_wall_pairs.sort(key=lambda x: x[0])
#
# # -------------------------------------------------------------------
#
# with rvt_transaction(doc, __title__):
#     for i, (_, wall) in enumerate(param_wall_pairs, start=1):
#         wall_param = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
#         wall_param.Set('Wall-{}'.format(i))

# TODO: check the intersection
# TODO: get the intersection point
# TODO: sor the intersection point and set
