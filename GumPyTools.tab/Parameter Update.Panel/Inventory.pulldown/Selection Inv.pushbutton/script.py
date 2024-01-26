# -*- coding: utf-8 -*-

__title__ = 'Selection Inv'
__doc__ = """
This script will select only specific
elements to be assigned on a specific
room.
NOTE:
This script automatically detect which filtered
elements are inside the room.

REASON:
There are multiple rooms in a single
active view.

HOW TO:
1. Select a room or group of rooms.
2. It will automatically assign the elements
 inside it's respective room.
--------------------------------------
v1: 15 Nov 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Snippets import _x_selection
from Snippets.element_collection import element_collection
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import clr
clr.AddReference("System")


# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================


doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection


filter_type = _x_selection.ISelectionFilter_Classes([Room])
selected_element = selection.PickObjects(ObjectType.Element, filter_type, "Select Room")

selected_rooms = [doc.GetElement(el) for el in selected_element]
if not selected_rooms:
    sys.exit()

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    output = script.get_output()
    output.center()
    output.resize(300, 600)
    output.print_md('### NUMBER OF SELECTED ITEMS   : {}'.format(len(selected_rooms)))

    for selected_room in selected_rooms:

        calculator = SpatialElementGeometryCalculator(doc)
        results = calculator.CalculateSpatialElementGeometry(selected_room)
        room_solid = results.GetGeometry()  # imaginary solid created via room

        collector = FilteredElementCollector(doc, active_view.Id).WherePasses(
            ElementIntersectsSolidFilter(room_solid)).ToElements()

        # 🟠 ROOM PARAMETERS
        sel_room_name = selected_room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
        sel_room_number = selected_room.Number
        # loose param
        room_user_cat = selected_room.LookupParameter('Room Inventory By User Category')
        room_user_item = selected_room.LookupParameter('Room Inventory By User Items')
        room_user_desc = selected_room.LookupParameter('Room Inventory By User Item Description')
        room_user_qty = selected_room.LookupParameter('Room Inventory By User Item Quantities')

        elements = []   # elements with category

        for element in collector:
            if element.Category and element.Category.Name:
                elements.append(element)

        by_user_lst = []  # family instance '(BY USER)'
        built_in_lst = []

        for element in elements:
            el_type_id = element.GetTypeId()
            el_symbol = doc.GetElement(el_type_id)
            if el_symbol is not None:
                # parameter
                manufacturer_val = el_symbol.get_Parameter(BuiltInParameter.ALL_MODEL_MANUFACTURER)
                filters = active_view.GetFilters()

                is_filtered_by_user = False

                for filter_id in filters:
                    filter_element = doc.GetElement(filter_id)  # type: ParameterFilterElement

                    # Get the filter from the ParameterFilterElement
                    el_filter = filter_element.GetElementFilter()  # type 'LogicalAndFilter' / 'LogicalOrFilter'

                    # Check if the element satisfies the filter
                    if el_filter and el_filter.PassesFilter(element):
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
                if not filters or not is_filtered_by_user:
                    # returns true if objects has no filter and not under '(BY USER)'
                    if isinstance(category, Category) and category.Id.IntegerValue in categories:
                        built_in_lst.append(element)
                    # print("Element {} is affected by filter {}".format(element.Id.IntegerValue, filter_element.Name))

        # ╦  ╔═╗╔═╗╔═╗╔═╗
        # ║  ║ ║║ ║╚═╗║╣
        # ╩═╝╚═╝╚═╝╚═╝╚═╝ loose furniture
        # =====================================================================================================================

        by_user_cat = []
        by_user_item = []
        by_user_desc = []
        by_user_qty = []
        by_user_obj_name = []

        for item in by_user_lst:
            if item:
                # 🟢 GET PARAMS OF LOOSE FURNITURE
                model_element_id = item.GetTypeId()
                model_type = doc.GetElement(model_element_id)
                """ this is the parameter to get that will set in room """
                model_type_cat_param = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsValueString()  # type comments
                if model_type_cat_param is None:
                    print("Element {} has no description for 'Loose Items' in {} - {}.".format(item.Id,
                                                                                               sel_room_name,
                                                                                               sel_room_number))
                model_type_item_param = model_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID).AsValueString()  # type mark
                model_type_desc_param = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION).AsValueString()  # type description

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
        filtered_by_user_cat = [item for item in by_user_cat if item is not None]
        unique_by_user_cat = set(filtered_by_user_cat)
        filtered_by_user_item = [item for item in by_user_item if item is not None]
        unique_by_user_item = set(filtered_by_user_item)
        unique_by_user_desc = set(by_user_desc)

        #  convert to string
        by_user_cat_str = '\n'.join(unique_by_user_cat)
        by_user_item_str = '\n'.join(unique_by_user_item)
        by_user_desc_str = '\n'.join(unique_by_user_desc)
        by_user_qty_str = '\n'.join(split_by_user_qty)

        # 🟥 SET TO ROOM PARAMETER
        # ======================================
        if selected_room:
            if room_user_cat:
                room_user_cat.Set(by_user_cat_str)
            if room_user_item:
                room_user_item.Set(by_user_item_str)
            if by_user_desc_str and room_user_desc:
                room_user_desc.Set(by_user_desc_str)
            if by_user_qty_str and room_user_qty:
                room_user_qty.Set(by_user_qty_str)

        # ╔╗ ╦ ╦╦╦ ╔╦╗  ╦╔╗╔
        # ╠╩╗║ ║║║  ║───║║║║
        # ╚═╝╚═╝╩╩═╝╩   ╩╝╚╝ built-in objects
        # ==========================================================================================================

        bi_archi = []
        bi_cab_furn = []
        bi_san_fit = []
        bi_wall_prot = []

        for item in built_in_lst:
            model_element_id = item.GetTypeId()
            model_type = doc.GetElement(model_element_id)
            # ⭕
            built_in_cat = model_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsValueString()
            if built_in_cat is None:
                print("Element {} has no description for 'Built-in Items' in {} - {}.".format(item.Id,
                                                                                              sel_room_name,
                                                                                              sel_room_number))
            elif built_in_cat == 'ARCHITECTURAL WORK':
                bi_archi.append(item)
            elif built_in_cat == 'SANITARY FITMENT':
                bi_san_fit.append(item)
            elif built_in_cat == 'WALL PROTECTION':
                bi_wall_prot.append(item)
            elif built_in_cat == 'CABINETRY/BUILT-IN FURNITURE' or built_in_cat == 'CABINETRY / BUILT-IN FURNITURE':
                bi_cab_furn.append(item)


        # built-in param
        room_inv_cat1 = selected_room.LookupParameter('Room Inventory Category 1')
        room_inv_cat2 = selected_room.LookupParameter('Room Inventory Category 2')
        room_inv_cat3 = selected_room.LookupParameter('Room Inventory Category 3')
        room_inv_cat4 = selected_room.LookupParameter('Room Inventory Category 4')
        # SET ROOM INVENTORY NUMBER
        room_inv_cat1.Set('ARCHITECTURAL WORK')
        room_inv_cat2.Set('CABINETRY/BUILT-IN FURNITURE')
        room_inv_cat3.Set('SANITARY FITMENT')
        room_inv_cat4.Set('WALL PROTECTION')
        # ------------------------------------------------XXXX-----------------------------------------------------
        # 🟢 MAIN EXECUTION OF BUILT-IN
        all_elements = [bi_archi, bi_cab_furn, bi_san_fit, bi_wall_prot]

        for index, item in enumerate(all_elements, start=1):
            element_collection(item, index, selected_room)

        # ---------------------------------------------xxx----------------------------------------------------
        room_name = selected_room.LookupParameter('Name')

        print('=' * 50)
        print('ROOM NAME : {}'.format(room_name.AsValueString().upper()))
        print('ROOM NUMBER : {}'.format(selected_room.Number))
        print("Total Built-In Furniture: {}".format(len(built_in_lst)))
        print("Total Loose Furniture: {}".format(len(by_user_lst)))
        print('=' * 50)

    t.Commit()
