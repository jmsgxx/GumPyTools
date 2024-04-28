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
from Snippets._context_manager import try_except, rvt_transaction
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

chosen_view_str = ''
chosen_sht_str = ''


def create_viewport(sheet_ref, view_ref):
    sht_outline = sheet_ref.Outline
    x = sht_outline.Max.U - sht_outline.Min.U
    y = sht_outline.Max.V - sht_outline.Min.V
    origin_pt = XYZ(x / 2.2, y / 2, 0)
    Viewport.Create(doc, sheet_ref.Id, view_ref.Id, origin_pt)


def starts_with(vw_name, chosen_str):
    return vw_name.startswith(str(chosen_str))


def contains(vw_name, chosen_str):
    return str(chosen_str) in vw_name


def equals(vw_name, chosen_str):
    return str(chosen_str) == vw_name


def ends_with(vw_name, chosen_str):
    return vw_name.endswith(str(chosen_str))


option_methods = {
    'Starts With': starts_with,
    'Contains': contains,
    'Equals': equals,
    'Ends With': ends_with
}

# view
view_opt_dict = {}

for view in selected_views:
    view_name = view.Name
    for option, method in option_methods.items():
        result = method(view_name, chosen_view_str)
        view_opt_dict[option] = result

# sheet
sheet_opt_dict = {}

for sheet in all_sheets:
    sheet_name = sheet.Name
    for option, method in option_methods.items():
        result = method(sheet_name, chosen_sht_str)
        sheet_opt_dict[option] = result
# ======================================================================================================
# 🐣 UI

components = [Label('Search Method for View Name'),
              ComboBox('view_option_method', view_opt_dict),
              Label('Input Words to Search'),
              TextBox('view_input_str', text="text"),
              Label('Search Method for Sheet Number'),
              ComboBox('sheet_option_method', sheet_opt_dict),
              TextBox('sheet_input_str', text="text"),
              Separator(),
              Button('Create')]

form = FlexForm('Put Views on sheets', components)
form.show()

user_input              = form.values
view_method_option      = user_input['view_option_method']
view_search_str         = user_input['view_input_str']
sheet_method_option     = user_input['sheet_option_method']
sheet_search_str        = user_input['sheet_input_str']

# ======================================================================================================

view_plans = []

for v in selected_views:
    if view_search_str in v.Name:
        view_plans.append(v)


sheet_views = []

for s in all_sheets:     # type: ViewSheet
    if sheet_search_str in s.SheetNumber:
        sheet_views.append(s)


with rvt_transaction(doc, __title__):
    # try:
    for s in sheet_views:
        for v in view_plans:
            s_number = s.SheetNumber
            v_name = v.Name
            # print("{}:{}".format(s_number, v_name))

            if s_number[-2:] == v_name[-2:]:
                # print("{}:{}".format(s_number, v_name))
                create_viewport(s, v)
            elif v_name == view_search_str and s_number == sheet_search_str:
                create_viewport(s, v)

    # except Exception as e:
    #     forms.alert(str(e))

forms.alert("Views Created!", warn_icon=False)

# todo conditions is irrelevant now, fixed the UI will only work either string in name, or exactly equal
