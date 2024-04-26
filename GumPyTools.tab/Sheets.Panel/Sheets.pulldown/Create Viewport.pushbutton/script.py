# -*- coding: utf-8 -*-

__title__ = 'Create Viewport'
__doc__ = """
Put views on sheet.
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from Snippets._x_selection import get_multiple_elements
from Snippets._context_manager import try_except
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)

import clr

clr.AddReference("System")
from System.Collections.Generic import List

# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel

# ======================================================================================================

selected_views = get_multiple_elements()
all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

chosen_view_str = None
chosen_sht_str = None

filtered_views = [view for view in selected_views if view.Name == chosen_view_str]
filtered_sheets = [sheet for sheet in all_sheets if sheet.SheetNumber == chosen_sht_str]
# ======================================================================================================
# 🐣 UI

components = [Label('View Name Keyword:'),
              TextBox('start_key', text=""),
              ComboBox('combobox1', {'Opt 1': 10.0, 'Opt 2': 20.0}),
              Label('Enter Name:'),
              TextBox('textbox1', Text="Default Value"),
              CheckBox('checkbox1', 'Check this'),
              Separator(),
              Button('Select')]

form = FlexForm('Put Views on sheets', components)
form.show()

user_input = form.values
start_str = user_input['start_key']

# ======================================================================================================
with try_except():
    for s, v in zip(filtered_sheets, filtered_views):
        s_number = s.SheetNumber
        v_name = v.Name
        v_name_key = v_name.startswith(start_str)

        # make a condition here
        sht_outline = s.Outline
        x = sht_outline.Max.U - sht_outline.Min.U
        y = sht_outline.Max.V - sht_outline.Min.V
        origin_pt = XYZ(x / 2.2, y / 2, 0)
        Viewport.Create(doc, s.Id, v.Id, origin_pt)

# TODO WORK ON THE FILTERING OF THE UI, DECIDE IF STARTSWITH, CONTAIN DO YOU WANT. NOT SURE YET HOW TO DO THE OPTIONS
