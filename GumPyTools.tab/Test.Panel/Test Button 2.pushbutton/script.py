# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
import pyrevit
from pyrevit import script, forms, revit
from System.Collections.Generic import List
from datetime import datetime

import clr
clr.AddReference("System")


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================


doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
all_phase = list(doc.Phases)
phase = (all_phase[-1])

list_of_categories = List[BuiltInCategory]([
    BuiltInCategory.OST_DataDevices,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_CommunicationDevices,
    BuiltInCategory.OST_SecurityDevices,
    BuiltInCategory.OST_NurseCallDevices])

level_filter = ElementLevelFilter(active_level.Id)
category_filter = ElementMulticategoryFilter(list_of_categories)
combined_filter = LogicalAndFilter(category_filter, level_filter)

all_elements_in_level = FilteredElementCollector(doc).WherePasses(combined_filter).WhereElementIsNotElementType().ToElements()

# ROOM
all_links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# Find the specific link
ar_model = None
for link in all_links:
    link_name = link.Name
    if 'ARC' in link_name:
        ar_model = link

linked_doc = ar_model.GetLinkDocument()

all_rooms_in_level = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
    for room in all_rooms_in_level:
        boundary_option = SpatialElementBoundaryOptions()
        boundary_segments = room.GetBoundarySegments(boundary_option)

        if boundary_segments:
            base = CurveLoop()

            for segment in boundary_segments[0]:
                base.Append(segment.GetCurve())
            try:
                cuboid = GeometryCreationUtilities.CreateExtrusionGeometry([base], XYZ.BasisZ, 2100)

                num_faces = cuboid.Faces.Size
                num_edges = cuboid.Edges.Size

                print('Number of faces: ', num_faces)
                print('Number of edges: ', num_edges)

            except Exception as e:
                print("An error occurred: ", e)

        else:
            print("No boundary segments found for room.")
    # ================================================================================================================
    for element in all_elements_in_level:
        if element:
            #  type param
            el_type_id = element.GetTypeId()
            el_type = doc.GetElement(el_type_id)
            if el_type:
                type_description_param = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)
                description_param = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
                type_image_param = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_IMAGE)
                # print(type_description_param.AsString())
                # print(type_image_param.AsValueString())


            #  instance param
            element_id = element.Id
            category_name = element.Category.Name
            family_name = element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()

            element_location = element.Location
            if element_location is not None:
                el_loc_point = element_location.Point  # xyz printing ok
                pos_x = el_loc_point.X
                pos_y = el_loc_point.Y
                pos_z = el_loc_point.Z

        # TODO wait for reply from discord, might get an idea how to fix this, find a way to get the room
        """update: no solution"""

    # unique_fam_names = set()
    #
    # for element in all_elements_in_link:
    #     if element is not None and element.Category is not None:
    #         family_name = element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
    #         unique_fam_names.add(family_name)
    #
    # for name in sorted(unique_fam_names):
    #     print(name.AsValueString())

    t.Commit()
