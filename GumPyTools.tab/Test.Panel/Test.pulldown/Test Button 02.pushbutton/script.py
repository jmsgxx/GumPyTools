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
from Autodesk.Revit.UI.Selection import Selection, ObjectType
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


# REPLACEMENT_TYPE = None
# ELEMENTS_TO_REPLACE = []
#
# # ------------------------------------------------
# all_ef_tags = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ElectricalFixtureTags).\
#     WhereElementIsElementType().ToElements()
#
# for tag_type in all_ef_tags:
#     tag_name = tag_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
#     if tag_name == 'Electrical Device Panel-Circuit Tag_RED':
#         REPLACEMENT_TYPE = tag_type
#
# # ------------------------------------------------
#
# selected_ef = get_multiple_elements()   # custom function
# el_filter = ElementCategoryFilter(BuiltInCategory.OST_ElectricalFixtureTags)
#
# for ef in selected_ef:  # electrical fixtures
#     # 🟡 electrical fixture element
#     param1 = ef.LookupParameter('Parameter1').AsValueString()
#     param2 = ef.LookupParameter('Parameter2').AsValueString()
#     param3 = ef.LookupParameter('Parameter3').AsValueString()
#
#     tag_el_ids = ef.GetDependentElements(el_filter)  # dependent tags on elements
#     for el_id in tag_el_ids:  # will get instance element id
#         ins_el = doc.GetElement(el_id)
#         el_type_id = ins_el.GetTypeId()     # type id
#         el_type = doc.GetElement(el_type_id)    # type element
#         el_name = el_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
#
#         if param1 == "1" and param2 == "2" and param3 == "3":
#             ELEMENTS_TO_REPLACE.append(ins_el)
#
# # ------------------------------------------------
# with rvt_transaction(doc, __title__):
#     for el in ELEMENTS_TO_REPLACE:
#         set_type(el, REPLACEMENT_TYPE)

BLUE_TAG = []
RED_TAG = []
REPLACEMENT_TAG_BLUE = None
REPLACEMENT_TAG_RED = None


# ---------------------------------------------------------------
all_ef_tags = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ElectricalFixtureTags).\
    WhereElementIsElementType().ToElements()

for tag in all_ef_tags:
    fam_name = tag.FamilyName
    if fam_name == 'TAG-RED':
        REPLACEMENT_TAG_RED = tag
    elif fam_name == 'TAG-BLUE':
        REPLACEMENT_TAG_BLUE = tag


# ---------------------------------------------------------------
all_el_fixture = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_ElectricalFixtures).\
    WhereElementIsNotElementType().ToElements()

el_filter = ElementCategoryFilter(BuiltInCategory.OST_ElectricalFixtureTags)

with rvt_transaction(doc, __title__):
    for ef in all_el_fixture:

        param1 = ef.LookupParameter('1-TAG-EQUIPAMENTO')

        param6 = ef.LookupParameter('6-REM-NUMERO DA FASE').AsValueString()
        param7 = ef.LookupParameter('7-REM-NUMERO DO PREDIO').AsValueString()
        param8 = ef.LookupParameter('8-REM-NUMERO SEQUENCIAL').AsValueString()

        dep_tags = ef.GetDependentElements(el_filter)
        for tag_id in dep_tags:
            ins_el = doc.GetElement(tag_id)

            tag_fam = ins_el.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM)
            if tag_fam:
                tag_fam_name = tag_fam.AsValueString()
                # print(tag_fam_name)


                if param6 == '15' and param7 == '02' and param8 == '03':
                    BLUE_TAG.append(ins_el)
                    param1.Set('BLUE')
                elif param6 == '15' and param7 == '02' and param8 == '02':
                    param1.Set("RED")
                    RED_TAG.append(ins_el)
    # ---------------------------------------------------------------
    for red in RED_TAG:
        fam_tag = red.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM)
        fam_tag.Set(REPLACEMENT_TAG_RED.Id)

    for blue in BLUE_TAG:
        fam_tag = blue.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM)
        fam_tag.Set(REPLACEMENT_TAG_BLUE.Id)


