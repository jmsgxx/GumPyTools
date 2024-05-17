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
import math
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
# wall_type = FilteredElementCollector(doc).OfClass(WallType).FirstElement()
#
# line_selection = get_multiple_elements()
#
#
#
# if not line_selection:
#     with try_except():
#         filter_type = CurvesFilter()
#         line_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Lines")
#         line_selection = [doc.GetElement(dr) for dr in line_list]
#
#         if not line_selection:
#             forms.alert("error", exitscript=True, warn_icon=False)
#
# wall_id = ElementId(1341927)
#
# with rvt_transaction(doc, __title__):
#     with try_except():
#         line_list = []
#         for line in line_selection:     # type: ModelLine
#             curve = line.GeometryCurve
#             start_pt = curve.GetEndPoint(0)
#             end_pt = curve.GetEndPoint(1)
#
#             lines = List[Curve]()
#             lines.Add(Line.CreateBound(start_pt, end_pt))
#
#         for el in line_list:
#             """
#             args: Document, list of curves, ElementID Wall, ElementID Level,
#              height dbl, offset dbl, flip bool, struc bool
#             """
#             Wall.Create(doc, lines, wall_id, active_level.Id, False)
# ======================================================================================================


def WallOrientation(x_wall):
    x_loc = x_wall.Location
    not_flipped = False
    if hasattr(x_loc, "Curve"):
        l_curve = x_loc.Curve
        if hasattr(x_wall, "Flipped"):
            not_flipped = x_wall.Flipped
        if str(type(l_curve)) == "Autodesk.Revit.DB.Line":
            if not_flipped:
                return x_wall.Orientation.ToVector().Reverse()
            else:
                return x_wall.Orientation.ToVector()
        else:
            x_direction = (l_curve.GetEndPoint(1) - l_curve.GetEndPoint(0)).Normalize()
            if not_flipped:
                return XYZ.BasisZ.CrossProduct(x_direction).Reverse()
            else:
                return XYZ.BasisZ.CrossProduct(x_direction)
    else:
        return None


# ======================================================================================================
selected_walls = get_multiple_elements()

layerIds, layer_mat, layer_func, layer_width, layers, strucLayer, coreLayer, deckProfile = [], [], [], [], [], [], [], []

# ======================================================================================================
# 1️⃣ DECONSTRUCT THE WALL

ui_unit = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()

for elem in selected_walls:
    ids, mat, func, width, core, deck = [], [], [], [], [], []
    doc = elem.Document

    if isinstance(elem, ElementType):
        wall_type = elem
    elif isinstance(elem, Wall) and not elem.IsStackedWall and not elem.WallType.Kind == WallKind.Curtain:
        wall_type = elem.WallType  # this is the element
    else:
        wall_type = None
    if wall_type:
        compStr = wall_type.GetCompoundStructure()
        # Get and sort layers by Id in reverse order (Highest id first)...
        layers = list(compStr.GetLayers())
        layers.sort(key=lambda x: x.LayerId)
        for layer in layers:
            ids.append(layer.LayerId)
            mat.append(wall_type.Document.GetElement(layer.MaterialId))
            func.append(layer.Function)
            width.append(UnitUtils.ConvertFromInternalUnits(layer.Width, ui_unit))
            core.append(compStr.IsCoreLayer(layer.LayerId))
            deck.append(doc.GetElement(layer.DeckProfileId))

    layerIds.append(ids)
    layer_mat.append(mat)
    layer_func.append(func)
    layer_width.append(width)
    strucLayer.append(layers)
    coreLayer.append(core)
    deckProfile.append(deck)
# ======================================================================================================
#  2️⃣ Get the wall curve
elem_width = []
elem_func = []
increments = []

with rvt_transaction(doc, __title__):
    for wall in selected_walls:
        doc = wall.Document

        try:
            counter = 0
            layer_width = []
            layer_func = []
            comp_struc = wall.WallType.GetCompoundStructure()
            num_layers = comp_struc.LayerCount
            while counter < num_layers:
                elem_width.append(UnitUtils.ConvertFromInternalUnits(comp_struc.GetLayerWidth(i), ui_unit))
                layer_func.append(comp_struc.GetLayerFunction(counter))
                counter += 1
        except:
            pass

        elem_func.append(layer_func)

        increments.append([sum(elem_width) for i in range(len(elem_width))])

        direction = WallOrientation(wall)

        elem_width_divided = [y / 2 for y in elem_width]

        wall_loc = wall.Location
        if isinstance(wall_loc, LocationCurve):
            wall_loc.Curve = wall_loc.Curve.CreateTransformed(Transform.CreateTranslation(
                direction * (math.fsum(elem_width_divided) - (increments[-1][-1] - math.fsum(elem_width_divided)))))

        wall_curve = wall_loc.Curve
        for i in elem_func:
            for j in i:
                print(type(j))
        print(wall_curve)

# ======================================================================================================
# 3️⃣ create compound structure

#
# new_fam_type_names = tolist(IN[1])
# functions = tolist(IN[2])
# materials = tolist(UnwrapElement(IN[3]))
# widths = tolist(IN[4])
# new_fam_types = []
#
# for elem, new_fam_type_name in zip(selected_walls, new_fam_type_names):
#     if isinstance(elem, ElementType):
#         fam_type = elem
#     elif isinstance(elem, Wall):
#         fam_type = elem.WallType
#     else:
#         pass
#     try:
#         new_fam_type = fam_type.Duplicate(new_fam_type_name)
#         layers = []
#         for material, width, function in zip(materials, widths, functions):
#             if isinstance(function, MaterialFunctionAssignment):
#                 layerFunction = function
#             else:
#                 layerFunction = System.Enum.Parse(MaterialFunctionAssignment, function)
#             layers.append(
#                 CompoundStructureLayer((UnitUtils.ConvertToInternalUnits(width, UIunit)), layerFunction, material.Id))
#         compound = CompoundStructure.CreateSimpleCompoundStructure(layers)
#         if fam_type.ToString() != 'Autodesk.Revit.DB.WallType':
#             compound.EndCap = EndCapCondition.NoEndCap
#         else:
#             pass
#         new_fam_type.SetCompoundStructure(compound)  # can stop in here
#         new_fam_types.append(new_fam_type)
#
#     except:
#         fec = FilteredElementCollector(doc).OfClass(fam_type.GetType())
#         type_dict = dict([(Element.Name.__get__(i), i) for i in fec])
#         n1 = unicode(new_fam_type_name)
#         if n1 in type_dict:
#             new_fam_types.append(type_dict[n1])
