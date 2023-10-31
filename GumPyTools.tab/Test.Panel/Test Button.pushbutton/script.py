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

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # 🟠 ROOM PARAMETERS
    room_user_cat   = selected_room.LookupParameter('Room Inventory By User Category')
    room_user_item  = selected_room.LookupParameter('Room Inventory By User Items')
    room_user_desc  = selected_room.LookupParameter('Room Inventory By User Item Description')
    room_user_qty   = selected_room.LookupParameter('Room Inventory By User Item Quantities')

    elements = []
    for element in collector:
        element_cat = element.Category
        if element_cat is not None:
            element_name = element_cat.Name
            if element_name != "":
                elements.append(element)

    by_user_lst     = []    # family instance '(BY USER)'
    by_user_cat     = []
    by_user_item    = []
    by_user_desc    = []
    by_user_qty     = []
    by_user_obj_name = []

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

            if not filters or not is_filtered_by_user:
                if isinstance(element, FamilyInstance):
                    built_in_lst.append(element)
                # print("Element {} is affected by filter {}".format(element.Id.IntegerValue, filter_element.Name))

    for i in built_in_lst:
        print(type(i))

    # ╦  ╔═╗╔═╗╔═╗╔═╗
    # ║  ║ ║║ ║╚═╗║╣
    # ╩═╝╚═╝╚═╝╚═╝╚═╝ loose furniture
    # =====================================================================================================================

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
    by_user_cat_str     = '\n'.join(unique_by_user_desc)
    by_user_item_str    = '\n'.join(unique_by_user_item)
    by_user_desc_str    = '\n'.join(unique_by_user_desc)
    by_user_qty_str     = '\n'.join(split_by_user_qty)

    # 🟥 SET TO ROOM PARAMETER
    # ==========================================================================
    # if selected_room:
    #     if room_user_cat is not None:
    #         room_user_cat.Set(by_user_cat_str)
    #     if room_user_item is not None:
    #         room_user_item.Set(by_user_item_str)
    #     if by_user_desc_str and room_user_desc is not None:
    #         room_user_desc.Set(by_user_desc_str)
    #     if by_user_qty_str and room_user_qty is not None:
    #         room_user_qty.Set(by_user_qty_str)










    t.Commit()
# =============================================================================================




