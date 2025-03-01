# -*- coding: utf-8 -*-

__title__ = 'Door Update'
__doc__ = """
This script will update:
- Door Panel Code
- Door Operation Code
- Door Lock Function Code
- Door Construction Code
- Door Protection Pull or Wall Code
- Door Protection Pull or Wall Height Code
- Door Protection Push or Track Code
- Door Protection Push or Track Height Code
- Door Mark
- Door Number
__________________________________
v3: 16 Oct 2023
v2: 08 Oct 2023
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
            params = item.LookupParameter(param_code)
            if params is not None:
                param_code_list.append((index, params.AsValueString()))
    return param_code_list


def set_by_index(filtered_list, lookup_desc, param_dict):
    param_error = []
    for index, value in filtered_list:
        if value is not None:
            door_desc = all_doors[index].LookupParameter(lookup_desc)
            if door_desc is not None and value in param_dict:
                door_desc.Set(param_dict[value])


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
door_panel_path             = os.path.abspath(r'/lib/Ref/Door Panel.csv')
door_operation_path         = os.path.abspath(r'/lib/Ref/Door Operation.csv')
door_lock_path              = os.path.abspath(r'/lib/Ref/Door Lock Function.csv')
door_construction_path      = os.path.abspath(r'/lib/Ref/Door Construction.csv')
door_protection_path        = os.path.abspath(r'/lib/Ref/Door Protection.csv')
door_protection_ht_path     = os.path.abspath(r'/lib/Ref/Door Protection Height.csv')
door_feature_path             = os.path.abspath(r'/lib/Ref/Door Feature.csv')

# ✅ ----------------XXX dictionary XXX------------
door_panel_dict             = create_dict(door_panel_path)
door_operation_dict         = create_dict(door_operation_path)
door_lock_dict              = create_dict(door_lock_path)
door_construction_dict      = create_dict(door_construction_path)
door_protection_dict        = create_dict(door_protection_path)
door_protection_ht_dict     = create_dict(door_protection_ht_path)
door_feature_dict             = create_dict(door_feature_path)


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # ✅ GET ALL DOOR TYPES

    all_phase = list(doc.Phases)
    phase = (all_phase[1])

    ins_all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

    all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors) \
        .WhereElementIsElementType().ToElements()

    # 🟢 CALL THE get_list() TO GET THE LIST OF OBJECT FROM all_doors
    door_panel_lst              = get_list('Door Panel Code')
    door_op_lst                 = get_list('Door Operation Code')
    door_lock_lst               = get_list('Door Lock Function Code')
    door_cons_lst               = get_list('Door Construction Code')
    door_prot_pl_wl_lst         = get_list('Door Protection Pull or Wall Code')
    door_prot_pl_wl_htx_lst     = get_list('Door Protection Pull or Wall Height Code')
    door_prot_ps_tr_lst         = get_list('Door Protection Push or Track Code')
    door_prot_ps_tr_htx_lst     = get_list('Door Protection Push or Track Height Code')

    # 🟢 CALL THE set_by_index()
    set_by_index(door_panel_lst,            'Door Panel', door_panel_dict)
    set_by_index(door_op_lst,               'Door Operation', door_operation_dict)
    set_by_index(door_lock_lst,             'Door Lock Function', door_lock_dict)
    set_by_index(door_cons_lst,             'Door Construction', door_construction_dict)
    set_by_index(door_prot_pl_wl_lst,       'Door Protection Pull or Wall', door_protection_dict)
    set_by_index(door_prot_pl_wl_htx_lst,   'Door Protection Pull or Wall Height Text', door_protection_ht_dict)
    set_by_index(door_prot_ps_tr_lst,       'Door Protection Push or Track', door_protection_dict)
    set_by_index(door_prot_ps_tr_htx_lst,   'Door Protection Push or Track Height Text', door_protection_ht_dict)

    # 🔷 this is a special section for "DOOR FEATURE CODE"
    """
    'Door Feature Code' consists of a combination of single item string and a combination of strings separated by comma (,)
    take note. Python will not treat it as a list so you need to split it and put in new list. Get their index. Be mindful
    of NoneType.
    """
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


    def change_value(door_feat, door_dict):
        errors = []  # List to store error messages
        for item in door_feat.split(','):
            item = item.strip()
            try:
                if item in door_dict:
                    yield door_dict[item]
                else:
                    raise KeyError("Door Feature Item '{}' not found in door_dict".format(item))
            except KeyError as e:
                errors.append(str(e))  # Store the error message

        # Print all errors at the end
        for error in errors:
            print(error)


    new_value_param = []
    for value in door_feat_lst:
        if value is not None:
            new_value = ', '.join(change_value(value, dict(door_feature_dict)))
        else:
            new_value = None
        new_value_param.append(new_value)

    # set the new value on all parameters after getting the value from the dictionary
    for index, door in enumerate(all_doors):
        if door is not None:
            door_feature_desc = door.LookupParameter('Door Feature')
            if door_feature_desc is not None and new_value_param[index] is not None:
                door_feature_desc.Set(new_value_param[index])

    # ╔═╗╔═╗╔╗╔╔═╗╔═╗╔╦╗
    # ║  ║ ║║║║║  ╠═╣ ║
    # ╚═╝╚═╝╝╚╝╚═╝╩ ╩ ╩ set the 'DOOR REMARKS' value with the concatenation of all changed
    # value
    # ================================================================================

    for dr_param in all_doors:
        if dr_param is None:
            continue
        else:
            parameters = [
                dr_param.LookupParameter('Door Operation'),
                dr_param.LookupParameter('Door Panel'),
                dr_param.LookupParameter('Door Lock Function'),
                dr_param.LookupParameter('Door Construction'),
                dr_param.LookupParameter('Door Protection Pull or Wall'),
                dr_param.LookupParameter('Door Protection Pull or Wall Height Text'),
                dr_param.LookupParameter('Door Protection Push or Track'),
                dr_param.LookupParameter('Door Protection Push or Track Height Text'),
                dr_param.LookupParameter('Door Feature')
            ]

            # out string parameters, excluding None values
            string_parameters = [param.AsValueString() for param in parameters if
                                 param is not None and param.AsValueString() is not None]

            # Concatenate the string parameters
            concat_string = ','.join(string_parameters)

            concat_door_remarks = dr_param.LookupParameter('Door Remarks')
            if concat_door_remarks is not None:
                concat_door_remarks.Set(concat_string)

    # 🟩 DOOR MARK AND NUMBERING
    # ===============================================================================-

    # 🟢 SET THE 'Door Number' AND 'Mark'
    # Group doors by room
    doors_by_room = {}
    for door in ins_all_doors:
        room = door.ToRoom[phase]
        if room:
            room_number = room.Number
            if room_number not in doors_by_room:
                doors_by_room[room_number] = []
            doors_by_room[room_number].append(door)

    # Generate a sequence for each group of doors and assign door numbers
    for room_number, doors in doors_by_room.items():
        for i, door in enumerate(doors):
            door_sequence = str(i + 1).zfill(2)
            door_mark = "{}-{}".format(room_number, door_sequence)
            door_number = "D{}".format(door_sequence)
            door.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set(door_mark)
            door.LookupParameter('Door Number').Set(door_number)

    t.Commit()

