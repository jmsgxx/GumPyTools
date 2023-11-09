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

all_rooms_in_link_level = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
    # for room_link in all_rooms_in_link_level:   # exclude the unplaced rooms
    #     if room_link and room_link.Location:
    #         room_loc = room_link.Location.Point
    #
    #         room_copy = doc.Create.NewRoom(active_level, UV(room_loc.X, room_loc.Y))
    #         #  name
    #         room_copy_name = room_copy.get_Parameter(BuiltInParameter.ROOM_NAME)
    #         rm_link_name = room_link.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
    #         if rm_link_name:
    #             room_copy_name.Set(str(rm_link_name))
    #         else:
    #             continue
    #         # number
    #         room_copy_number = room_copy.get_Parameter(BuiltInParameter.ROOM_NUMBER)
    #         rm_link_number = room_link.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    #         if rm_link_number:
    #             room_copy_number.Set(str(rm_link_number))
    #         else:
    #             continue
    #         #    print
    #         print("Room Name:   {}".format(rm_link_name))  # print statement to check rm_link_name
    #         print("Room Number: {}".format(rm_link_number))  # print statement to check rm_link_number
    #         print('-' * 50)

    # CHECK THE CURRENT MODEL
    current_level_filter = ElementLevelFilter(active_level.Id)

    rooms_current = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Rooms)\
        .WherePasses(current_level_filter).WhereElementIsNotElementType().ToElements()

    # print("Total Room in link:      {}".format(len(all_rooms_in_link_level)))
    # print("Total Room in current:   {}".format(len(rooms_current)))
    #
    # for room_cur in rooms_current:
    #     print(room_cur.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString())
    #     print(room_cur.Number)
    #     print('=' * 50)


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
            room_active = element.Room[phase]
            print(room_active)

        # TODO wait for reply from discord, might get an idea how to fix this, find a way to get the room
        """update1: no solution
            update 2: reverse engineer do the thing in mep, link archi
        """

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
