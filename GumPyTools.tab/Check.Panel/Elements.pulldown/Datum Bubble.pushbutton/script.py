# -*- coding: utf-8 -*-

__title__ = 'Datum Bubble'
__doc__ = """
This script will toggle the visibility of datum and Level Bubble.

HOW TO:

1. You can either select the elements first and hit
the command or;
2. Click the command, select the elements then click
'Finish' on the the upper left corner.

- If 'Start' is selected, 'End' will turn off and vice versa.
- If 'Start and 'End' are both selected. It will turn on both
the bubble and vice versa.
- Do a trial end error to know which is start and end.

This will work for single or multiple datums and levels.
__________________________________
Author: Joven Mark Gumana
v1. 25 May 2024
v2. 26 May 2024 - minimize button and added Level
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
selected_datum = get_multiple_elements()

if not selected_datum:
    with try_except():
        filter_type = ISelectionFilter_Classes([Grid, Level])
        datum_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
        selected_datum = [doc.GetElement(gr) for gr in datum_list]

    if not selected_datum:
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
                  Label("NOTE: ✅ Start and ✅ End = On/Off both sides"),
                  Separator(),
                  Button('Select')]

    form = FlexForm("Datum Bubble View Toggle.v2", components)
    form.show()

    user_input = form.values
    start_pos   = user_input['start_bub']
    end_pos     = user_input['end_bub']

except KeyError:
    forms.alert('No input provided, please try again!', exitscript=True)
# ======================================================================================================
# 3️⃣ main command

for datum in selected_datum:     # type: Grid
    bubble_start_vis    = datum.IsBubbleVisibleInView(DatumEnds.End0, active_view)
    bubble_end_vis      = datum.IsBubbleVisibleInView(DatumEnds.End1, active_view)
    # -----------------------------------------------------------------------------
    with revit.Transaction(__title__):
        if start_pos and end_pos:
            if bubble_start_vis and bubble_end_vis:
                start_bub_hide(datum)
                end_bub_hide(datum)
            else:
                start_bub_show(datum)
                end_bub_show(datum)

        elif start_pos:
            start_bub_show(datum)
            end_bub_hide(datum)

        elif end_pos:
            end_bub_show(datum)
            start_bub_hide(datum)
