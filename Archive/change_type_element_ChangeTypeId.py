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


REPLACEMENT_TYPE = None
ELEMENTS_TO_REPLACE = []

# ------------------------------------------------
all_ef_tags = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ElectricalFixtureTags).\
    WhereElementIsElementType().ToElements()

for tag_type in all_ef_tags:
    tag_name = tag_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if tag_name == 'Electrical Device Panel-Circuit Tag_RED':
        REPLACEMENT_TYPE = tag_type

# ------------------------------------------------

selected_ef = get_multiple_elements()   # custom function
el_filter = ElementCategoryFilter(BuiltInCategory.OST_ElectricalFixtureTags)

for ef in selected_ef:      # electrical fixtures
    tag_el_ids = ef.GetDependentElements(el_filter)     # dependent tag on elements
    for el_id in tag_el_ids:    # will get instance element id
        ins_el = doc.GetElement(el_id)
        el_type_id = ins_el.GetTypeId()     # type id
        el_type = doc.GetElement(el_type_id)    # type element
        el_name = el_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()

        # 🟢 instance element to replace
        if el_name == 'Electrical Device Panel-Circuit Tag_WHITE':
            ELEMENTS_TO_REPLACE.append(ins_el)

# ------------------------------------------------
with rvt_transaction(doc, __title__):
    for el in ELEMENTS_TO_REPLACE:
        set_type(el, REPLACEMENT_TYPE)
