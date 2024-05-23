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
from Snippets._x_selection import ISelectionFilter_Classes
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import pyrevit
import sys
import clr

clr.AddReference("System")

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
# 🔴 checking the wall type names
all_wall_type = FilteredElementCollector(doc).OfClass(WallType).WhereElementIsElementType().ToElements()

# ======================================================================================================
# 1️⃣ wall selection
selected_walls = get_multiple_elements()

if not selected_walls:
    with try_except():
        filter_type = ISelectionFilter_Classes([Wall])
        wall_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_walls = [doc.GetElement(wall) for wall in wall_list]

    if not selected_walls:
        forms.alert('No wall selected', exitscript=True)

# ======================================================================================================
with rvt_transaction(doc, __title__):
    new_walls = []
    try:
        for wall in selected_walls:

            wall_loc = wall.Location
            wall_curve = wall_loc.Curve

            wall_type = wall.WallType
            wall_type_name = wall_type.FamilyName
            wall_comp = wall_type.GetCompoundStructure()
            wall_layers = list(wall_comp.GetLayers())

            total_thickness = sum(layer.Width for layer in wall_layers)
            counter_thickness = 0
            # 2️⃣ separating the layers of the wall
            for layer in wall_layers:
                new_layers = []
                wall_mat            = doc.GetElement(layer.MaterialId)
                wall_func           = layer.Function
                wall_width          = layer.Width
                wall_mat_id         = layer.MaterialId

                # 3️⃣ creating new wall type
                new_layers.append(CompoundStructureLayer(wall_width, wall_func, wall_mat_id))
                new_wall_type       = wall_type.Duplicate(str(wall_func) + wall_mat.Name)
                new_wall_type.Name  = wall_mat.Name

                compound = CompoundStructure.CreateSimpleCompoundStructure(new_layers)
                new_wall_type.SetCompoundStructure(compound)


                # 4️⃣ figuring the center of layers for new walls
                offset = ((total_thickness - (2 * counter_thickness)) - wall_width) / 2
                if not wall.Flipped:
                    offset = -offset
                #  Creates a new curve that is an offset of the existing curve.
                offset_curve = wall_curve.CreateOffset(offset, XYZ.BasisZ)

                # 5️⃣ crate wall
                wall_create = Wall.Create(doc, offset_curve, new_wall_type.Id, active_level.Id, 10, 0, False, False)
                
                # accumulated thickness
                counter_thickness += wall_width
                # collect the new walls
                new_walls.append(wall_create)

    except Exception as e:
        print(e)

    # retain the original properties of un split wall
    else:
        for new_wall in new_walls:
            for ex_wall in selected_walls:

                base_off        = ex_wall.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET).AsDouble()
                top_cons        = ex_wall.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE).AsElementId()
                top_off         = ex_wall.get_Parameter(BuiltInParameter.WALL_TOP_OFFSET).AsDouble()
                unconnected_ht  = ex_wall.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsDouble()

                base_off_param          = new_wall.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)
                top_cons_param          = new_wall.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE)
                top_off_param           = new_wall.get_Parameter(BuiltInParameter.WALL_TOP_OFFSET)
                unconnected_ht_param    = new_wall.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM)

                if base_off:
                    base_off_param.Set(base_off)

                if top_cons == ElementId.InvalidElementId:
                    unconnected_ht_param.Set(unconnected_ht)
                else:
                    top_cons_param.Set(top_cons)
                    top_off_param.Set(top_off)

    # delete the original walls
    finally:
        if wall_create:
            for i in selected_walls:
                doc.Delete(i.Id)
        else:
            sys.exit()

# TODO: fix the duplication wall type names





















