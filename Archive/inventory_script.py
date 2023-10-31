# -*- coding: utf-8 -*-

__title__ = 'Test Button'
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
from pyrevit import forms, revit
from System.Collections.Generic import List
from collections import Counter

import clr
import revitron
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


# SELECT A ROOM
with forms.WarningBar(title='Pick an element:'):
    selected_room = revit.pick_element()

el_cat          = selected_room.Category.Name

if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)

# COLLECTOR OF ELEMENTS TO SET '(BY USER)'
collector = FilteredElementCollector(doc, active_view.Id).WhereElementIsNotElementType()

# 🟠 ROOM PARAMETERS
# loose param
room_user_cat   = selected_room.LookupParameter('Room Inventory By User Category')
room_user_item  = selected_room.LookupParameter('Room Inventory By User Items')
room_user_desc  = selected_room.LookupParameter('Room Inventory By User Item Description')
room_user_qty   = selected_room.LookupParameter('Room Inventory By User Item Quantities')

# built-in param
num_var = ""
room_inv_cat            = selected_room.LookupParameter('Room Inventory Category {}'.format(num_var))
room_inv_cat_item_desc  = selected_room.LookupParameter('Room Inventory Category {} Item Description'.format(num_var))
room_inv_cat_item_qty   = selected_room.LookupParameter('Room Inventory Category {} Item Quantities'.format(num_var))
room_inv_cat_item       = selected_room.LookupParameter('Room Inventory Category {} Items'.format(num_var))


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    elements = []
    for element in collector:
        element_cat = element.Category
        if element_cat is not None:
            element_name = element_cat.Name
            if element_name != "":
                elements.append(element)

    by_user_lst         = []    # family instance '(BY USER)'
    built_in_lst = []

    for element in elements:
        el_type_id  = element.GetTypeId()
        el_symbol   = doc.GetElement(el_type_id)
        if el_symbol is not None:
            # parameter
            manufacturer_val    = el_symbol.get_Parameter(BuiltInParameter.ALL_MODEL_MANUFACTURER)
            filters             = active_view.GetFilters()

            is_filtered_by_user = False

            for filter_id in filters:
                filter_element = doc.GetElement(filter_id)  # type 'ParameterFilterElement'

                # Get the filter from the ParameterFilterElement
                el_filter = filter_element.GetElementFilter()  # type 'LogicalAndFilter' / 'LogicalOrFilter'

                # Check if the element satisfies the filter
                if el_filter.PassesFilter(element):
                    if filter_element.Name == 'By User':
                        is_filtered_by_user = True
                        if manufacturer_val is not None and not manufacturer_val.IsReadOnly:
                            manufacturer_val.Set('(BY USER)')
                            by_user_lst.append(element)

            category = element.Category
            categories = [int(BuiltInCategory.OST_Casework),
                          int(BuiltInCategory.OST_GenericModel),
                          int(BuiltInCategory.OST_SpecialityEquipment),
                          int(BuiltInCategory.OST_Furniture),
                          int(BuiltInCategory.OST_MedicalEquipment),
                          int(BuiltInCategory.OST_PlumbingFixtures)]
            if not filters or not is_filtered_by_user:  # returns true if objects has no filter and not under '(BY USER)'
                if isinstance(category, Category) and category.Id.IntegerValue in categories:
                    built_in_lst.append(element)
                # print("Element {} is affected by filter {}".format(element.Id.IntegerValue, filter_element.Name))


    # ╦  ╔═╗╔═╗╔═╗╔═╗
    # ║  ║ ║║ ║╚═╗║╣
    # ╩═╝╚═╝╚═╝╚═╝╚═╝ loose furniture
    # =====================================================================================================================

    by_user_cat         = []
    by_user_item        = []
    by_user_desc        = []
    by_user_qty         = []
    by_user_obj_name    = []

    for item in by_user_lst:
        if item:
            # 🟢 GET PARAMS OF LOOSE FURNITURE
            model_element_id = item.GetTypeId()
            model_type = doc.GetElement(model_element_id)
            """ this is the parameter to get that will set in room """
            model_type_cat_param    = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsValueString()  # type comments
            model_type_item_param   = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID).AsValueString()  # type mark
            model_type_desc_param   = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION).AsValueString()  # type description

            by_user_cat.append(model_type_cat_param)
            by_user_item.append(model_type_item_param)
            by_user_desc.append(model_type_desc_param)

            by_user_obj_name.append(item.Name)

            # print("Element ID: {} for {}".format(item.Id.IntegerValue, model_type_cat_param))

    # generate quantity of items
    obj_counter = Counter(by_user_obj_name)
    unique_by_user_obj_name = set(by_user_obj_name)
    for item in unique_by_user_obj_name:
        by_user_qty.append(obj_counter[item])

    split_by_user_qty = [str(item) for item in by_user_qty]

    # convert to set to get the unique items
    unique_by_user_cat      = set(by_user_cat)
    unique_by_user_item     = set(by_user_item)
    unique_by_user_desc     = set(by_user_desc)

    #  convert to string
    by_user_cat_str     = '\n'.join(unique_by_user_cat)
    by_user_item_str    = '\n'.join(unique_by_user_item)
    by_user_desc_str    = '\n'.join(unique_by_user_desc)
    by_user_qty_str     = '\n'.join(split_by_user_qty)

    # 🟥 SET TO ROOM PARAMETER
    # ======================================
    # if selected_room:
    #     if room_user_cat is not None:
    #         room_user_cat.Set(by_user_cat_str)
    #     if room_user_item is not None:
    #         room_user_item.Set(by_user_item_str)
    #     if by_user_desc_str and room_user_desc is not None:
    #         room_user_desc.Set(by_user_desc_str)
    #     if by_user_qty_str and room_user_qty is not None:
    #         room_user_qty.Set(by_user_qty_str)


    # ╔╗ ╦ ╦╦╦ ╔╦╗  ╦╔╗╔
    # ╠╩╗║ ║║║  ║───║║║║
    # ╚═╝╚═╝╩╩═╝╩   ╩╝╚╝ built-in objects
    # ==========================================================================================================

    built_in_cat        = []
    built_in_item       = []
    built_in_desc       = []
    built_in_qty        = []
    built_in_obj_name   = []

    for item in built_in_lst:
        if item:
            # 🟢 GET PARAMS OF BUILT-IN FURNITURE
            model_element_id = item.GetTypeId()
            model_type = doc.GetElement(model_element_id)
            """ this is the parameter to get that will set in room """
            model_type_cat_param    = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsValueString()  # type comments
            model_type_item_param   = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID).AsValueString()  # type mark
            model_type_desc_param   = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION).AsValueString()  # type description

            built_in_cat.append(model_type_cat_param)
            built_in_item.append(model_type_item_param)
            built_in_desc.append(model_type_desc_param)
            built_in_obj_name.append(item.Name)

    # 1️⃣ SET THE TYPE COMMENTS
    unique_built_in_cat = set(built_in_cat)
    filtered_cat = [value for value in unique_built_in_cat if value not in [None, 'Door Feature', 'N/A']]

    for i, value in enumerate(filtered_cat, start=1):
        room_inv_cat = selected_room.LookupParameter('Room Inventory Category {}'.format(i))
        # if room_inv_cat is not None:
        #     room_inv_cat.Set(value)
        #     print("{}:{}".format(i, value))

    # 2️⃣ SET THE TYPE MARK
    unique_built_in_item = set(built_in_item)
    filtered_item = [value for value in unique_built_in_item if value not in [None, '0', '']]

    print(filtered_item)

    for i, value in enumerate(filtered_item, start=1):
        room_inv_cat_item_desc = selected_room.LookupParameter('Room Inventory Category {} Item Description'.format(i))
        if room_inv_cat_item is not None:
            room_inv_cat_item.Set(value)
            print("{}:{}".format(i, value))







    t.Commit()
# =============================================================================================




