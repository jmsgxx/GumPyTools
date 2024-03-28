# -*- coding: utf-8 -*-

__title__ = 'Test Button 03'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._x_selection import DoorCustomFilter, get_multiple_elements, ISelectionFilter_Classes
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
import pyrevit
from pyrevit import forms
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================

all_tblocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks)\
    .WhereElementIsNotElementType()\
    .ToElements()

tb_type = {}

for t in all_tblocks:
    tb_type_id = t.GetTypeId()
    tb_type_el = doc.GetElement(tb_type_id)     # type: FamilySymbol

    fam_type = tb_type_el.FamilyName
    fam_ins = t.Name

    fam_key = ('{}: {}'.format(fam_type, fam_ins))

    if fam_key not in tb_type:
        tb_type[fam_key] = tb_type_el


# =====================================================================================================
# UI
try:
    components = [Label('Select Title Block:'),
                  ComboBox('title_block', tb_type),
                  Separator(),
                  Button('Select')]

    form = FlexForm('Title Blocks', components)
    form.show()
    user_inputs = form.values

    t_block_choice     = user_inputs['title_block']

except KeyError:
    forms.alert('No input. Exiting script', exitscript=True)
# =====================================================================================================
# execute

selected_sheets = get_multiple_elements()

for sheet in selected_sheets:
    existing_tblock = FilteredElementCollector(doc, sheet.Id).OfClass(FamilyInstance)\
        .OfCategory(BuiltInCategory.OST_TitleBlocks)\
        .ToElements()


    with rvt_transaction(doc, __title__):
        for block in existing_tblock:
            block.Symbol = t_block_choice


