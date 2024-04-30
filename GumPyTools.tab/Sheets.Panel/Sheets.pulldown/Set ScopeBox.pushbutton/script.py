# -*- coding: utf-8 -*-

__title__ = 'Set ScopeBox'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script
from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from pyrevit import forms, revit
import pyrevit
import sys
import clr
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

# ======================================================================================================

selected_views = get_multiple_elements()
all_scope_bx = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_VolumeOfInterest).ToElements()
output = script.get_output()

# ----------------------------------------------------------------------------------------------------------
# 🔴 UI
sb_search_str = None
try:
    components = [Label('Scope Box Keyword'),
                  TextBox('sb_input_str', text=""),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Put Views on sheets', components)
    form.show()

    user_input              = form.values
    sb_search_str         = user_input['sb_input_str']

except Exception as e:
    forms.alert("{}.No Input.".format(e), exitscript=True)

# ----------------------------------------------------------------------------------------------------------
# 🔵 MAIN SCRIPT
with rvt_transaction(doc, __title__):

    output.center()
    output.resize(400, 700)

    for view in selected_views:
        for scope_bx in all_scope_bx:
            """
            be careful with looping, for some reason this motherfucker gave me a hard time.
            """
            view_p_name = view.Name
            scope_bx_name = scope_bx.Name
            if scope_bx_name.startswith(sb_search_str) and view_p_name[-3:] == scope_bx_name[-3:]:
                view_s_box = view.get_Parameter(BuiltInParameter.VIEWER_VOLUME_OF_INTEREST_CROP)
                view_s_box.Set(scope_bx.Id)
                print("View Name:\t\t\t{}\nScope Box Name: {}\n--------".format(view_p_name, scope_bx_name))


