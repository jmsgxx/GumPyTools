# -*- coding: utf-8 -*-

__title__ = 'Selected Code-Desc'
__doc__ = """
This script will update selected doors only.
Not the whole model.
- Door Panel Code
- Door Operation Code
- Door Lock Function Code
- Door Construction Code
- Door Protection Pull or Wall Code
- Door Protection Pull or Wall Height Code
- Door Protection Push or Track Code
- Door Protection Push or Track Height Code

HOW TO:
1. Select the desired door and click the command
    or click the command directly and press 'ok'.
2. The door descriptions will be  updated according to its code.
3. Print statement will confirm that change had
 been done or operation has aborted.
__________________________________
v2. 19 Dec 2023
v1: 18 Dec 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets.notion_com_logger import notion_com_logger
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from datetime import datetime
from Snippets._x_selection import ISelectionFilter_Categories, ISelectionFilter_Classes
import pyrevit
from pyrevit import forms, script
import sys

import re
import clr
import xlrd
clr.AddReference("System")





# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================

# directory = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\NDH_Door Data.xlsx'
directory = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\SKA-Tools.extension\lib\Ref\NDH_Door Data.xlsx'
wb = xlrd.open_workbook(directory)



def create_dict_xl(sheet_name):
    """
    create dictionary for code:description
    """
    data = {}
    # Open the workbook and select the worksheet by name
    sheet = wb.sheet_by_name(sheet_name)

    # index 0 = code, index 1 = description
    code_index = 0
    description_index = 1

    # Iterate through each row in the worksheet
    for j in range(sheet.nrows):
        code = sheet.cell_value(j, code_index)
        if isinstance(code, float) and code.is_integer():
            code = int(code)
        description = sheet.cell_value(j, description_index)
        data[code] = description

    return data


def get_list(param_code):
    """
    create a list based on parameters
    """
    param_code_list = []
    for index, item in enumerate(all_doors):
        if item:
            params = item.LookupParameter(param_code)
            if params:
                param_code_list.append((index, params.AsValueString()))
    return param_code_list


def set_by_index(filtered_list, lookup_desc, param_dict):
    for index, value in filtered_list:
        if value is not None:
            try:
                value = float(value)
            except ValueError:
                # If value is not a number, strip white spaces
                value = value.strip()
            door_desc = all_doors[index].LookupParameter(lookup_desc)
            if door_desc is not None:
                if value in (key.strip() if isinstance(key, str) else key for key in param_dict):
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
selection       = uidoc.Selection     # type: Selection

# ✅ ----------------XXX dictionary XXX------------
door_panel_dict                = create_dict_xl('WORK_DR_KEY_PANEL')
door_operation_dict            = create_dict_xl('WORK_DR_KEY_OPER')
door_lock_dict                 = create_dict_xl('WORK_DR_KEY_LOCKFCN')
door_construction_dict         = create_dict_xl('WORK_DR_KEY_CONST')
door_prot_pull_dict            = create_dict_xl('WORK_DR_KEY_PROTPULL')
door_prot_pullht_dict          = create_dict_xl('WORK_DR_KEY_PROTPULLHT')
door_prot_push_dict            = create_dict_xl('WORK_DR_KEY_PROTPUSH')
door_prot_pushht_dict          = create_dict_xl('WORK_DR_KEY_PROTPUSHHT')
door_feature_dict              = create_dict_xl('WORK_DR_KEY_FEATURE')


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # ✅ GET ALL DOOR TYPES
    all_phase = list(doc.Phases)
    phase = (all_phase[1])
    try:
        all_door_ins = [doc.GetElement(el_id) for el_id in selection.GetElementIds()]   # family instance
        all_doors = [door.Symbol for door in all_door_ins]  # family symbol

        if not all_doors:
            filter_clas = ISelectionFilter_Classes([FamilyInstance])
            door_list = selection.PickObjects(ObjectType.Element, filter_clas)
            all_doors_list = [doc.GetElement(el) for el in door_list]
            all_doors = [door.Symbol for door in all_doors_list]
            if not all_doors:
                forms.alert("Select Doors.\nTry again.", exitscript=True)
    except Exception as e:
        forms.alert(str(e), exitscript=True)



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
    set_by_index(door_prot_pl_wl_lst,       'Door Protection Pull or Wall', door_prot_pull_dict)
    set_by_index(door_prot_pl_wl_htx_lst,   'Door Protection Pull or Wall Height Text', door_prot_pullht_dict)
    set_by_index(door_prot_ps_tr_lst,       'Door Protection Push or Track', door_prot_push_dict)
    set_by_index(door_prot_ps_tr_htx_lst,   'Door Protection Push or Track Height Text', door_prot_pushht_dict)

    # 🔷 this is a special section for "DOOR FEATURE CODE"
    """
    'Door Feature Code' consists of a combination of single item string and a combination of strings separated by comma (,)
    take note. Python will not treat it as a list so you need to split it and put in new list. Get their index. Be mindful
    of NoneType.
    """
    door_feat_lst = []
    for doors in all_doors:
        if doors:
            dr_code = doors.LookupParameter('Door Feature Code')
            if dr_code:
                door_feat_lst.append(dr_code.AsValueString())

    split_list = []
    for index, value in enumerate(door_feat_lst):
        if value is not None:
            split_values = value.split(', ')
            for split_value in split_values:
                split_list.append((index, split_value))


    def change_value(door_feat, door_dict):
        errors = []  # List to store error messages
        for item in re.split('[,.]', door_feat):
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
            if value == '-' or value == '--':
                new_value = ''
            else:
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

    t.Commit()
#     ==================================================================================
current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%M hrs')

forms.alert('Door Parameters updated!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)

# notion_com_logger(__title__)