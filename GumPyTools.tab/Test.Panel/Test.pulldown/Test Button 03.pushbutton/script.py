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
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection
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


selected_walls = get_multiple_elements()

layerIds,layermat,layerfunc,layerwidth,layers,strucLayer,coreLayer,deckProfile = [],[],[],[],[],[],[],[]

# ======================================================================================================
# 1️⃣ DECONSTRUCT THE WALL

for elem in selected_walls:
    ids, mat, func, width, core, deck = [], [], [], [], [], []
    doc = elem.Document

    ui_unit = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()

    if isinstance(elem, ElementType):
        wall_type = elem
    elif isinstance(elem, Wall) and not elem.IsStackedWall and not elem.WallType.Kind == WallKind.Curtain:
        wall_type = elem.WallType   # this is the element
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
    layermat.append(mat)
    layerfunc.append(func)
    layerwidth.append(width)
    strucLayer.append(layers)
    coreLayer.append(core)
    deckProfile.append(deck)

