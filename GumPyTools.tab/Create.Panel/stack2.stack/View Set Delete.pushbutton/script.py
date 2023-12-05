# -*- coding: utf-8 -*-

__title__ = 'View Set Delete'
__doc__ = """
This script will delete the 
selected view set.

HOW TO:

- Run the command. 
- Select the desired view sets.
- Hit ok
__________________________________
v1. 05 Dec 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
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


collector = FilteredElementCollector(doc).OfClass(ViewSheetSet)
collector_name = sorted([item.Name for item in collector])
chosen_view_set = forms.SelectFromList.show(collector_name, title="Select View Set to Delete", button_name='Select Set', multiselect=True)

with Transaction(doc, __title__) as t:
    t.Start()

    deleted_view_set = []
    deleted_view_set_names = []
    if not chosen_view_set:
        sys.exit()
    else:
        for view_set in collector:
            if view_set.Name in chosen_view_set:
                deleted_view_set.append(view_set.Id)
                deleted_view_set_names.append(view_set.Name)

    for view_id in deleted_view_set:
        doc.Delete(view_id)

    t.Commit()

    forms.alert('View Sets Deleted\n{}'.format("\n".join(deleted_view_set_names)), exitscript=False)


