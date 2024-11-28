# -*- coding: utf-8 -*-

__title__ = 'NumBySpline'
__doc__ = """
This is script will number elements based on the
on the projected points of intersection of
spline.

How does this work:
Intersection points between element and spline are being
projected into spline then getting the parameters of the 
point on the its domain, i.e. 0 to 1.

HOW TO:
1. Select spline
2. Select Elements

Note: This is probably just a template for other elements
that need to be renumbered. To modify carefully later.
__________________________________
Author: Joven Mark Gumana
v1. 08 Jun 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
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

# TODO: 1. FLEXFORM CHOOSE OPTIONS FOR WALL OR FAMILY INSTANCE, WINDOWS, DOORS
# TODO: if wall, choose the wall method, else if option is in list [windows, door] do the other one,
'''create filter class for doors and window, selection by active view or rectangular selection'''





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
# 1️⃣ get the intersection of spline and walls
pt_at_spline = []
wall_list = []

for wall in selected_walls:
    wall_curve = wall.Location.Curve
    results = clr.Reference[IntersectionResultArray]()
    intersection_line = wall_curve.Intersect(selected_spline, results)
    if intersection_line == SetComparisonResult.Overlap:
        # 2️⃣ get the intersection point
        for result in results.Value:
            result_point = result.XYZPoint
            projected_pt = selected_spline.Project(result_point)    # create pt on intersection
            param_val = projected_pt.Parameter      # position of point on spline from 0 t0 1
            pt_at_spline.append(param_val)
            wall_list.append(wall)

combined_list = list(zip(pt_at_spline, wall_list))     # combine for sorting
combined_list.sort(key=lambda x: x[0])
print(combined_list)


# 3️⃣ set the parameter
with rvt_transaction(doc, "Renumber Walls"):
    for i, (_, wall) in enumerate(combined_list, start=1):
        wall_param = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
        wall_param.Set('WL-{}'.format(str(i).zfill(3)))
