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
from Snippets._convert import convert_m_to_feet
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


def get_faces_of_floors(floor):
    faces_ = []
    try:
        floor_geo = floor.get_Geometry(Options())
        print("Floor Geometry: ", floor_geo)
        for geo in floor_geo:
            if isinstance(geo, GeometryInstance):
                geo = geo.GetInstanceGeometry()
            if isinstance(geo, Solid):
                geo = [geo]
            for obj in geo:
                if isinstance(obj, Solid):
                    print("Solid found: ", obj)
                    for face in obj.Faces:
                        normal = face.ComputeNormal(UV(0, 0))
                        print("Face normal: ", normal)
                        if normal.IsAlmostEqualTo(XYZ(0, 0, 1)):
                            faces_.append(face)
        print("Found {} faces".format(len(faces_)))
    except Exception as e:
        print("Error in get_faces_of_floors: {}".format(e))
    return faces_


def thicken_faces(_doc, _faces, _thickness):
    solids = []
    for face in _faces:
        try:
            # Create a plane from the face's normal and origin
            normal = face.ComputeNormal(UV(0, 0))
            origin = face.Origin
            plane = Plane.CreateByNormalAndOrigin(normal, origin)
            sketch_plane = SketchPlane.Create(_doc, plane)
            profile = face.GetEdgesAsCurveLoops()
            if not profile:
                print("No profile found for face: {}".format(face))
                continue
            print("Profile: ", profile)

            # Create a solid from the face profile and thickness
            solid = GeometryCreationUtilities.CreateExtrusionGeometry(profile, normal, _thickness)
            solids.append(solid)
        except Exception as e:
            print("Error creating solid: {}".format(e))

    # Union all solids into a single solid
    if solids:
        try:
            union_solid = solids[0]
            for solid in solids[1:]:
                union_solid = BooleanOperationsUtils.ExecuteBooleanOperation(union_solid, solid,
                                                                             BooleanOperationsType.Union)

            # Create a DirectShape element to hold the unioned solid
            direct_shape = DirectShape.CreateElement(_doc, ElementId(BuiltInCategory.OST_Mass))
            direct_shape.SetShape([union_solid])
            _doc.Regenerate()
            print("Created DirectShape: {}".format(direct_shape.Id))
        except Exception as e:
            print("Error creating unioned DirectShape: {}".format(e))


try:
    selected_floors = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Floors) \
        .WhereElementIsNotElementType().ToElements()

    print("Selected floors: ", selected_floors)

    faces = []

    for floor in selected_floors:
        try:
            faces.extend(get_faces_of_floors(floor))
        except Exception as e:
            print("Error processing floor: {}".format(e))
            continue

    print("Total faces found: ", len(faces))

    with rvt_transaction(doc, __title__):
        thickness = convert_m_to_feet(2.1)
        thicken_faces(doc, faces, thickness)
except Exception as e:
    print("Error: {}".format(e))




