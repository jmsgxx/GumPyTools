# -*- coding: utf-8 -*-

__title__ = 'View Set API'
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
clr.AddReference("System")



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

plot_batch_value = forms.ask_for_string(title="Param String", prompt="Put parameter value")
view_set_name = forms.ask_for_string(title="View Set Name", prompt="Input view set name")

# collect the view sheets
view_sheet = FilteredElementCollector(doc).OfClass(ViewSheet)

# initialize view set
my_view_set = ViewSet()

for vs in view_sheet:
    param_vs = vs.LookupParameter('Plot Batch')
    if param_vs and param_vs.AsString() == plot_batch_value:
        my_view_set.Insert(vs)

# get the PrintManager from the current document
print_manager = doc.PrintManager

# set this PrintManager to use the "Selected Views/Sheets" option
print_manager.PrintRange = PrintRange.Select

# get the ViewSheetSetting which manages the view/sheet set information of current document
view_sheet_setting = print_manager.ViewSheetSetting

# set the views in this ViewSheetSetting to the newly created ViewSet
view_sheet_setting.CurrentViewSheetSet.Views = my_view_set

# if len(my_view_set) == 0:
#     TaskDialog.Show("Error", "No sheet numbers contain '{}'".format(param_vs.AsValueString()))

with Transaction(doc, "Create ViewSet") as t:
    t.Start()

    set_name = view_set_name

    view_sheet_setting.SaveAs(set_name)
    forms.alert("Total number of sheets in set '{}'".format(my_view_set.Size), exitscript=False, warn_icon=False)

    t.Commit()
