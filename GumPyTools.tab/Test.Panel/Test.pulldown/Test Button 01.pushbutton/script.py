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
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
from Snippets._x_selection import get_multiple_elements
from pyrevit import forms, script

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

all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()

ffl_level = []

for level in all_levels:
    if level.Name.startswith("N_") and level.Name.endswith("FFL"):
        ffl_level.append(level)


# level_list = ["B2", "B1", "LG", "L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9",
#               "L11", "L12", "L13", "L14", "L15", "L16"]
with rvt_transaction(doc, __title__):
    for i in range(17):
        for l in ffl_level:
            l_name = l.Name
            l_split = l_name.split("_")
            if l_split[1] == str(i).zfill(2):
                new_view = ViewPlan.Create(doc, ElementId(362112), l.Id)
                new_view.Name = "SS_DOC_L{}_200".format(i)


