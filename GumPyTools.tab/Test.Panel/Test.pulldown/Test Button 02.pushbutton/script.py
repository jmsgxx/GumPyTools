# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
__________________________________
Author: Joven Mark Gumana

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import csv
from Snippets._convert import convert_m_to_feet
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, StairsFilter
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType, ISelectionFilter
from FunctionFiles._selection import SelectElementBIGClass, FECollectorCat
from collections import Counter

import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection
# ======================================================================================================


def set_type(item, item_type):
    if hasattr(item, 'ChangeTypeId'):
        return item.ChangeTypeId(item_type.Id)



REPLACEMENT_TYPE_900 = None
REPLACEMENT_TYPE_1500 = None
ELEMENTS_TO_REPLACE = []

all_se = (FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpecialityEquipment)
          .WhereElementIsNotElementType().ToElements())

for se in all_se:
    type_id = se.GetTypeId()
    type_el = doc.GetElement(type_id)
    if type_el:
        family_name = type_el.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()
        if family_name == "SE_NHOST_INT_COR-GUARD_GENC_300":
            type_name = type_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            if type_name == "VL/900":
                REPLACEMENT_TYPE_900 = type_el
            elif type_name == "VL/1500":
                REPLACEMENT_TYPE_1500 = type_el

# ======================================================================================================

# specialty_equip_filter = SelectElementBIGClass(BuiltInCategory.OST_SpecialityEquipment)
#
# selected_cg = get_multiple_elements()
#
# if not selected_cg:
#     try:
#         filter_type = specialty_equip_filter
#         se_lst = selection.PickObjects(ObjectType.Element, filter_type, 'Select Corner Guards')
#         selected_cg = [doc.GetElement(se) for se in se_lst]
#
#         if not selected_cg:
#             forms.alert('No selection.', exitscript=True)
#
#     except Exception as e:
#         forms.alert(str(e))
#
# # --------------------------------------------------------------
#
# for cg in selected_cg:
#     type_id = cg.GetTypeId()
#     type_el = doc.GetElement(type_id)
#
#     if type_el:
#         type_name = type_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
#         if type_name == "VL/1500":
#             ELEMENTS_TO_REPLACE.append(cg)
#
# # --------------------------------------------------------------
#
#
# with Transaction(doc, __title__) as t:  # type: Transaction
#     t.Start()
#     try:
#         count = 0
#         for el in ELEMENTS_TO_REPLACE:
#             changed_type = set_type(el, REPLACEMENT_TYPE_900)
#             if changed_type:
#                 count += 1
#
#     except Exception as e:
#         forms.alert(str(e), exitscript=True, warn_icon=True)
#
#     else:
#         t.Commit()
#         forms.alert("Success!. Changed Elements: {} items".format(count), exitscript=False, warn_icon=False)

# ======================================================================================================

# se_collector = FECollectorCat(big_enum=BuiltInCategory.OST_SpecialityEquipment,
#                               selected_view_id=active_view.Id,
#                               by_instance=True)
#
# all_specialty_equip = se_collector.get_elements()
#
#
# with Transaction(doc, __title__) as t:  # type: Transaction
#     t.Start()
#     try:
#         count = 0
#         for el in all_specialty_equip:
#             type_id = el.GetTypeId()
#             type_el = doc.GetElement(type_id)
#
#             if type_el:
#                 type_name = type_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
#                 if type_name == "VL/900":
#                     el.ChangeTypeId(REPLACEMENT_TYPE_1500.Id)
#                     count += 1
#
#     except Exception as e:
#         forms.alert(str(e), exitscript=True)
#     else:
#         t.Commit()
#         forms.alert("Success!. Elements changed: {}".format(count), exitscript=False, warn_icon=False)
# ======================================================================================================
# se_collector = FECollectorCat(big_enum=BuiltInCategory.OST_SpecialityEquipment,
#                               selected_view_id=active_view.Id,
#                               by_instance=True)
#
# all_specialty_equip = se_collector.get_elements()
#
#
#
# with Transaction(doc, __title__) as t:  # type: Transaction
#     t.Start()
#     try:
#         count = 0
#         for el in all_specialty_equip:
#             if el.Location:
#                 type_id = el.GetTypeId()
#                 type_el = doc.GetElement(type_id)
#
#                 if type_el:
#                     if type_el.Category.Name == "Specialty Equipment":
#                         type_name = type_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
#                         if type_name == "VL_90_Degree":
#                             el.ChangeTypeId(REPLACEMENT_TYPE_1500.Id)
#                             count += 1
#                         elif type_name == "VL":
#                             el.ChangeTypeId(REPLACEMENT_TYPE_1500.Id)
#                             count += 1
#
#     except Exception as e:
#         forms.alert(str(e), exitscript=True)
#     else:
#         t.Commit()
#         forms.alert("Success! Total number of elements: {}".format(count), exitscript=False, warn_icon=False)

# ======================================================================================================

se_collector = FECollectorCat(big_enum=BuiltInCategory.OST_SpecialityEquipment,
                              selected_view_id=active_view.Id,
                              by_instance=True)

all_specialty_equip = se_collector.get_elements()

all_vl = []

for i in all_specialty_equip:
    for el in all_specialty_equip:
        type_id = el.GetTypeId()
        type_el = doc.GetElement(type_id)

        if type_el:
            type_name = type_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            if "VL" in type_name:
                all_vl.append(type_name)

count = Counter(all_vl)

for k, v in count.items():
    print("{}: {:,}".format(k, v))

# unique_vl = set(all_vl)
#
# for i in unique_vl:
#     print(i)

# ======================================================================================================

