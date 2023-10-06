# -*- coding: utf-8 -*-

__title__ = 'Door Code-Description'
__doc__ = """
This script will add description
on door parameters based on the code.
Info will be fetched from CSV file
that came from KOP.
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


def match_set_descr(list_code, dict_code, set_desc_param):
    if list_code in dict_code:
        value = dict_code[list_code]
        set_desc_param.Set(value)




# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel

# ✅-----------------XXX csv XXX-----------------
door_panel_path             = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Panel.csv')
door_operation_path         = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Operation.csv')
door_lock_path              = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Lock Function.csv')
door_feature_path           = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Feature.csv')
door_construction_path      = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Construction.csv')
door_protection_path        = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Protection.csv')
door_protection_ht_path     = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Protection Height.csv')

# ✅ ----------------XXX dictionary XXX------------
door_panel_dict             = create_dict(door_panel_path)
door_operation_dict         = create_dict(door_operation_path)
door_lock_dict              = create_dict(door_lock_path)
door_feature_dict           = create_dict(door_feature_path)
door_construction_dict      = create_dict(door_construction_path)
door_protection_dict        = create_dict(door_protection_path)
door_protection_ht_dict     = create_dict(door_protection_ht_path)


# ✅ GET ALL DOOR TYPES
all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors)\
            .WhereElementIsElementType().ToElements()




# ========================================================================================================
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ main
# =========================================================================================================

"""
perform the operation to get the proper description based on the given the code and iterate from the dictionary
that came from the csv file
"""
with Transaction(doc, __title__) as t:
    t.Start()

    lst_door_feature_code = []

    for door in all_doors:
        # 🟢 GET THE SHARED PARAMETER FROM THE MODEL
        door_panel_desc             = door.LookupParameter('Door Panel')
        door_operation_desc         = door.LookupParameter('Door Operation')
        door_lock_desc              = door.LookupParameter('Door Lock Function')
        door_feature_desc           = door.LookupParameter('Door Feature')
        door_construction_desc      = door.LookupParameter('Door Construction')
        door_prot_pl_wl_desc        = door.LookupParameter('Door Protection Pull or Wall')
        door_prot_pl_wl_htx_desc    = door.LookupParameter('Door Protection Pull or Wall Height Text')
        door_prot_ps_tr_desc        = door.LookupParameter('Door Protection Push or Track')
        door_prot_ps_tr_htx_desc    = door.LookupParameter('Door Protection Push or Track Height Text')

        # 🔴 GET THE 'CODE' PARAMETER
        sp_dr_panel_code            = door.LookupParameter('Door Panel Code').AsValueString()
        sp_dr_operation_code        = door.LookupParameter('Door Operation Code').AsValueString()
        sp_dr_lock_code             = door.LookupParameter('Door Lock Function Code').AsValueString()
        sp_dr_construction_code     = door.LookupParameter('Door Construction Code').AsValueString()
        sp_dr_prot_pl_wl_code       = door.LookupParameter('Door Protection Pull or Wall Code').AsValueString()
        sp_dr_prot_pl_wl_htx_code   = door.LookupParameter('Door Protection Pull or Wall Height Code').AsValueString()
        sp_dr_prot_ps_tr_code       = door.LookupParameter('Door Protection Push or Track Code').AsValueString()
        sp_dr_prot_ps_tr_htx_code   = door.LookupParameter('Door Protection Push or Track Height Code').AsValueString()

        # 🔵 SET THE CORRESPONDING VALUE TO DESC
        # match_set_descr(sp_dr_panel_code, door_panel_dict, door_panel_desc)
        # match_set_descr(sp_dr_operation_code, door_operation_dict, door_operation_desc)
        # match_set_descr(sp_dr_lock_code, door_lock_dict, door_lock_desc)
        # match_set_descr(sp_dr_construction_code, door_construction_dict, door_construction_desc)
        # match_set_descr(sp_dr_prot_pl_wl_code, door_protection_dict, door_prot_pl_wl_desc)
        # match_set_descr(sp_dr_prot_pl_wl_htx_code, door_protection_ht_dict, door_prot_pl_wl_htx_desc)
        # match_set_descr(sp_dr_prot_ps_tr_code, door_protection_dict, door_prot_ps_tr_desc)
        # match_set_descr(sp_dr_prot_ps_tr_htx_code, door_protection_ht_dict, door_prot_ps_tr_htx_desc)

        sp_dr_feature_code = door.LookupParameter('Door Feature Code').AsValueString()

        if isinstance(sp_dr_feature_code, list):
            codes = [code.strip() for code in sp_dr_feature_code if code is not None]
        else:
            codes = [code.strip() for code in (sp_dr_feature_code.split(",") if sp_dr_feature_code else []) if
                     code is not None]
        lst_door_feature_code.extend(codes)

        for item in lst_door_feature_code:
            if item in door_feature_dict:
                # print("Key '{}' matched in dictionary.".format(item))
                value = door_feature_dict[item]
                # print("Retrieved value: {}".format(value))
                door_feature_desc.Set(value)
            else:
                print("Key '{}' not found in dictionary.".format(item))
    t.Commit()
