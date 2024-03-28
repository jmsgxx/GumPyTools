# -*- coding: utf-8 -*-

__title__ = 'Tblock Replace'
__doc__ = """
Will replace the existing titleblock.

HOW TO:
1. Select sheets or multiple sheets.
2. Click the command and select the desired
title block.
3. Hit Create.

***IF YOU ENCOUNTER ANY ERROR OR ANY QUESTION,
CONTACT THE AUTHOR.👇
__________________________________
v1. 28 Mar 2024
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import FlexForm, Label, ComboBox, Separator, Button
from Autodesk.Revit.UI.Selection import Selection
from Snippets._x_selection import get_multiple_elements
from Snippets._context_manager import rvt_transaction
from Autodesk.Revit.DB import *
from pyrevit import forms
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
current_view    = active_view.Id

# =====================================================================================================
# 1️⃣ select all the title block instance first
all_tblocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks)\
    .WhereElementIsNotElementType()\
    .ToElements()

tb_type = {}

for t in all_tblocks:
    # get the type
    tb_type_id = t.GetTypeId()
    tb_type_el = doc.GetElement(tb_type_id)     # type: FamilySymbol

    fam_type = tb_type_el.FamilyName    # type name
    fam_ins = t.Name    # family name

    fam_key = ('{}: {}'.format(fam_type, fam_ins))

    if fam_key not in tb_type:
        tb_type[fam_key] = tb_type_el


# =====================================================================================================
# 2️⃣ UI
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
# 3️⃣ execute

# select sheet on the browser
selected_sheets = get_multiple_elements()

# will return a list of family instance
for sheet in selected_sheets:
    existing_tblock = FilteredElementCollector(doc, sheet.Id).OfClass(FamilyInstance)\
        .OfCategory(BuiltInCategory.OST_TitleBlocks)\
        .ToElements()


    with rvt_transaction(doc, __title__):
        # loop through the list of family instance
        for block in existing_tblock:
            block.Symbol = t_block_choice


