# -*- coding: utf-8 -*-

__title__ = 'WallByLine'
__doc__ = """
This script will unconnected wall/s by selecting lines.

HOW TO:
1. Create lines to be converted as a wall.
2. Select those lines or click the command then
select lines and press finish.
3. Specify wall type from pull down menu.
4. Specify height in millimeters.
5. Hit create button.

NOTE: This will create an unconnected height of walls.

TODO: Create an interface for connected levels.
__________________________________
v1. 24 Jan 2024
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)
from Snippets._convert import convert_internal_units
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms
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
# 1️⃣ select wall
line_selection = get_multiple_elements()

if not line_selection:
    with try_except():
        filter_type = ISelectionFilter_Classes([ModelLine])
        line_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Lines")
        line_selection = [doc.GetElement(dr) for dr in line_list]

        if not line_selection:
            forms.alert("No line selected. Exiting command.", exitscript=True, warn_icon=False)

# =====================================================================================================
# 2️⃣ UI
wall_types      = FilteredElementCollector(doc).OfClass(WallType).ToElements()
wall_type_dict  = {wall.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString(): wall.Id for wall in wall_types}

wall_choice = None
ht_val = None

try:
    components = [Label('Select Wall:'),
                  ComboBox('wall_type_var', wall_type_dict),
                  Label('Wall Height:'),
                  TextBox('ht_value'),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Create Wall', components)
    form.show()
    user_inputs = form.values

    wall_choice     = user_inputs['wall_type_var']
    ht_choice       = user_inputs['ht_value']
    ht_val          = convert_internal_units(int(ht_choice), True, 'mm')

except KeyError as e:
    forms.alert('No input selected.',
                exitscript=True,
                warn_icon=True)

# =====================================================================================================
# 3️⃣ Create wall
with rvt_transaction(doc, __title__):
    try:
        line_list = []
        for line in line_selection:     # type: ModelLine
            curve       = line.GeometryCurve
            start_pt    = curve.GetEndPoint(0)
            end_pt      = curve.GetEndPoint(1)
            l_curve     = Line.CreateBound(start_pt, end_pt)
            line_list.append(l_curve)

        for el in line_list:
            """
            args: Document, list of curves, ElementID Wall, ElementID Level,
             height dbl, offset dbl, flip bool, struc bool
            """
            create_wall = Wall.Create(doc, el, wall_choice, active_level.Id, ht_val, 0, False, False)

    except Exception as e:
        forms.alert(str(e))

    else:
        if create_wall:
            for line in line_selection:
                doc.Delete(line.Id)
