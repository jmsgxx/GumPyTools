# -*- coding: utf-8 -*-

__title__ = 'Views Create'
__doc__ = """
Will create view plan.
- Select View Type
- Select level
- Select number of view you want to create
------------------------------------
v1. 02 Feb 2024
Author: Joven Mark Gumana
"""


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
selection = uidoc.Selection     # type: Selection

# ==========================================================x============================================
# 🔴 view family type
all_vft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

vft_types = [i for i in all_vft if i.ViewFamily == ViewFamily.FloorPlan]

view_fam_types = []

for item in vft_types:
    vf_type_id = item.Id
    vf_type_element = doc.GetElement(vf_type_id)
    view_fam_types.append(vf_type_element)
    # vf_type_name = vf_type_element.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()

vft_dict = {name.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString(): name.Id for name in view_fam_types}

# --------------------------------------------------------------------------------------------------
# 🔴 levels
all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()

# for level in all_levels:
#     print(level.Name)

level_dict = {level.Name: level.Id for level in all_levels}
# --------------------------------------------------------------------------------------------------
num_add         = None
view_family     = None
level_choice    = None
v_name          = None

# --------------------------------------------------------------------------------------------------
# 🔴 UI
try:
    components = [Label('View Type:'),
                  ComboBox('view_family_type', vft_dict),
                  Label('Level:'),
                  ComboBox('level_name', level_dict),
                  Label('View Name'),
                  TextBox('main_name'),
                  Label('Desired Number of Views'),
                  TextBox('run_num', default='1'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Create View Plan', components)
    form.show()

    user_input = form.values
    view_family   = user_input['view_family_type']
    level_choice = user_input['level_name']
    v_name = user_input['main_name']
    num_add = user_input['run_num']
except Exception as e:
    forms.alert("Key error '{}'. Because no input.".format(str(e)), exitscript=True)
# --------------------------------------------------------------------------------------------------
# ✅ MAIN

with rvt_transaction(doc, __title__):
    with try_except():
        for i in range(int(num_add)):
            new_v_plan = ViewPlan.Create(doc, view_family, level_choice)
            new_v_plan.Name = "{}_{}".format(v_name, str(i + 1).zfill(2))


forms.alert("Views created!", exitscript=False, warn_icon=False)
