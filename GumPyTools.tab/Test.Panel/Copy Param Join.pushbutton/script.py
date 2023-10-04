# -*- coding: utf-8 -*-

__title__ = 'Copy Param Join'
__doc__ = """
This script will add description
on door parameters based on the code.
Info will be fetched from excel file
that came from KOP
__________________________________
v1: 03 Oct 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *

import os
import csv
import clr

clr.AddReference("System")


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# =====================================================================================================
def create_dict(directory):
    data = {}
    with open(directory, 'r') as f:
        param_dict = csv.DictReader(f)
        for row in param_dict:
            code = row['code']
            description = row['description']
            data[code] = description
    return data


def get_desc_fr_dict(sp_model, dict_csv):
    # probably should create a list and append
    for sp_value in sp_model:
        if sp_value:
            for k, v in dict_csv.items():
                if k == sp_value:
                    description = v
                    return description
        else:
            return None


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel

# ✅-----------------XXX csv XXX-----------------
door_panel_path         = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Panel.csv')
door_operation_path     = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Operation.csv')
door_lock_path          = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Lock Function.csv')
door_feature_path       = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Feature.csv')
door_construction_path  = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Construction.csv')

# ✅ ----------------XXX dictionary XXX------------
door_panel_dict         = create_dict(door_panel_path)
door_operation_dict     = create_dict(door_operation_path)
door_lock_dict          = create_dict(door_lock_path)
door_feature_dict       = create_dict(door_feature_path)
door_construction_dict  = create_dict(door_construction_path)


# ✅get all door types
all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors)\
            .WhereElementIsElementType().ToElements()

# ✅get door shared parameters
sp_door_panel_code          = [door.LookupParameter('Door Panel Code').AsValueString() for door in all_doors]
sp_door_operation_code      = [door.LookupParameter('Door Operation Code').AsValueString() for door in all_doors]
sp_door_lock_code           = [door.LookupParameter('Door Lock Function Code').AsValueString() for door in all_doors]
sp_door_feature_code        = [door.LookupParameter('Door Feature Code').AsValueString() for door in all_doors]
sp_door_construction_code   = [door.LookupParameter('Door Construction Code').AsValueString() for door in all_doors]


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================

"""
perform the operation to get the proper description based on the given the code and iterate from the dictionary
that came from the csv file
"""
door_panel          = (get_desc_fr_dict(str(sp_door_panel_code), door_panel_dict))
door_operation      = (get_desc_fr_dict(str(sp_door_operation_code), door_operation_dict))
door_lock           = (get_desc_fr_dict(str(sp_door_lock_code), door_lock_dict))
door_feature        = (get_desc_fr_dict(str(sp_door_feature_code), door_feature_dict))
door_construction   = (get_desc_fr_dict(str(sp_door_construction_code), door_construction_dict))

with Transaction(doc, __title__) as t:
    t.Start()

    for door in all_doors:
        # 🟢 GET THE SHARED PARAMETER FROM THE MODEL
        door_panel_desc         = door.LookupParameter('Door Panel')
        door_operation_desc     = door.LookupParameter('Door Operation')
        door_lock_desc          = door.LookupParameter('Door Lock Function')
        door_feature_desc       = door.LookupParameter('Door Feature')
        door_construction_desc  = door.LookupParameter('Door Construction')

        # 🟢 SET THE VALUES TO SHARED PARAMETER
        # if door_construction_desc:
        #     door_panel_desc.Set(door_panel)
        if door_operation_desc:
            # door_operation_desc.Set(door_operation)
            for dop in sp_door_operation_code:
                if dop != "":
                    for keys, values in door_operation_dict.items():
                        if keys == dop:
                            door_op_description = values
                            door_operation_desc.Set(door_op_description)

        # if door_lock_desc:
        #     door_lock_desc.Set(door_lock)
        # if door_feature_desc:
        #     door_feature_desc.Set(door_feature)
        # if door_construction_desc:
        #     door_construction_desc.Set(door_construction)

    t.Commit()
