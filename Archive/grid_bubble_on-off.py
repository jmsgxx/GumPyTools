# -*- coding: utf-8 -*-

__title__ = 'Test Button 03'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection


# ======================================================================================================
selected_grids = get_multiple_elements()

if not selected_grids:
    with try_except():
        filter_type = ISelectionFilter_Classes([Grid])
        grid_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_grids = [doc.GetElement(gr) for gr in grid_list]

    if not selected_grids:
        forms.alert('No wall selected', exitscript=True)

bub_position = {
    'Start Bubble': 0,
    'End Bubble': 1
}

show_opt = {
    'Show': 0,
    'Hide': 1,
}

components = [Label('Bubble Position'),
              ComboBox('bub_pos', bub_position),
              Separator(),
              Label('Show or Hide'),
              ComboBox('show_hide', show_opt),
              Separator(),
              Button('Select')]
form = FlexForm("What's up Jack?", components)
form.show()

user_input = form.values
bubble = user_input['bub_pos']
show_hide = user_input['show_hide']

with rvt_transaction(doc, __title__):
    for grid in selected_grids:     # type: Grid
        if bubble == 0 and show_hide == 1:
            grid.HideBubbleInView(DatumEnds.End0, active_view)
        elif bubble == 0 and show_hide == 0:
            grid.ShowBubbleInView(DatumEnds.End0, active_view)
        elif bubble == 1 and show_hide == 1:
            grid.HideBubbleInView(DatumEnds.End1, active_view)
        elif bubble == 1 and show_hide == 0:
            grid.ShowBubbleInView(DatumEnds.End1, active_view)



