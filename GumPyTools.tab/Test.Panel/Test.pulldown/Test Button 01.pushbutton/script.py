# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)
from Snippets._convert import convert_internal_units
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button)
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================

all_t_blocks = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()


# get tblock type first

selected_sheets = get_multiple_elements()

t_block_dict = {t_block.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString(): t_block for t_block in all_t_blocks}

components = [Label('Select Title Block:'),
              ComboBox('title_block', t_block_dict),
              Separator(),
              Button('Select')]

form = FlexForm('Title Blocks', components)
form.show()
user_inputs = form.values

t_block_choice     = user_inputs['title_block']

with rvt_transaction(doc, __title__):
    for sheet in selected_sheets:
        existing_tblock = FilteredElementCollector(doc, sheet.Id).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()
        if existing_tblock:
            existing_tblock.Symbol = t_block_choice

