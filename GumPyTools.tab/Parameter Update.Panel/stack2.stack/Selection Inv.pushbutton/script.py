# -*- coding: utf-8 -*-

__title__ = 'Selection Inv'
__doc__ = """
NOT FINISHED. NEED TO COLLECT THE ELEMENTS
PROPERLY.

This script will select only specific
elements to be assigned on a specific
room.

REASON:
There are multiple rooms in a single
active view.

HOW TO:
1. Select a room.
2. If there's no error, window select
elements to update.
--------------------------------------
v1: 15 Nov 2023
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
from datetime import datetime

import clr
import revitron
clr.AddReference("System")



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

# Use the rectangle picking tool to identify model elements to select.
collector = uidoc.Selection.PickElementsByRectangle("Select by rectangle")

# 🟠 ROOM PARAMETERS
# loose param
room_user_cat   = selected_room.LookupParameter('Room Inventory By User Category')
room_user_item  = selected_room.LookupParameter('Room Inventory By User Items')
room_user_desc  = selected_room.LookupParameter('Room Inventory By User Item Description')
room_user_qty   = selected_room.LookupParameter('Room Inventory By User Item Quantities')


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

    by_user_lst  = []    # family instance '(BY USER)'
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
    filtered_by_user_cat    = [item for item in by_user_cat if item is not None]
    unique_by_user_cat      = set(filtered_by_user_cat)
    filtered_by_user_item   = [item for item in by_user_item if item is not None]
    unique_by_user_item     = set(filtered_by_user_item)
    unique_by_user_desc     = set(by_user_desc)

    #  convert to string
    by_user_cat_str     = '\n'.join(unique_by_user_cat)
    by_user_item_str    = '\n'.join(unique_by_user_item)
    by_user_desc_str    = '\n'.join(unique_by_user_desc)
    by_user_qty_str     = '\n'.join(split_by_user_qty)

    # 🟥 SET TO ROOM PARAMETER
    # ======================================
    if selected_room:
        if room_user_cat is not None:
            room_user_cat.Set(by_user_cat_str)
        if room_user_item is not None:
            room_user_item.Set(by_user_item_str)
        if by_user_desc_str and room_user_desc is not None:
            room_user_desc.Set(by_user_desc_str)
        if by_user_qty_str and room_user_qty is not None:
            room_user_qty.Set(by_user_qty_str)


    # ╔╗ ╦ ╦╦╦ ╔╦╗  ╦╔╗╔
    # ╠╩╗║ ║║║  ║───║║║║
    # ╚═╝╚═╝╩╩═╝╩   ╩╝╚╝ built-in objects
    # ==========================================================================================================

    bi_archi        = []
    bi_cab_furn     = []
    bi_san_fit      = []
    bi_wall_prot    = []

    for item in built_in_lst:
        model_element_id = item.GetTypeId()
        model_type = doc.GetElement(model_element_id)
        # ⭕
        built_in_cat = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsValueString()
        if built_in_cat     == 'ARCHITECTURAL WORK':
            bi_archi.append(item)
        elif built_in_cat   == 'CABINETRY/BUILT-IN FURNITURE':
            bi_cab_furn.append(item)
        elif built_in_cat   == 'SANITARY FITMENT':
            bi_san_fit.append(item)
        elif built_in_cat   == 'WALL PROTECTION':
            bi_wall_prot.append(item)

    # built-in param
    room_inv_cat1            = selected_room.LookupParameter('Room Inventory Category 1')
    room_inv_cat2            = selected_room.LookupParameter('Room Inventory Category 2')
    room_inv_cat3            = selected_room.LookupParameter('Room Inventory Category 3')
    room_inv_cat4            = selected_room.LookupParameter('Room Inventory Category 4')
    # SET ROOM INVENTORY NUMBER
    room_inv_cat1.Set('ARCHITECTURAL WORK')
    room_inv_cat2.Set('CABINETRY/BUILT-IN FURNITURE')
    room_inv_cat3.Set('SANITARY FITMENT')
    room_inv_cat4.Set('WALL PROTECTION')
    # ------------------------------------------------XXXX-----------------------------------------------------
    # ✅ ARCHITECTURAL WORK
    bi_archi_item = []
    bi_archi_desc = []
    bi_archi_name = []
    bi_archi_qty = []

    for i in bi_archi:
        if i:
            model_element_id = i.GetTypeId()
            model_type = doc.GetElement(model_element_id)
            archi_item_param = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
            archi_desc_param = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
            archi_obj_name = i.Name
            bi_archi_name.append(archi_obj_name)


            if archi_item_param is not None:
                archi_item = archi_item_param.AsValueString()
                bi_archi_item.append(archi_item)

            if archi_desc_param is not None:
                archi_desc = archi_desc_param.AsValueString()
                bi_archi_desc.append(archi_desc)

    # generate quantity of items
    cat1_counter = Counter(bi_archi_name)
    unique_archi_obj_name = set(bi_archi_name)
    for item in unique_archi_obj_name:
        bi_archi_qty.append(cat1_counter[item])

    split_bi_archi_qty = [str(item) for item in bi_archi_qty]

    # convert to set to get the unique items
    unique_bi_archi_item = set(bi_archi_item)
    unique_bi_archi_desc = set(bi_archi_desc)
    # convert to string
    bi_archi_item_str    = '\n'.join(unique_bi_archi_item)
    bi_archi_desc_str    = '\n'.join(unique_bi_archi_desc)
    bi_archi_qty_str     = '\n'.join(split_bi_archi_qty)
    # set
    room_inv_cat_item1 = selected_room.LookupParameter('Room Inventory Category 1 Items')
    room_inv_cat_item_desc1 = selected_room.LookupParameter('Room Inventory Category 1 Item Description')
    room_inv_cat_item_qty1   = selected_room.LookupParameter('Room Inventory Category 1 Item Quantities')

    if room_inv_cat_item1 is not None:
        room_inv_cat_item1.Set(bi_archi_item_str)

    if room_inv_cat_item_desc1 is not None:
        room_inv_cat_item_desc1.Set(bi_archi_desc_str)

    if room_inv_cat_item_qty1 and bi_archi_qty is not None:
        room_inv_cat_item_qty1.Set(bi_archi_qty_str)
    # ------------------------------------------------XXXX-----------------------------------------------------
    # ✅ CABINETRY/BUILT-IN FURNITURE
    bi_cab_furn_item    = []
    bi_cab_furn_desc    = []
    bi_cab_furn_name    = []
    bi_cab_furn_qty     = []

    for i in bi_cab_furn:
        if i:
            model_element_id        = i.GetTypeId()
            model_type              = doc.GetElement(model_element_id)
            cab_furn_item_param     = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
            cab_furn_desc_param     = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
            cab_furn_obj_name       = i.Name
            bi_cab_furn_name.append(cab_furn_obj_name)

            if cab_furn_item_param is not None:
                cab_furn_item = cab_furn_item_param.AsValueString()
                bi_cab_furn_item.append(cab_furn_item)

            if cab_furn_desc_param is not None:
                cab_furn_desc = cab_furn_desc_param.AsValueString()
                bi_cab_furn_desc.append(cab_furn_desc)

    # generate quantity of items
    cat2_counter = Counter(bi_cab_furn_name)
    unique_cab_furn_obj_name = set(bi_cab_furn_name)
    for item in unique_cab_furn_obj_name:
        bi_cab_furn_qty.append(cat2_counter[item])

    split_bi_cab_furn_qty = [str(item) for item in bi_cab_furn_qty]

    # convert to set to get the unique items
    unique_bi_cab_furn_item = set(bi_cab_furn_item)
    unique_bi_cab_furn_desc = set(bi_cab_furn_desc)
    # convert to string
    bi_cab_furn_item_str = '\n'.join(unique_bi_cab_furn_item)
    bi_cab_furn_desc_str = '\n'.join(unique_bi_cab_furn_desc)
    bi_cab_furn_qty_str = '\n'.join(split_bi_cab_furn_qty)

    # set
    room_inv_cat_item2 = selected_room.LookupParameter('Room Inventory Category 2 Items')
    room_inv_cat_item_desc2 = selected_room.LookupParameter('Room Inventory Category 2 Item Description')
    room_inv_cat_item_qty2 = selected_room.LookupParameter('Room Inventory Category 2 Item Quantities')

    if room_inv_cat_item2 is not None:
        room_inv_cat_item2.Set(bi_cab_furn_item_str)

    if room_inv_cat_item_desc2 is not None:
        room_inv_cat_item_desc2.Set(bi_cab_furn_desc_str)

    if room_inv_cat_item_qty2 and bi_cab_furn_qty is not None:
        room_inv_cat_item_qty2.Set(bi_cab_furn_qty_str)
    # ------------------------------------------------XXXX-----------------------------------------------------
    # ✅ SANITARY FITMENT
    bi_san_fit_item = []
    bi_san_fit_desc = []
    bi_san_fit_name = []
    bi_san_fit_qty = []

    for i in bi_san_fit:
        if i:
            model_element_id = i.GetTypeId()
            model_type = doc.GetElement(model_element_id)
            san_fit_item_param = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
            san_fit_desc_param = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
            san_fit_obj_name = i.Name
            bi_san_fit_name.append(san_fit_obj_name)

            if san_fit_item_param is not None:
                san_fit_item = san_fit_item_param.AsValueString()
                bi_san_fit_item.append(san_fit_item)

            if san_fit_desc_param is not None:
                san_fit_desc = san_fit_desc_param.AsValueString()
                bi_san_fit_desc.append(san_fit_desc)

    # generate quantity of items
    cat3_counter = Counter(bi_san_fit_name)
    unique_san_fit_obj_name = set(bi_san_fit_name)
    for item in unique_san_fit_obj_name:
        bi_san_fit_qty.append(cat3_counter[item])

    split_bi_san_fit_qty = [str(item) for item in bi_san_fit_qty]

    # convert to set to get the unique items
    filtered_san_fit_item = [item for item in bi_san_fit_item if item is not None]
    unique_bi_san_fit_item = set(filtered_san_fit_item)
    unique_bi_san_fit_desc = set(bi_san_fit_desc)
    # convert to string
    bi_san_fit_item_str = '\n'.join(unique_bi_san_fit_item)
    bi_san_fit_desc_str = '\n'.join(unique_bi_san_fit_desc)
    bi_san_fit_qty_str = '\n'.join(split_bi_san_fit_qty)
    # set
    room_inv_cat_item3 = selected_room.LookupParameter('Room Inventory Category 3 Items')
    room_inv_cat_item_desc3 = selected_room.LookupParameter('Room Inventory Category 3 Item Description')
    room_inv_cat_item_qty3 = selected_room.LookupParameter('Room Inventory Category 3 Item Quantities')

    if room_inv_cat_item3 is not None:
        room_inv_cat_item3.Set(bi_san_fit_item_str)

    if room_inv_cat_item_desc3 is not None:
        room_inv_cat_item_desc3.Set(bi_san_fit_desc_str)

    if room_inv_cat_item_qty3 and bi_san_fit_qty is not None:
        room_inv_cat_item_qty3.Set(bi_san_fit_qty_str)

    # ------------------------------------------------XXXX-----------------------------------------------------
    # ✅ WALL PROTECTION
    bi_wall_prot_item = []
    bi_wall_prot_desc = []
    bi_wall_prot_name = []
    bi_wall_prot_qty = []

    for i in bi_wall_prot:
        if i:
            model_element_id = i.GetTypeId()
            model_type = doc.GetElement(model_element_id)
            wall_prot_item_param = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
            wall_prot_desc_param = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
            wall_prot_obj_name = i.Name
            bi_wall_prot_name.append(wall_prot_obj_name)

            if wall_prot_item_param is not None:
                wall_prot_item = wall_prot_item_param.AsValueString()
                bi_wall_prot_item.append(wall_prot_item)

            if wall_prot_desc_param is not None:
                wall_prot_desc = wall_prot_desc_param.AsValueString()
                bi_wall_prot_desc.append(wall_prot_desc)

    # generate quantity of items
    cat4_counter = Counter(bi_wall_prot_name)
    unique_wall_prot_obj_name = set(bi_wall_prot_name)
    for item in unique_wall_prot_obj_name:
        bi_wall_prot_qty.append(cat4_counter[item])

    split_bi_wall_prot_qty = [str(item) for item in bi_wall_prot_qty]

    # convert to set to get the unique items
    unique_bi_wall_prot_item = set(bi_wall_prot_item)
    unique_bi_wall_prot_desc = set(bi_wall_prot_desc)
    # convert to string
    bi_wall_prot_item_str = '\n'.join(unique_bi_wall_prot_item)
    bi_wall_prot_desc_str = '\n'.join(unique_bi_wall_prot_desc)
    bi_wall_prot_qty_str = '\n'.join(split_bi_wall_prot_qty)
    # set
    room_inv_cat_item4 = selected_room.LookupParameter('Room Inventory Category 4 Items')
    room_inv_cat_item_desc4 = selected_room.LookupParameter('Room Inventory Category 4 Item Description')
    room_inv_cat_item_qty4 = selected_room.LookupParameter('Room Inventory Category 4 Item Quantities')

    if room_inv_cat_item4 is not None:
        room_inv_cat_item4.Set(bi_wall_prot_item_str)

    if room_inv_cat_item_desc4 is not None:
        room_inv_cat_item_desc4.Set(bi_wall_prot_desc_str)

    if room_inv_cat_item_qty4 and bi_wall_prot_qty is not None:
        room_inv_cat_item_qty4.Set(bi_wall_prot_qty_str)

    t.Commit()
# =============================================================================================
current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')

forms.alert('Parameters updated!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)



