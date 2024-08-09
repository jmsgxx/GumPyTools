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
from Snippets._convert import convert_internal_to_m2, convert_m_to_feet
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter, StairsFilter
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import pyrevit
import sys
import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum

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
# # 1️⃣ get all the revit link instance
# all_links_view = FilteredElementCollector(doc, active_view.Id).OfClass(RevitLinkInstance).ToElements()
#
# # 2️⃣ filter the link that you need
# rvt_link = None
# for link in all_links_view:
#     link_name = link.Name
#     if 'ARC' in link_name:
#         rvt_link = link
#
# linked_doc = rvt_link.GetLinkDocument()
#
# # 3️⃣ get all the rooms on your chosen revit link instance
# all_rooms_in_link_level = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Rooms)\
#             .WhereElementIsNotElementType().ToElements()
# ======================================================================================================


def get_faces_of_treads(staircase):
    """get the faces from geometry element"""
    faces_list = []
    stair_geo = staircase.get_Geometry(Options())
    for geo in stair_geo:
        if isinstance(geo, GeometryInstance):
            geo = geo.GetInstanceGeometry()
        if isinstance(geo, Solid):
            geo = [geo]
        for obj in geo:
            if isinstance(obj, Solid):
                for face in obj.Faces:
                    normal = face.ComputeNormal(UV(0, 0))   # face normal
                    if normal.IsAlmostEqualTo(XYZ(0, 0, 1)):
                        faces_list.append(face)
    return faces_list


def thicken_faces(document, list_faces, thick_num):
    """extrude the extracted normal face"""
    solids = []
    for face in list_faces:
        try:
            # plane normal origin
            normal = face.ComputeNormal(UV(0, 0))
            origin = face.Origin
            plane = Plane.CreateByNormalAndOrigin(normal, origin)
            SketchPlane.Create(document, plane)
            profile = face.GetEdgesAsCurveLoops()
            if not profile:
                continue
            # create solid
            solid = GeometryCreationUtilities.CreateExtrusionGeometry(profile, normal, thick_num)
            solids.append(solid)
        except Exception as err:
            print(err)

    # union solid
    if solids:
        try:
            union_solid = solids[0]
            for solid in solids[1:]:
                union_solid = BooleanOperationsUtils.ExecuteBooleanOperation(union_solid, solid,
                                                                             BooleanOperationsType.Union)
            # Create DirectShape element
            ds = DirectShape.CreateElement(document, ElementId(BuiltInCategory.OST_Mass))
            ds.SetShape([union_solid])
            document.Regenerate()
        except Exception as e:
            print(e)


all_categories = doc.Settings.Categories

cat_dict = {
    "Stairs": BuiltInCategory.OST_Stairs,
    "Floors": BuiltInCategory.OST_Floors
}

# TODO: Error expected BuiltInCategory, got Stairs

try:
    components = [Label('Mass Creation for Headroom:'),
                  ComboBox('cat_select', cat_dict),
                  Label('Specify Height in mm'),
                  TextBox('ht_input'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Create View Plan', components)
    form.show()

    user_input = form.values
    selection_cat = user_input['cat_select']
    input_ht = user_input['ht_input']

    # ------------------------------------------------------------------------------------------
    # 🟡 stair selection
    # selected_stair = get_multiple_elements()
    #
    # if not selected_stair:
    #     filter_type = StairsFilter()
    #     stair_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Stair")
    #     selected_stair = [doc.GetElement(el) for el in stair_list]

    # enum_name = Enum.GetName(BuiltInCategory, selection_cat.IntegerValue)
    # bic_dic = {
    #     "OST_Floor": BuiltInCategory.OST_Floors,
    #     "OST_Stairs": BuiltInCategory.OST_Stairs
    # }
    # for k,v in bic_dic:
    # bic = bic_dic.get(enum_name)
    # print(bic)
    selected_elements = FilteredElementCollector(doc, active_view.Id).OfCategory(selection_cat)\
        .WhereElementIsNotElementType().ToElements()
    # ------------------------------------------------------------------------------------------
    # 🟩 execute
    faces = []
    for el in selected_elements:
        faces.extend(get_faces_of_treads(el))

    with rvt_transaction(doc, __title__):
        input_to_m = input_ht / 1000
        thickness = convert_m_to_feet(input_to_m)
        # thicken_faces(doc, faces, thickness)
except Exception as e:
    print("Error {}".format(e))
else:
    forms.alert(title="Headroom Mass", msg="Mass Created", warn_icon=False, exitscript=False)






