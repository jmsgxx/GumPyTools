# -*- coding: utf-8 -*-

__title__ = 'Duplicate View'
__doc__ = """
Will duplicate views as dependent.
- Input desired additional dependent
- Input previous number to follow (if any)
- Input desired view name
-------------------------------------
v1. 02 Feb 2024
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
selection = uidoc.Selection     # type: Selection

# ==========================================================x============================================
selected_view = get_multiple_elements()

num_add     = None
name_view   = None
prev_number = None

# 🟢 UI
try:
    components = [
        Label('No. of additional dependent'),
        TextBox('dep_num', default='1'),
        Label('Preceding Number'),
        TextBox('pre_num', default='0'),
        Separator(),
        Button('Create')
    ]

    form = FlexForm('Create View Plan', components)
    form.show()

    user_input = form.values
    prev_number = user_input['pre_num']
    num_add   = user_input['dep_num']

except KeyError:
    sys.exit()


view_names = []

# ---------------------------------------------------------------------------------------------
# MAIN

all_view_names = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
for v in all_view_names:
    if v:
        view_names.append(v.Name)

with rvt_transaction(doc, __title__):
    parent_view_name = None

    for view in selected_view:
        if type(view) == ViewPlan:
            parent_view_name = view.Name
            new_views = []
            if view.CanViewBeDuplicated(ViewDuplicateOption.AsDependent):
                for num in range(int(num_add)):
                    duplicate_view = ViewPlan.Duplicate(view, ViewDuplicateOption.AsDependent)
                    new_views.append(duplicate_view)


            for x, new_view_id in enumerate(new_views, start=1):
                n_view = doc.GetElement(new_view_id)
                if n_view.Name in view_names:
                    forms.alert("View name is already in the model.\nTry again.",
                                warn_icon=True, exitscript=True)
                else:
                    n_view.Name = "{}_{}".format(parent_view_name, str(x + int(prev_number)).zfill(2))

forms.alert("Duplicate views as dependents created!", warn_icon=False, exitscript=False)


