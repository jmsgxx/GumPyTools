# -*- coding: utf-8 -*-

__title__ = 'Views Create'
__doc__ = """
Will create view plan.
- Select View Type
- Select level
- Select number of view you want to create
------------------------------------
v1. 02 Feb 2024
v2. 26 Apr 2024 - optimized ViewFamilyType
Author: Joven Mark Gumana
"""

import sys

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import forms
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button, TextBox)
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
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
# 🔴 view family type
all_vft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

# get only the ViewFamilyType for plans, e.g, floor plan, ceiling, area plan
view_fam = [v for v in all_vft if "plan" in str(v.ViewFamily).lower()]

view_fam_dict = {view.ViewFamily: view.Id for view in view_fam}

# --------------------------------------------------------------------------------------------------
# 🔴 levels
all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
level_dict = {level.Name: level.Id for level in all_levels}
# --------------------------------------------------------------------------------------------------
view_family     = None
level_choice    = None
v_name          = None
# --------------------------------------------------------------------------------------------------
# 🔴 UI

try:
    components = [Label('View Type:'),
                  ComboBox('view_family_type', view_fam_dict),
                  Label('Level:'),
                  ComboBox('level_name', level_dict),
                  Label('View Name'),
                  TextBox('main_name'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Create View Plan', components)
    form.show()

    user_input = form.values
    view_family   = user_input['view_family_type']
    level_choice = user_input['level_name']
    v_name = user_input['main_name']

except Exception as e:
    sys.exit()
# --------------------------------------------------------------------------------------------------
# ✅ MAIN

with rvt_transaction(doc, __title__):
    with try_except():
        new_v_plan = ViewPlan.Create(doc, view_family, level_choice)
        new_v_plan.Name = "{}".format(v_name)

forms.alert("Views created!", exitscript=False, warn_icon=False)
