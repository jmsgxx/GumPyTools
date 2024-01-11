# -*- coding: utf-8 -*-

__title__ = 'View Set Create'
__doc__ = """
Create a View Set the relies the on 
the value of project parameter "Plot
Batch" of Sheets.
HOW TO:
1. Type the value of the Plot Batch
of the sheets.
2. Input a preferred name for View Set.
It will automatically be created as the
View Set.
__________________________________
v1. 04 Dec 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button, TextBox)
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
from datetime import datetime
import pyrevit
import clr
import sys
from Snippets._context_manager import rvt_transaction, try_except
clr.AddReference("System")



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

output = pyrevit.output.get_output()
output.center()
output.resize(200, 300)


all_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

# 🟥 GET THE VALUE OF PLOT BATCH AND PUT IN THE LIST
plot_batch = []
for sheet in all_sheets:
    if sheet:
        plot_batch_param = sheet.LookupParameter('Plot Batch')
        if plot_batch_param.HasValue:
            plot_batch.append(plot_batch_param.AsString())


# 🟦 CREATE A DICTIONARY FOR VALUES IN PLOT BATCH
plot_batch_value = {name: name for name in set(plot_batch)}

# =====================================================================================
# 🟦 UI
view_set_name = None
pl_batch_val = None

try:
    components = [Label('Plot Batch Value:'),
                  ComboBox('view_set_val', plot_batch_value),
                  Label('View Set Name:'),
                  TextBox('input_name'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('View Set Create', components)
    form.show()

    user_input = form.values
    pl_batch_val   = user_input['view_set_val']
    view_set_name  = user_input['input_name']

    if not view_set_name:
        forms.alert("Please input a view name.\nTry again.", exitscript=True, warn_icon=True)

except KeyError:
    forms.alert("No values provided. Exiting command", exitscript=True, warn_icon=True)

# =====================================================================================
# initialize view set
current_view_set = ViewSet()

for vs in all_sheets:       # type: View
    param_vs = vs.LookupParameter('Plot Batch').AsString()
    if param_vs == pl_batch_val:
        current_view_set.Insert(vs)


print_manager                                   = doc.PrintManager
print_manager.PrintRange                        = PrintRange.Select
view_sheet_setting                              = print_manager.ViewSheetSetting
view_sheet_setting.CurrentViewSheetSet.Views    = current_view_set      # set to current view set

with rvt_transaction(doc, __title__):
    with try_except():
        view_sheet_setting.SaveAs(view_set_name)
        forms.alert("Total number of sheets in set '{}'".format(current_view_set.Size),
                    exitscript=False,
                    warn_icon=False)





