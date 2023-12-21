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
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
from datetime import datetime
import pyrevit
import clr
import sys
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


# 🟦 SELECT PARAM VALUE OF PLOT BATCH FROM THE LIST
plot_batch_value = forms.SelectFromList.show(set(plot_batch),
                                             multiselect=True,
                                             button_name='Select',
                                             title='Select Plot Batch Value')  # should accept a list on first argument

# plot_batch_value    = forms.ask_for_string(title="Param String", prompt="Put parameter value")
if not plot_batch_value:    # exit the command if no value chosen
    sys.exit()


view_set_name       = forms.ask_for_string(title="View Set Name", prompt="Input view set name")
if not view_set_name:
    sys.exit()

# initialize view set
current_view_set = ViewSet()

for vs in all_sheets:
    param_vs = vs.LookupParameter('Plot Batch')
    for plot_batch_item in plot_batch_value:
        if param_vs and param_vs.AsString() == plot_batch_item:
            current_view_set.Insert(vs)


print_manager               = doc.PrintManager
print_manager.PrintRange    = PrintRange.Select
view_sheet_setting                              = print_manager.ViewSheetSetting
view_sheet_setting.CurrentViewSheetSet.Views    = current_view_set      # set to current view set

with Transaction(doc, "Create ViewSet") as t:
    t.Start()

    set_name = view_set_name
    try:
        view_sheet_setting.SaveAs(set_name)
        forms.alert("Total number of sheets in set '{}'".format(current_view_set.Size), exitscript=False, warn_icon=False)
    except Exception as e:
        output.print_md("### {} Delete first the view set that is causing the problem using 'View Set Delete'.".format(e))
        sys.exit()

    t.Commit()



