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
    all_doors = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()

    door_feat_lst = []
    for doors in all_doors:
        dr_code = doors.LookupParameter('Door Feature Code').AsValueString()
        door_feat_lst.append(dr_code)

    split_list = []
    for index, value in enumerate(door_feat_lst):
        if value is not None:
            split_values = value.split(', ')
            for split_value in split_values:
                split_list.append((index, split_value))


    def change_value(door_feat_list, door_dict):
        for item in door_feat_list.split(','):
            item = item.strip()
            if item in door_dict:
                yield door_dict[item]
            else:
                yield item


    new_value_param = []
    for value in door_feat_lst:
        if value is not None:
            new_value = ', '.join(change_value(value, dict(door_feature_dict)))
        else:
            new_value = None  # keep None values
        new_value_param.append(new_value)

    for index, door in enumerate(all_doors):
        if door is not None:
            door_feature_desc = door.LookupParameter('Door Feature')
            if door_feature_desc is not None and new_value_param[index] is not None:
                door_feature_desc.Set(new_value_param[index])

    # for i, door in enumerate(all_doors):
    #     if i < len(new_value_param):
    #         door_feat_desc = door.LookupParameter('Door Feature')
    #         if new_value_param[i] is not None:
    #             if door_feat_desc is None:
    #                 continue

    t.Commit()