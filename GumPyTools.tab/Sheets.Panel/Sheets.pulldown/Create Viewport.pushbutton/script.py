# -*- coding: utf-8 -*-

__title__ = 'Create Viewport'
__doc__ = """
This script will put views on sheets.

***PLEASE READ***
1. FOR MULTIPLE SHEETS
- it will take the last 2 characters of View Name
and Sheet Number and see if it matches to 
create a viewport.

2. FOR SINGLE SHEET
- input exactly the full View Name and full Sheet Number

HOW TO USE:
- Select sheet/sheets from project browser
- Input the necessary keywords and press create
- Print statement will pop up if successful

CONTACT THE AUTHOR FOR ANY PROBLEM AND ERROR SO 
WE CAN SOLVE IT.
__________________________________
Author: Joven Mark Gumana
v1. 28 APR 2024
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
from pyrevit import script

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
# 🟩 function


def create_viewport(sheet_ref, view_ref):
    with try_except():
        sht_outline = sheet_ref.Outline
        x = sht_outline.Max.U - sht_outline.Min.U
        y = sht_outline.Max.V - sht_outline.Min.V
        origin_pt = XYZ(x / 2.2, y / 2, 0)
        Viewport.Create(doc, sheet_ref.Id, view_ref.Id, origin_pt)
        return True


def out_result(sht_num, sht_nam, vw_nam):
    print("{}_{}".format(sht_num, sht_nam))
    print("\t---{}".format(vw_nam))


# ======================================================================================================
output          = script.get_output()
selected_views  = get_multiple_elements()
all_sheets      = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

chosen_view_str = ''
chosen_sht_str = ''
# ======================================================================================================

# 🐣 UI
view_search_str     = None
sheet_search_str    = None

try:
    components = [Label('View Name Keyword'),
                  TextBox('view_input_str', text="text"),
                  Label('Sheet Number Keyword'),
                  TextBox('sheet_input_str', text="text"),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Put Views on sheets', components)
    form.show()

    user_input              = form.values
    view_search_str         = user_input['view_input_str']
    sheet_search_str        = user_input['sheet_input_str']

except Exception as e:
    forms.alert("{}.No Input.".format(e), exitscript=True)
# ======================================================================================================

#  🟨 main script

sheet_views = []

for s in all_sheets:     # type: ViewSheet
    if sheet_search_str in s.SheetNumber:
        sheet_views.append(s)


with rvt_transaction(doc, __title__):
    with try_except():

        counter = 0

        for s in sheet_views:
            for v in selected_views:
                output.center()
                output.resize(500, 700)
                s_number = s.SheetNumber
                s_name = s.Name
                v_name = v.Name
                # print("{}:{}".format(s_number, v_name))

                if s_number[-2:] == v_name[-2:]:
                    # print("{}:{}".format(s_number, v_name))
                    if create_viewport(s, v):
                        out_result(s_number, s_name, v_name)
                        counter += 1

                elif v_name == view_search_str and s_number == sheet_search_str:
                    if create_viewport(s, v):
                        out_result(s_number, s_name, v_name)
                        counter += 1

        if counter == 0:
            forms.alert("No sheets created. Exiting script.", exitscript=True, warn_icon=False)





