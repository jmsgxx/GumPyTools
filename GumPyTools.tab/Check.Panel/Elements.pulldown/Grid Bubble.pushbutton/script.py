# -*- coding: utf-8 -*-

__title__ = 'Grid Bubble'
__doc__ = """
This script will toggle the visibility of Grid Bubble.

HOW TO:

1. You can either select the elements first and hit
the command or;
2. Click the command, select the elements then click
'Finish' on the the upper left corner.

This will work for single or multiple grids.
__________________________________
Author: Joven Mark Gumana
v1. 25 May 2024
v2. 26 May 2024 - minimize button
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import ISelectionFilter_Classes
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Snippets._context_manager import try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import pyrevit
import sys
import clr

clr.AddReference("System")

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
# 🟥 functions


def start_bub_show(element):
    element.ShowBubbleInView(DatumEnds.End0, active_view)


def start_bub_hide(element):
    element.HideBubbleInView(DatumEnds.End0, active_view)


def end_bub_show(element):
    element.ShowBubbleInView(DatumEnds.End1, active_view)


def end_bub_hide(element):
    element.HideBubbleInView(DatumEnds.End1, active_view)


# ======================================================================================================
# 1️⃣ collect the grids
selected_grids = get_multiple_elements()

if not selected_grids:
    with try_except():
        filter_type = ISelectionFilter_Classes([Grid])
        grid_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_grids = [doc.GetElement(gr) for gr in grid_list]

    if not selected_grids:
        forms.alert('No wall selected', exitscript=True)


# ======================================================================================================
# 2️⃣ ui
both_pos = None
start_pos = None
end_pos = None
user_input = None

try:
    components = [Label("Show/Hide Bubble"),
                  Separator(),
                  CheckBox('start_bub', 'Start'),
                  CheckBox('end_bub', 'End'),
                  Separator(),
                  Label("If Bubble is on '✅ Start/End = Off'"),
                  Separator(),
                  Button('Select')]

    form = FlexForm("Grid Bubble View Toggle.v2", components)
    form.show()

    user_input = form.values
    start_pos   = user_input['start_bub']
    end_pos     = user_input['end_bub']

except KeyError:
    forms.alert('No input provide, please try again!', exitscript=True)
# ======================================================================================================
# 3️⃣ main command

for grid in selected_grids:     # type: Grid
    bubble_start_vis    = grid.IsBubbleVisibleInView(DatumEnds.End0, active_view)
    bubble_end_vis      = grid.IsBubbleVisibleInView(DatumEnds.End1, active_view)
    # -----------------------------------------------------------------------------
    with revit.Transaction(__title__):
        if start_pos and end_pos:
            if bubble_start_vis and bubble_end_vis:
                start_bub_hide(grid)
                end_bub_hide(grid)
            else:
                start_bub_show(grid)
                end_bub_show(grid)

        elif start_pos:
            if bubble_start_vis:
                start_bub_hide(grid)
            else:
                start_bub_show(grid)

        elif end_pos:
            if bubble_end_vis:
                end_bub_hide(grid)
            else:
                end_bub_show(grid)