# -*- coding: utf-8 -*-

__title__ = 'Test Button'
__doc__ = """
testing button for anything.
__________________________________
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms

import os
import csv
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================


def create_dict(directory):
    data = {}
    with open(directory, 'r') as f:
        param_dict = csv.DictReader(f)
        for row in param_dict:
            code = row['code']
            description = row['description']
            data[code] = description
    return data


# def get_list(param_code):
#     param_code_list = []
#     for index, item in enumerate(all_doors):
#         if item is not None:
#             param = item.LookupParameter(param_code)
#             if param is not None:
#                 param_code_list.append((index, param.AsValueString()))
#     return param_code_list


# def set_by_index(filtered_list, lookup_desc, param_dict):
#     for index, value in filtered_list:
#         door_desc = all_doors[index].LookupParameter(lookup_desc)
#         if door_desc is not None and value in param_dict:
#             door_desc.Set(param_dict[value])
            # for k, v in param_dict.items():
                # if value == k:
                #     continue
                # else:
                #     print("Iterator '{}' is not equal with '{}'".format(value, param_dict[k]))



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

# ✅-----------------XXX csv XXX-----------------
door_feature_path             = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Feature.csv')

# ✅ ----------------XXX dictionary XXX------------
door_feature_dict             = create_dict(door_feature_path)

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # ✅ GET ALL DOOR TYPES
    all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()


    def get_list(param_code):
        param_code_list = []
        for index, item in enumerate(all_doors):
            try:
                if item is not None:
                    param = item.LookupParameter(param_code)
                    if param is not None:
                        param_code_list.append((index, param.AsValueString()))
            except Exception as e:
                print("Error in get_list at index %s: %s" % (index, e))
        return param_code_list


    def flatten_with_index(lst):
        flat_list = []
        for i, element in enumerate(lst):
            try:
                if isinstance(element, list):  # if element is a sublist
                    for index, item in element:
                        if item is not None and item.strip():  # ignore whitespace and None
                            flat_list.append((index, item))  # append the index and item to flat_list
                elif element:  # if element is a single item
                    if element[1] is not None and element[1].strip():  # ignore whitespace and None
                        flat_list.append((i, element[1]))  # append the index and second item of the tuple to flat_list
            except Exception as e:
                print("Error in flatten_with_index at index %s: %s" % (i, e))
        return flat_list


    def set_values(original_list, flat_list, param_dict):
        for index, value in flat_list:
            try:
                codes = value.split(',')  # split the codes
                for code in codes:  # handle each code individually
                    code = code.strip()  # remove leading and trailing spaces
                    if code in param_dict:
                        door_desc = all_doors[index].LookupParameter('Door Feature')
                        if door_desc is not None:
                            if door_desc.IsReadOnly:
                                print("Parameter is read-only at index %s" % index)
                            else:
                                try:
                                    door_desc.Set(param_dict[code])
                                except Exception as e:
                                    print("Error setting parameter at index %s: %s" % (index, e))
                        else:
                            print("Parameter not found at index %s" % index)
                    else:
                        print("Value not found in dictionary: %s" % code)
            except Exception as e:
                print("Error in set_values at index %s: %s" % (index, e))
        return original_list


    # Get the list of doors
    door_feature_lst = get_list('Door Feature Code')

    # Flatten the list and set the values
    flat_feature_list = flatten_with_index(door_feature_lst)
    set_values(door_feature_lst, flat_feature_list, door_feature_dict)

    # door_op = []
    # for i, door in enumerate(all_doors):
    #     if door is not None:
    #         param = door.LookupParameter('Door Operation Code')
    #         if param is not None:
    #             door_op.append((i, param.AsValueString()))



    # 🟢 CALL THE SET_BY_INDEX FUNCTION
    # set_by_index(door_panel_lst, 'Door Panel', door_panel_dict)


    # for i, dr in door_prot_pl_wl_lst:
    #     door = all_doors[i].LookupParameter('Door Protection Pull or Wall')
    #     if door is not None and dr in door_protection_dict:
    #         door.Set(door_protection_dict[dr])
            # for k, v in door_panel_dict.items():
            #     if dr == k:
            #         print("Dr {} is the same as Dict Key {}".format(dr, door_panel_dict[k]))

    t.Commit()