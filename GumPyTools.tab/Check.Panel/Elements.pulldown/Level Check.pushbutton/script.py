# -*- coding: utf-8 -*-

__title__ = 'Level Check'
__doc__ = """
level print out

*** CONTACT THE AUTHOR FOR TROUBLESHOOTING ***
--------------------------
Author: Joven Mark Gumana

v1. 12 Aug 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button)
from Snippets._convert import convert_internal_units
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from pyrevit import forms, script
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
# 🚦 function


def get_sorted_result(sorted_list):
    result = []
    for idx, (l_name, l_val) in enumerate(sorted_list):
        level_diff_flt = None
        if idx == 0:
            level_diff = ''
        else:
            level_diff = float(l_val) - float(sorted_list[idx - 1][1])
            level_diff_flt = "{:.0f}".format(level_diff)
        result.append((l_name, l_val, level_diff_flt))

    sorted_result = sorted(result, key=lambda x: float(x[1]))
    return sorted_result

# =====================================================================================================


# 1️⃣ collect all the levels
all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

nab_ffl = []
nab_sfl = []
eb_ffl = []
eb_sfl = []
data = []

# 2️⃣ iterate on list and get the parameters
for i in all_levels:
    level_name = i.Name
    level_val = i.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
    # 🟪 convert from feet to mm
    level_val_conv = convert_internal_units(float(level_val), False, "mm")

    # 🟡 new block ffl
    if level_name.startswith("N") and "FFL" in level_name:
        nab_ffl.append((level_name, "{:.0f}".format(level_val_conv)))
    # 🟡 new block sfl
    elif level_name.startswith("N") and "SFL" in level_name:
        nab_sfl.append((level_name, "{:.0f}".format(level_val_conv)))
    # 🟡 existing block ffl
    elif level_name.startswith("E") and "FFL" in level_name:
        eb_ffl.append((level_name, "{:.0f}".format(level_val_conv)))
    # 🟡 existing block sfl
    elif level_name.startswith("E") and "SFL" in level_name:
        eb_sfl.append((level_name, "{:.0f}".format(level_val_conv)))

    elif level_name == "DATUM":
        nab_ffl.append((level_name, "{:.0f}".format(level_val_conv)))
        nab_sfl.append((level_name, "{:.0f}".format(level_val_conv)))
        eb_ffl.append((level_name, "{:.0f}".format(level_val_conv)))
        eb_sfl.append((level_name, "{:.0f}".format(level_val_conv)))

    # 🟢 all levels
    data.append((level_name, "{:.0f}".format(level_val_conv)))

sorted_nab_ffl     = sorted(nab_ffl, key=lambda x: float(x[1]))
sorted_nab_sfl     = sorted(nab_sfl, key=lambda x: float(x[1]))
sorted_eb_ffl      = sorted(eb_ffl, key=lambda x: float(x[1]))
sorted_eb_sfl      = sorted(eb_sfl, key=lambda x: float(x[1]))
sorted_data        = sorted(data, key=lambda x: float(x[1]))



# 🟩 call the function
nab_ffl          = get_sorted_result(sorted_nab_ffl)
nab_sfl          = get_sorted_result(sorted_nab_sfl)
eb_ffl           = get_sorted_result(sorted_eb_ffl)
eb_sfl           = get_sorted_result(sorted_eb_sfl)
all_data         = get_sorted_result(sorted_data)

# 👀3️⃣ UI
# -------------------------------------------------------------------------------
lev_dict = {
    "NAB FFL": nab_ffl,
    "NAB SFL": nab_sfl,
    "EB FFL": eb_ffl,
    "EB SFL": eb_sfl,
    "ALL FFL and SFL": all_data
}
select_param = None
try:
    components = [Label('Check Levels:'),
                  ComboBox('select_param', lev_dict),
                  Separator(),
                  Button('Select')]

    form = FlexForm('Create View Plan', components)
    form.show()

    user_input = form.values
    select_param = user_input['select_param']
except Exception as e:
    forms.alert("Error. No input given. Try again".format(str(e)), warn_icon=True, exitscript=True)
# -------------------------------------------------------------------------------
# 4️⃣ output
output = script.get_output()
output.center()
output.resize(400, 800)
try:
    output.print_table(table_data=list(select_param),
                       title='Levels',
                       columns=['Level Name', 'Elevation', 'Difference'],
                       formats=["", "", "{}"])
except Exception as e:
    forms.alert("Error. Attribute cannot be found. Try again.", warn_icon=True, exitscript=True)



