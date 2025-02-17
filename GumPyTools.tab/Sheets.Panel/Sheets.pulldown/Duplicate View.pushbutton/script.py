# -*- coding: utf-8 -*-

__title__ = 'Duplicate View/s'
__doc__ = """
Will duplicate a singe view or multiple views as dependent,
stand alone or with detailing.

1. Select a single view or multiple views.
2. Run the command.
3. Input desired duplicate option
4. Input number of desired copies
5. Input previous number to follow (if any)
-------------------------------------
v1. 02 Feb 2024
v2. 26 Feb 2024 - Additional Duplicate Option
Author: Joven Mark Gumana
"""

import sys

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button, TextBox)
from Snippets._context_manager import rvt_transaction
from Autodesk.Revit.DB import *
from Snippets._x_selection import get_multiple_elements
from pyrevit import forms

import clr
clr.AddReference("System")


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝  variables
# ======================================================================================================

doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel


# ==========================================================x============================================
selected_view = get_multiple_elements()

# 🟠 duplicate option dictionary
dup_dict = {
    "Independent":      ViewDuplicateOption.Duplicate,
    "As Dependent":     ViewDuplicateOption.AsDependent,
    "With Detailing":   ViewDuplicateOption.WithDetailing
}

num_add     = None
name_view   = None
prev_number = None

# 🟢 UI
try:
    components = [Label('Duplicate Options'),
                  ComboBox('dup_option', dup_dict),
                  Label('No. of additional dependent'),
                  TextBox('dep_num', default='1'),
                  Label('Preceding Number'),
                  TextBox('pre_num', default='0'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Create View Plan', components)
    form.show()

    user_input      = form.values
    dup_opt         = user_input['dup_option']
    prev_number     = user_input['pre_num']
    num_add         = user_input['dep_num']

except KeyError:
    sys.exit()

# ---------------------------------------------------------------------------------------------
# MAIN

all_view_names = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
view_names = []

for v in all_view_names:
    if v:
        view_names.append(v.Name)

with rvt_transaction(doc, __title__):
    parent_view_name = None

    for view in selected_view:
        if type(view) == ViewPlan:
            parent_view_name = view.Name
            new_views = []
            if view.CanViewBeDuplicated(dup_opt):
                for num in range(int(num_add)):
                    duplicate_view = view.Duplicate(dup_opt)
                    new_views.append(duplicate_view)

            if len(new_views) != 0:
                forms.alert("Duplicate views as dependents created!", warn_icon=False, exitscript=False)

            # for x, new_view_id in enumerate(new_views, start=1):
            #     n_view = doc.GetElement(new_view_id)
            #     if n_view.Name in view_names:
            #         forms.alert("View name is already in the model.\nTry again.",
            #                     warn_icon=True, exitscript=True)
            #     else:
            #         n_view.Name = "{}_{}".format(parent_view_name, str(x + int(prev_number)).zfill(2))
            #         forms.alert("Duplicate views as dependents created!", warn_icon=False, exitscript=False)
