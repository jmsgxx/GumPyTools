# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button, TextBox)
from Snippets._context_manager import rvt_transaction
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

components = [Label('View Family Type:'),
              ComboBox('view_fam', vft_dict),
              Label('Level:'),
              ComboBox('level_name', level_dict),
              Separator(),
              Button('Create')]

form = FlexForm('Create View Plan', components)
form.show()

user_input = form.values
view_family   = user_input['view_fam']
level_choice = user_input['level_name']


for view_plan in range(5):
    new_v_plan = ViewPlan.Create(doc, view_family, level_choice)
    new_v_plan.Name = "DOC_FP_FFL_08_50_{}".format(view_plan + 11)





