# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
test script
__________________________________
Author: Joven Mark Gumana
v1. 21 May 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import ISelectionFilter_Classes
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Structure import StructuralType
import pyrevit
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


def get_points_on_curve(curve, n):
    points = []
    for i in range(n+1):
        param = float(i) / n
        point = curve.Evaluate(float(param), True)
        points.append(point)
    return points

# 1️⃣ collect the grids


selected_model_arc = get_multiple_elements()
all_gen = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()

if not selected_model_arc:
    with try_except():
        filter_type = ISelectionFilter_Classes([ModelArc])
        arc_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Arc")
        selected_model_arc = [doc.GetElement(ell) for ell in arc_list]

    if not selected_model_arc:
        forms.alert('No wall selected', exitscript=True)

with rvt_transaction(doc, __title__):
    for arc in selected_model_arc:
        fam_ins = None
        for i in all_gen:   # type: FamilyInstance
            if i.Name == 'Family1':
                fam_ins = i
                break
        fam_sym = fam_ins.Symbol
        arc_geom = arc.GeometryCurve
        arc_geom_cen = arc_geom.Center
        arc_line = Line.CreateUnbound(arc_geom_cen, XYZ.BasisY)
        x_pts = get_points_on_curve(arc_geom, 4)
        try:
            for pt in x_pts:
                el_id = []  # Initialize the list here
                fam_create = doc.Create.NewFamilyInstance(pt, fam_sym, StructuralType.NonStructural)
                el_id.append(fam_create.Id)
                cent_to_crv_pt = Line.CreateBound(arc_geom_cen, pt)
                cent_dir = arc_line.Direction
                line_dir = cent_to_crv_pt.Direction
                ang = cent_dir.AngleTo(line_dir)
                fam_loc = fam_create.Location
                if isinstance(fam_loc, LocationPoint):
                    fam_point = fam_loc.Point
                    rotation_axis = Line.CreateBound(fam_point, fam_point + XYZ.BasisZ)
                ElementTransformUtils.RotateElements(doc, List[ElementId](el_id), rotation_axis, ang)
        except Exception as e:
            print(e)

# TODO its not working as intended after the family creation, need to work on the rotation line


