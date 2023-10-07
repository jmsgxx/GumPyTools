# -*- coding: utf-8 -*-

__title__ = 'Door Code-Description'
__doc__ = """
This script will add description
on door parameters based on the code.
Info will be fetched from CSV file
that came from KOP.
__________________________________
NOTE: 'Door Feature' is not included
as the structure of the list contains
single item, list, None, '-' and
Keyerror that isn't on the schedule.
Dynamo will be used for better
filtering.

v1: 03 Oct 2023
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


def get_list(param_code):
    param_code_list = []
    for index, item in enumerate(all_doors):
        if item is not None:
            param = item.LookupParameter(param_code)
            if param is not None:
                param_code_list.append((index, param.AsValueString()))
    return param_code_list


def set_by_index(filtered_list, lookup_desc, param_dict):
    for index, value in filtered_list:
        door_desc = all_doors[index].LookupParameter(lookup_desc)
        if door_desc is not None and value in param_dict:
            door_desc.Set(param_dict[value])
            if value not in param_dict:
                print("In {}, iterator '{}' does not match with any Dict Key".format(door_desc, value))



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
door_panel_path             = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Panel.csv')
door_operation_path         = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Operation.csv')
door_lock_path              = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Lock Function.csv')
door_construction_path      = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Construction.csv')
door_protection_path        = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Protection.csv')
door_protection_ht_path     = os.path.abspath(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\Door Protection Height.csv')

# ✅ ----------------XXX dictionary XXX------------
door_panel_dict             = create_dict(door_panel_path)
door_operation_dict         = create_dict(door_operation_path)
door_lock_dict              = create_dict(door_lock_path)
door_construction_dict      = create_dict(door_construction_path)
door_protection_dict        = create_dict(door_protection_path)
door_protection_ht_dict     = create_dict(door_protection_ht_path)


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # ✅ GET ALL DOOR TYPES
    all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors) \
        .WhereElementIsElementType().ToElements()

    # 🟢 CALL THE get_list() TO GET THE LIST OF OBJECT FROM all_doors
    door_panel_lst = get_list('Door Panel Code')
    door_op_lst = get_list('Door Operation Code')
    door_lock_lst = get_list('Door Lock Function Code')
    door_cons_lst = get_list('Door Construction Code')
    door_prot_pl_wl_lst = get_list('Door Protection Pull or Wall Code')
    door_prot_pl_wl_htx_lst = get_list('Door Protection Pull or Wall Height Code')
    door_prot_ps_tr_lst = get_list('Door Protection Push or Track Code')
    door_prot_ps_tr_htx_lst = get_list('Door Protection Push or Track Height Code')

    # 🟢 CALL THE set_by_index()
    set_by_index(door_panel_lst, 'Door Panel', door_panel_dict)
    set_by_index(door_op_lst, 'Door Operation', door_operation_dict)
    set_by_index(door_lock_lst, 'Door Lock Function', door_lock_dict)
    set_by_index(door_cons_lst, 'Door Construction', door_construction_dict)
    set_by_index(door_prot_pl_wl_lst, 'Door Protection Pull or Wall', door_protection_dict)
    set_by_index(door_prot_pl_wl_htx_lst, 'Door Protection Pull or Wall Height Text', door_protection_ht_dict)
    set_by_index(door_prot_ps_tr_lst, 'Door Protection Push or Track', door_protection_dict)
    set_by_index(door_prot_ps_tr_htx_lst, 'Door Protection Push or Track Height Text', door_protection_ht_dict)


    t.Commit()
